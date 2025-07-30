from edu_rdm_integration.collect_data.base.helpers import (
    BaseCollectingDataFunctionHelper,
    BaseCollectingDataRunnerHelper,
)
from edu_rdm_integration.collect_data.calculated.base.caches import (
    BaseCollectingCalculatedExportedDataFunctionCacheStorage,
    BaseCollectingCalculatedExportedDataRunnerCacheStorage,
)


class BaseCollectingCalculatedExportedDataRunnerHelper(BaseCollectingDataRunnerHelper):
    """
    Базовый класс помощников ранеров функций сбора расчетных данных для интеграции с "Региональная витрина данных".
    """

    def _prepare_cache_class(self) -> type[BaseCollectingCalculatedExportedDataRunnerCacheStorage]:
        """
        Возвращает класс кеша помощника ранера.
        """
        return BaseCollectingCalculatedExportedDataRunnerCacheStorage


class BaseCollectingCalculatedExportedDataFunctionHelper(BaseCollectingDataFunctionHelper):
    """
    Базовый класс помощников функций сбора расчетных данных для интеграции с "Региональная витрина данных".
    """

    def _prepare_cache_class(self) -> type[BaseCollectingCalculatedExportedDataFunctionCacheStorage]:
        """
        Возвращает класс кеша помощника функции.
        """
        return BaseCollectingCalculatedExportedDataFunctionCacheStorage
