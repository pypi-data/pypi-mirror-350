from abc import (
    ABCMeta,
)

from edu_rdm_integration.collect_data.base.managers import (
    BaseCollectingDataRunnerManager,
)
from edu_rdm_integration.collect_data.non_calculated.base.runners import (
    BaseCollectingExportedDataRunner,
)


class BaseCollectingExportedDataRunnerManager(BaseCollectingDataRunnerManager, metaclass=ABCMeta):
    """
    Менеджер ранеров функций сбора данных для интеграции с "Региональная витрина данных".
    """

    @classmethod
    def _prepare_runner_class(cls) -> type[BaseCollectingExportedDataRunner]:
        """
        Возвращает класс ранера.
        """
        return BaseCollectingExportedDataRunner
