""" Модуль для работы с реестром RPC методов. """

from typing import Dict, Iterable, List, Optional, Tuple, Type  # noqa: F401

from rms_rpc_core.base.rpc_base import BaseMethod
from rms_rpc_core.utils import clear_str


class Registry(object):  # noqa: WPS338
    """ Класс реестра RPC методов. """
    METHOD_NAME_FORMAT = "{service_name}__{method_name}"

    def __init__(  # noqa: WPS234
        self,
        service_name: Optional[str] = None,
        methods: Optional[List[Type[BaseMethod]]] = None
    ) -> None:
        self._service_name = clear_str(service_name)
        self._registry: Dict[str, Type[BaseMethod]] = {}

        if methods:
            for method in methods:
                self.add(method)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {self._service_name}>"  # noqa: WPS237

    def __hash__(self) -> int:
        return hash(self.__repr__())

    def __iter__(self) -> Iterable[Tuple[str, Type[BaseMethod]]]:   # noqa: WPS234
        for name, func in self._registry.items():  # noqa: WPS526
            yield name, func

    def add(self, handler: Type[BaseMethod], name: Optional[str] = None) -> None:
        """
            Метод добавления нового метода в реестр.

            Arguments:
                - handler: Обработчик (метод) RPC;
                - name: Название метода.
        """
        self._registry[self._make_method_name(name or handler.NAME)] = handler

    def _make_method_name(self, name: str) -> str:
        """
            Метод создания названия метода RPC.

            Arguments:
                - name: Название метода.

            Returning:
                Отформатированное название метода.
        """
        if self._service_name is None:
            return name
        return self.METHOD_NAME_FORMAT.format(
            service_name=self._service_name,
            method_name=name,
        )

    @classmethod
    def service_name(cls, fnk: str) -> Optional[str]:
        """
            Метод получения названия сервиса.

            Arguments:
                - fnk: Название функциональности.

            Returning:
                Название сервиса.
        """
        if "__" not in fnk:
            return None
        return fnk.split("__")[0]
