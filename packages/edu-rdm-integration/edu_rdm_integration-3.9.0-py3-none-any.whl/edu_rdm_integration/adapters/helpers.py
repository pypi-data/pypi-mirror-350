from abc import (
    ABCMeta,
)

from function_tools.helpers import (
    BaseFunctionHelper,
    BaseRunnerHelper,
)

from edu_rdm_integration.adapters.caches import (
    WebEduFunctionCacheStorage,
    WebEduRunnerCacheStorage,
)


class WebEduRunnerHelper(BaseRunnerHelper, metaclass=ABCMeta):
    """
    Базовый класс помощников ранеров функций продуктов Образования.
    """

    def _prepare_cache_class(self) -> type[WebEduRunnerCacheStorage]:
        """
        Возвращает класс кеша помощника ранера.
        """
        return WebEduRunnerCacheStorage


class WebEduFunctionHelper(BaseFunctionHelper, metaclass=ABCMeta):
    """
    Базовый класс помощников функций продуктов Образования.
    """

    def _prepare_cache_class(self) -> type[WebEduFunctionCacheStorage]:
        """
        Возвращает класс кеша помощника функции.
        """
        return WebEduFunctionCacheStorage
