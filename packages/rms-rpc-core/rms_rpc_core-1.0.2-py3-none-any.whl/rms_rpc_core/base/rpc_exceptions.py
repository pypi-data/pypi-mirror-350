""" Модуль ошибок для библиотеки RPC. """

from typing import Any, Dict, Optional, Tuple


class MQException(Exception):
    """ Класс ошибки RPC. """
    pass   # noqa: WPS604, WPS420


class AsyncTaskError(MQException):
    """ Класс ошибки асинхронных задач. """
    pass   # noqa: WPS604, WPS420


class AsyncTaskRetry(AsyncTaskError):
    """ Класс ошибки повторения асинхронных задач. """
    pass   # noqa: WPS604, WPS420


class RPCException(MQException):
    """ Класс базовой ошибки RPC. """
    pass   # noqa: WPS604, WPS420


class RPCRuntimeError(RPCException):
    """ Класс ошибки RPC в ходе выполнения. """
    def __init__(
        self,
        origin_exc: Optional[str] = None,
        traceback: Optional[str] = None,
        args: Optional[Tuple[str]] = None
    ) -> None:
        self._origin_exc = origin_exc
        self._traceback = traceback
        self.args = args or tuple()

    @property
    def origin_exc(self) -> str:
        """ Свойство получения оригинальной ошибки. """
        return self._origin_exc or ""

    @property
    def traceback(self) -> str:
        """ Свойство получения стека ошибки. """
        return self._traceback or ""

    def to_dict(self) -> Dict[str, Any]:
        """
            Метод приведения ошибки к объекту.

            Returning:
                Объект с данными ошибки формата:
                    {
                        exc: <Описание ошибки>,
                        traceback: <Стектрейс ошибки>,
                        args: <Аргументы ошибки>
                    }
        """
        return {
            "exc": self.origin_exc,
            "traceback": self.traceback,
            "args": self.args,
        }
