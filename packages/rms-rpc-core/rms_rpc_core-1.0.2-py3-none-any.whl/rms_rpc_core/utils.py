""" Модуль вспомогательных фукнций для библиотеки RPC. """

from asyncio import shield as _shield
from functools import wraps
from typing import Optional, Union
from uuid import UUID


def clear_str(string: Optional[str]) -> Optional[str]:
    """
        Метод очистки строки от лишних пробелов.

        Arguments:
            - string: Входная строка, которую нужно очистить.

        Returning:
            Очищенная строка.
    """
    return None if string is None or not string.strip() else string.strip()


def shield(func):
    """ Декаратор защиты выполнения асинхронных функций. """
    async def awaiter(future):
        return await future

    @wraps(func)
    def wrap(*args, **kwargs):
        return wraps(func)(awaiter)(_shield(func(*args, **kwargs)))  # noqa: WPS221

    return wrap


def get_full_function_path(func) -> str:
    """
        Метод получения полного пути функции.

        Arguments:
            - func: Функция, для которой необходимо получить полный путь.

        Returning:
            Полный путь функции.
    """
    return f"{func.__module__}.{func.__name__}"  # noqa: WPS237


def uuid_to_str(u_string: Optional[Union[UUID, str]]) -> Optional[str]:
    """
        Метод приведения uuid к строке.

        Arguments:
            - u_string: Переменная, содержащая uuid.

        Returning:
            uuid в строковом представлении.
    """
    return None if u_string is None else str(u_string)


def get_full_class_path(instance: object) -> str:
    """
        Метод получения полного пути класса.

        Arguments:
            - instance: Экземпляр класса, для которого необходимо получить полный путь.

        Returning:
            Полный путь класса.
    """
    return f"{instance.__class__.__module__}.{instance.__class__.__name__}"  # noqa: WPS237
