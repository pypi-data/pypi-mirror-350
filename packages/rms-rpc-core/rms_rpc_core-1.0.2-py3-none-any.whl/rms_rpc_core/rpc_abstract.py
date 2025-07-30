""" Модуль абстрактных (исходных) RPC объектов. """

import asyncio
import traceback
import uuid
from asyncio import AbstractEventLoop, TimeoutError, get_event_loop
from typing import Any, Dict, Optional, Type

import msgpack
from aio_pika.abc import AbstractIncomingMessage
from aio_pika.message import IncomingMessage
from aio_pika.patterns import RPC
from aio_pika.patterns.rpc import RPCException, RPCMessageType
from aiormq.tools import shield

from rms_rpc_core.base.rpc_base import BaseAMQP, log
from rms_rpc_core.base.rpc_exceptions import RPCRuntimeError
from rms_rpc_core.utils import get_full_class_path


class MsgPackRPC(RPC):
    """ Класс RPC с сериализатором MessagePack. """
    SERIALIZER = msgpack
    CONTENT_TYPE: str = "application/x-msgpack"

    async def on_result_message(self, message: AbstractIncomingMessage) -> None:  # noqa: WPS231
        """
            Метод обработки сообщения о результате.

            Arguments:
                - message: Входящее сообщение.
        """
        if message.correlation_id is None:
            log.warning(
                "Получено сообщение без идентификатора корреляции (correlation_id): %r",
                message,
            )
            return

        future = self.futures.pop(message.correlation_id, None)

        if future is None:
            log.warning("Неизвестное сообщение: %r", message)
            return

        try:
            payload = await self.deserialize_message(message)
        except Exception as exc:
            log.error("Ошибка десериализации ответа в сообщении: %r", message)
            future.set_exception(exc)
            return

        if (not future.cancelled()) and (not future.done()):
            if message.type == RPCMessageType.RESULT.value:
                future.set_result(payload)
            elif message.type == RPCMessageType.ERROR.value:
                if not isinstance(payload, Exception):
                    payload = RPCException("Обернутый объект, не является исключением", payload)
                future.set_exception(payload)
            elif message.type == RPCMessageType.CALL.value:
                future.set_exception(
                    TimeoutError("Время ожидания сообщения истекло", message),
                )
            else:
                future.set_exception(
                    RuntimeError(f"Неизвестный тип сообщения {message.type}"),
                )

    @staticmethod
    def user_decode(obj) -> Any:
        """
            Метод декодирования объекта.

            Arguments:
                - obj: Объект декодирования.

            Returning:
                Декодированный объект
        """
        if "__uuid__" in obj:
            try:
                return uuid.UUID(hex=str(obj["as_str"]))
            except ValueError:
                return uuid.UUID(hex=str(obj["as_str"].decode("ascii")))

        if "__exception__" in obj:
            return RPCRuntimeError(
                traceback=obj.get("error", {}).get("traceback", "Haven't traceback"),
                origin_exc=obj.get("error", {}).get("exc", "Haven't error message"),
                args=obj.get("error", {}).get("args", "Haven't error"),
            )

        return obj

    @staticmethod
    def user_encode(obj):
        """
            Метод кодирования объекта.

            Arguments:
                - obj: Объект кодирования.

            Returning:
                Кодированный объект
        """
        if isinstance(obj, uuid.UUID):
            return {
                "__uuid__": True,
                "as_str": str(obj.hex).encode("ascii"),
            }

        if isinstance(obj, Exception):
            err = RPCRuntimeError(
                origin_exc=get_full_class_path(obj),
                traceback=traceback.format_exc(),
            )

            return MsgPackRPC._serialize_exception(err)

        return obj

    def serialize_exception(self, exception: Exception) -> Dict[str, Any]:  # type: ignore
        """
            Метод сериализации ошибки.

            Arguments:
                - exception: Вызванная ошибка.

            Returning:
                Сериализованная ошибка (объект).
        """
        return self._serialize_exception(exception)

    def serialize(self, data: Any) -> bytes:
        """
            Метод сериализации данных.

            Arguments:
                - data: Данные для сериализации.

            Returning:
                Сериализованные данные.
        """
        return self.SERIALIZER.packb(
            data,
            default=self.user_encode,
        )

    def deserialize(self, data: Any) -> bytes:
        """
            Метод десериализации данных.

            Arguments:
                - data: Данные для десериализации.

            Returning:
                Десриализованные данные.
        """
        # NOTE raw=False - исправляет проблему с тем что ключ в словаре инициализируется как byte
        test = self.SERIALIZER.unpackb(
            data,
            raw=False,
            object_hook=self.user_decode,
        )

        return test

    async def on_call_message(  # noqa WPS217
        self,
        method_name: str,
        message: IncomingMessage,
    ) -> None:
        """
            Метод обработки сообщения вызова.

            Arguments:
                - method_name: Вызванный метод;
                - message: Сообщение.
        """
        if method_name not in self.routes:
            log.warning("Method %r not registered in %r", method_name, self)
            return

        try:
            payload = await self.deserialize_message(message)
            func = self.routes[method_name]
            result: Any = await self.execute(func, payload)
            message_type = RPCMessageType.RESULT
        except Exception as err:
            result = self.serialize_exception(err)
            message_type = RPCMessageType.ERROR

        if not message.reply_to:
            log.info("Сообщение RPC без заголовка \"reply_to\" %r."
                     "Результат вызова будет потерян", message)
            await message.ack()
            return

        # Переписываем on_call_message из RPC,
        # так как испраивли баг залипания при ошибках сериализации в aio-pika==8.2.5.
        # Это исправлено в aio-pika>=9.0.0.
        try:
            result_message = await self.serialize_message(
                payload=result,
                message_type=message_type,
                correlation_id=message.correlation_id,
                delivery_mode=message.delivery_mode,
            )
        except asyncio.CancelledError:
            raise
        except Exception as err:
            result_message = await self.serialize_message(
                payload=err,
                message_type=RPCMessageType.ERROR,
                correlation_id=message.correlation_id,
                delivery_mode=message.delivery_mode,
            )

        try:
            await self.channel.default_exchange.publish(
                result_message,
                message.reply_to,
                mandatory=False,
            )
        except Exception:
            log.exception("Не удалось отправить ответ %r", result_message)
            await message.reject(requeue=False)
            return

        if message_type == RPCMessageType.ERROR.value:
            await message.ack()
            return

        await message.ack()

    @staticmethod
    def _serialize_exception(err: Exception) -> Dict[str, Any]:
        """
            Внутренний метод сериализации ошибки.

            Arguments:
                - err: Вызванная ошибка.

            Returning:
                Сериализованная ошибка (объект).
        """
        return {
            "__exception__": True,
            "error": {
                "type": str(err.__class__.__name__),
                "exc": (
                    str(getattr(err, "origin_exc")) if getattr(err, "origin_exc", None) else None
                ),
                "traceback": (
                    str(getattr(err, "traceback")) if getattr(err, "traceback", None) else None
                ),
                "args": (str(getattr(err, "args")) if getattr(err, "args", None) else None),
            },
        }


class BaseRPC(object):
    """ Класс базового RPC. """
    AMQP_CLASS: Type[BaseAMQP] = BaseAMQP
    RPC_IMPL: Type[RPC] = MsgPackRPC

    def __init__(
        self,
        dsn: str,
        exchange_name: Optional[str] = None,
        is_durable: bool = True,
        loop: Optional[AbstractEventLoop] = None,
    ) -> None:
        self._loop = loop or get_event_loop()
        self._exchange_name = exchange_name
        self._amqp = self.AMQP_CLASS(
            dsn=dsn,
            is_durable=is_durable,
        )

        self._rpc: Optional[RPC] = None

    @property
    def amqp(self) -> BaseAMQP:
        """ Свойство amqp RPC. """
        return self._amqp

    @shield
    async def initialize(self) -> None:
        """ Метод инициализации RPC. """
        if self._rpc is not None:
            return

        self.RPC_IMPL.DLX_NAME = self._exchange_name or self.RPC_IMPL.DLX_NAME

        self._rpc = await self.RPC_IMPL.create(
            channel=await self.amqp.channel(),
            durable=self.amqp.is_durable,
        )

    async def close(self) -> None:
        """ Метод закрытия подключения RPC. """
        if self._rpc is not None:
            await self._rpc.close()
            self._rpc = None

        await self.amqp.close()

    async def __aenter__(self) -> "BaseRPC":
        await self.amqp.__aenter__()  # noqa:  WPS609
        await self.initialize()
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:
        await self.close()
        await self.amqp.__aexit__(exc_type, exc_value, exc_tb)  # noqa:  WPS609


__all__ = [
    "MsgPackRPC",
    "BaseRPC",
]
