""" Модуль описания базовых компонентов RPC. """

import abc
import logging
from typing import Any, Optional

from aio_pika import Channel, Connection, connect_robust

from rms_rpc_core.base.rpc_exceptions import MQException
from rms_rpc_core.utils import shield

log = logging.getLogger(__name__)


class BaseMethod(abc.ABC):
    """ Класс абстрактного базового метода RPC. """
    NAME = __name__

    @abc.abstractmethod
    async def handle(cls, *args, **kwargs) -> Any:  # noqa: N805
        """ Абстрактный метод обработки обращения к методу. """
        raise NotImplementedError("Обработчик не реализован")

    @classmethod
    async def setup(cls) -> None:  # noqa: B027
        """ Абстрактный метод настройки обработчика (метода) RPC. """
        pass  # noqa: WPS420

    @classmethod
    async def cleanup(cls) -> None:  # noqa: B027
        """ Абстрактный метод очистки ресурсов обработчика (метода) RPC. """
        pass  # Delete all opened resources  # noqa: WPS420


class BaseAMQP:
    """ Класс базового коннектора AMQP. """
    DEFAULT_IS_DURABLE: bool = True

    def __init__(
        self,
        dsn: str,
        is_durable: Optional[bool] = None,
    ):
        self._dsn: str = dsn
        self._is_durable: bool = is_durable or self.DEFAULT_IS_DURABLE

        self._connection: Optional[Connection] = None
        self._channel: Optional[Channel] = None

    @property
    def is_durable(self) -> bool:
        """ Настройка длительного подключения """
        return self._is_durable

    async def __aenter__(self) -> "BaseAMQP":
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:
        await self.close()

    @shield
    async def connection(self) -> Connection:
        """
            Метод инициализации подключения AMQP.

            Returning:
                Созданное подключение.
        """
        if self._connection is None or self._connection.is_closed:
            log.debug("Инициализация AMQP подключения")
            self._connection = await connect_robust(self._dsn)  # type: ignore

        return self._connection  # type: ignore

    @shield
    async def channel(self) -> Channel:
        """
            Метод получения канала подключения.
            Если подключение не было создано ранее, то оно будет создано.

            Returning:
                Канал подключения.
        """
        if self._channel is None or self._channel.is_closed:
            log.debug("Инициализация AMQP канала")
            connection = await self.connection()
            self._channel = await connection.channel()

        if self._channel is None:
            raise MQException("Невозможно открыть канал подключения")

        return self._channel

    @shield
    async def close(self) -> None:
        """ Метод закрытия канала и подключения. """
        if self._channel is not None and not self._channel.is_closed:
            log.debug("Закрытие AMQP канала")
            await self._channel.close()

        if self._connection is not None:
            log.debug("Закрытие AMQP подключения")
            await self._connection.close()


__all__ = [
    "BaseMethod",
    "BaseAMQP",
]
