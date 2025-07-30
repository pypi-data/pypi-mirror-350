from abc import (
    ABCMeta,
)

from educommon import (
    logger,
)
from function_tools.runners import (
    BaseRunner,
    GlobalHelperRunner,
)

from edu_rdm_integration.adapters.helpers import (
    WebEduRunnerHelper,
)
from edu_rdm_integration.adapters.results import (
    WebEduRunnerResult,
)
from edu_rdm_integration.adapters.validators import (
    WebEduRunnerValidator,
)
from edu_rdm_integration.consts import (
    LOGS_DELIMITER,
)


class WebEduRunner(BaseRunner, metaclass=ABCMeta):
    """
    Базовый класс ранеров функций продуктов Образования.
    """

    def _prepare_helper_class(self) -> type[WebEduRunnerHelper]:
        """
        Возвращает класс помощника ранера функции.
        """
        return WebEduRunnerHelper

    def _prepare_validator_class(self) -> type[WebEduRunnerValidator]:
        """
        Возвращает класс валидатора ранера функции.
        """
        return WebEduRunnerValidator

    def _prepare_result_class(self) -> type[WebEduRunnerResult]:
        """
        Возвращает класс результата ранера функции.
        """
        return WebEduRunnerResult

    def _prepare_runnable_before_enqueue(self, runnable, *args, **kwargs):
        """
        Подготовка запускаемого объекта к работе перед помещением в очередь.
        """
        super()._prepare_runnable_before_enqueue(runnable, *args, **kwargs)

        logger.info(f'{LOGS_DELIMITER * 2}enqueue {runnable.__class__.__name__}..')


class WebEduGlobalHelperRunner(GlobalHelperRunner, metaclass=ABCMeta):
    """
    Базовый класс для создания ранеров выполнения запускаемых объектов с
    глобальным помощником продуктов Образования.
    """

    def _prepare_helper_class(self) -> type[WebEduRunnerHelper]:
        """
        Возвращает класс помощника ранера функции.
        """
        return WebEduRunnerHelper

    def _prepare_validator_class(self) -> type[WebEduRunnerValidator]:
        """
        Возвращает класс валидатора ранера функции.
        """
        return WebEduRunnerValidator

    def _prepare_result_class(self) -> type[WebEduRunnerResult]:
        """
        Возвращает класс результата ранера функции.
        """
        return WebEduRunnerResult
