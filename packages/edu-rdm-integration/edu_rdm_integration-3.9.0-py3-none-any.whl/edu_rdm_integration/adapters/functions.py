from abc import (
    ABCMeta,
)

from function_tools.functions import (
    BaseFunction,
    LazySavingPredefinedQueueFunction,
    LazySavingPredefinedQueueGlobalHelperFunction,
)

from edu_rdm_integration.adapters.helpers import (
    WebEduFunctionHelper,
)
from edu_rdm_integration.adapters.results import (
    WebEduFunctionResult,
)
from edu_rdm_integration.adapters.validators import (
    WebEduFunctionValidator,
)


class WebEduFunction(BaseFunction, metaclass=ABCMeta):
    """
    Базовый класс для создания функций продуктов Образования.
    """


class WebEduLazySavingPredefinedQueueFunction(LazySavingPredefinedQueueFunction, metaclass=ABCMeta):
    """
    Базовый класс для создания функций с отложенным сохранением объектов
    моделей с предустановленной очередью продуктов Образования.
    """

    def _prepare_helper_class(self) -> type[WebEduFunctionHelper]:
        """
        Возвращает класс помощника функции.
        """
        return WebEduFunctionHelper

    def _prepare_validator_class(self) -> type[WebEduFunctionValidator]:
        """
        Возвращает класс валидатора функции.
        """
        return WebEduFunctionValidator

    def _prepare_result_class(self) -> type[WebEduFunctionResult]:
        """
        Возвращает класс результата функции.
        """
        return WebEduFunctionResult


class WebEduLazySavingPredefinedQueueGlobalHelperFunction(
    LazySavingPredefinedQueueGlobalHelperFunction,
    metaclass=ABCMeta,
):
    """
    Базовый класс для создания функций с отложенным сохранением,
    предустановленной очередью на сохранение и глобальным помощником продуктов Образования.
    """