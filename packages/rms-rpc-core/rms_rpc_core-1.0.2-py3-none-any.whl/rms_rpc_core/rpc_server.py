""" Модуль сервера RPC. """

import logging
from typing import Set, Type

from rms_rpc_core.rpc_abstract import BaseRPC
from rms_rpc_core.base.rpc_exceptions import RPCException
from rms_rpc_core.base.registry import Registry
from rms_rpc_core.utils import get_full_function_path, shield
from rms_rpc_core.rpc_method import BaseRPCMethod

log = logging.getLogger(__name__)


class RPCServer(BaseRPC):   # noqa:  WPS609
    """ Класс сервера RPC. """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._registries: Set[Registry] = set()
        self._is_locked: bool = False

    def add_registry(self, registry: Registry) -> None:
        """ Метод добавления """
        if self._is_locked:
            raise RPCException("ะกan not add the registry when the server is running.")

        self._registries.add(registry)

    @shield
    async def initialize(self):
        self._is_locked = True
        await super().initialize()

        for registry in self._registries:
            for name, method in registry:  # type: ignore
                await self._register_method(name, method)  # noqa: WPS476

    @shield
    async def close(self) -> None:
        self._is_locked = False
        for registry in self._registries:
            for _, method in registry:   # type: ignore
                await self._unregister_method(method)  # noqa: WPS476
        await super().close()

    async def _register_method(self, name: str, method: Type[BaseRPCMethod]) -> None:
        await method.setup()
        if self._rpc is not None:
            await self._rpc.register(
                method_name=name,
                func=method.call,
                durable=self.amqp.is_durable
            )
            log.debug("RPC method registered :: %s -> %s", name, get_full_function_path(method))

    async def _unregister_method(self, method: Type[BaseRPCMethod]) -> None:
        await method.cleanup()
        if self._rpc is not None:
            await self._rpc.unregister(method.call)
            log.debug("RPC method unregistered :: %s", get_full_function_path(method))
