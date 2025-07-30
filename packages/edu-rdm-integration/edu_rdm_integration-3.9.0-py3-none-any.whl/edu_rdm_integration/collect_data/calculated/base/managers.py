from abc import (
    ABCMeta,
)

from edu_rdm_integration.collect_data.base.managers import (
    BaseCollectingDataRunnerManager,
)
from edu_rdm_integration.collect_data.calculated.base.runners import (
    BaseCollectingCalculatedExportedDataRunner,
)


class BaseCollectingCalculatedExportedDataRunnerManager(BaseCollectingDataRunnerManager, metaclass=ABCMeta):
    """
    Менеджер ранеров функций сбора расчетных данных для интеграции с "Региональная витрина данных".
    """

    @classmethod
    def _prepare_runner_class(cls) -> type[BaseCollectingCalculatedExportedDataRunner]:
        """
        Возвращает класс ранера.
        """
        return BaseCollectingCalculatedExportedDataRunner
