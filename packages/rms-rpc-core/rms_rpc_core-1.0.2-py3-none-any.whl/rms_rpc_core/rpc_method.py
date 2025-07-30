""" Модуль описания базового метода RPC. """

import logging
import traceback
from abc import ABC
from typing import Any

from rms_rpc_core.base.rpc_base import BaseMethod
from rms_rpc_core.base.rpc_exceptions import RPCRuntimeError
from rms_rpc_core.utils import get_full_class_path

log = logging.getLogger(__name__)


class BaseRPCMethod(BaseMethod, ABC):  # noqa: B024
    """ Класс-основа для метода RPC. """
    @classmethod
    async def call(cls, **kwargs) -> Any:
        """ Метод обработчик вызова RPC-метода. """
        try:
            log.info('Remote call method: %s', cls.NAME)
            return await cls.handle(**kwargs)
        except Exception as exc:
            log.warning('Error during method `%s` executing', cls.NAME, exc_info=True)
            raise RPCRuntimeError(
                origin_exc=get_full_class_path(exc),
                traceback=traceback.format_exc(),
            )
