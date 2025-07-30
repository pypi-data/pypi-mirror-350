""" Модуль реализации RPC клиента. """

import logging
from asyncio import AbstractEventLoop
from typing import Any, Optional

from aio_pika import DeliveryMode

from rms_rpc_core.rpc_abstract import BaseRPC
from rms_rpc_core.base.rpc_exceptions import RPCException
from rms_rpc_core.base.registry import Registry

logger = logging.getLogger(__name__)


class RPCClient(BaseRPC):
    """ Класс реализации RPC клиента. """
    EXPIRATION: Optional[int] = None
    _DELIVERY_MODE = DeliveryMode.NOT_PERSISTENT

    def __init__(
        self,
        dsn: str,
        exchange_name: Optional[str] = None,
        is_durable: bool = True,
        loop: Optional[AbstractEventLoop] = None,
        metrics_collector: Any = None
    ):
        super().__init__(dsn=dsn, exchange_name=exchange_name, is_durable=is_durable, loop=loop)
        self._metric_collector = metrics_collector

        self._initialize_metrics()

    async def call_method(self, name: str, **params) -> Any:  # noqa: WPS120
        """
            Метод вызова RPC метода.

            Arguments:
                - name: Название RPC метода.

            Returning:
                Результат выполнения RPC метода.
        """
        method_resource = self._call_method_
        # Если установлен коллектор метрик, то собираем метрики.
        if self._metric_collector:
            method_resource = self._with_metric_call

        return await method_resource(name, **params)

    def _initialize_metrics(self):
        """ Метод инициализации метрик RPC. """
        # Set metric hanlders
        if self._metric_collector:
            metrics_name_space = self._metric_collector.namespace
            self._call_time_metric = self._metric_collector.hist(
                name="rpc_query_duration_seconds",
                docs="Time spent in RPC queries",
                labels=["service", "method"],
            )
            self._call_counter = self._metric_collector.counter(
                name=f"{metrics_name_space}_rpc_task_count",
                docs="RPC task counter",
                labels=["service", "method"],
            )
            # Tasks with errors
            self._shild_metric = self._metric_collector.counter(
                name=f"{metrics_name_space}_rpc_task_error_count",
                docs="RPC error task counter",
                labels=["service", "method"],
            )

    async def _call_method_(self, name: str, **params) -> Any:  # noqa: WPS120
        """
            Внутренний метод вызова RPC метода.

            Arguments:
                - name: Название RPC метода.

            Returning:
                Результат выполнения RPC метода.
        """
        await self.initialize()
        if self._rpc is not None:
            logger.info("Вызов RPC метода: %s", name)
            return await self._rpc.call(
                method_name=name,
                delivery_mode=self._DELIVERY_MODE,
                expiration=self.EXPIRATION,
                kwargs=params
            )

        raise RPCException("RPC не инициализирован")

    async def _with_metric_call(self, name: str, **params) -> Any:  # noqa: WPS120
        """
            Внутренний метод вызова RPC метода со сбором метрик.

            Arguments:
                - name: Название RPC метода.

            Returning:
                Результат выполнения RPC метода.
        """
        if not self._metric_collector:
            raise RPCException("Не задан коллектор метрик")

        self._call_counter.labels(service=Registry.service_name(name), method=name).inc()

        with self._shild_metric.labels(
            service=Registry.service_name(name),
            method=name,
        ).count_exceptions():
            with self._call_time_metric.labels(
                service=Registry.service_name(name),
                method=name,
            ).time():
                return await self._call_method_(name, **params)
