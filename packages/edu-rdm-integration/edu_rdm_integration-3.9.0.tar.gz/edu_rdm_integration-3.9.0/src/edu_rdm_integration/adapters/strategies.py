from abc import (
    ABCMeta,
)
from typing import (
    Optional,
)

from function_tools.strategies import (
    FunctionImplementationStrategy,
)

from edu_rdm_integration.adapters.caches import (
    WebEduFunctionCacheStorage,
    WebEduRunnerCacheStorage,
)
from edu_rdm_integration.adapters.errors import (
    WebEduError,
)
from edu_rdm_integration.adapters.functions import (
    WebEduFunction,
    WebEduLazySavingPredefinedQueueFunction,
)
from edu_rdm_integration.adapters.helpers import (
    WebEduFunctionHelper,
    WebEduRunnerHelper,
)
from edu_rdm_integration.adapters.managers import (
    WebEduRunnerManager,
)
from edu_rdm_integration.adapters.presenters import (
    WebEduResultPresenter,
)
from edu_rdm_integration.adapters.results import (
    WebEduFunctionResult,
    WebEduRunnerResult,
)
from edu_rdm_integration.adapters.runners import (
    WebEduRunner,
)
from edu_rdm_integration.adapters.validators import (
    WebEduFunctionValidator,
    WebEduRunnerValidator,
)


class WebEduFunctionImplementationStrategy(FunctionImplementationStrategy, metaclass=ABCMeta):
    """
    Базовый класс стратегии реализации функции продуктов Образования.
    """

    def _prepare_manager_class(self):
        """
        Устанавливает класс менеджера.
        """
        self._manager_class = WebEduRunnerManager

    def _prepare_runner_class(self):
        """
        Устанавливает класс ранера.
        """
        self._runner_class = WebEduRunner

    def _prepare_function_class(self):
        """
        Устанавливает класс Функции.
        """
        self._function_class = WebEduFunction

    def _prepare_runner_helper_class(self):
        """
        Устанавливает класс помощника ранера.
        """
        self._runner_helper_class = WebEduRunnerHelper

    def _prepare_function_helper_class(self):
        """
        Устанавливает класс помощника функции.
        """
        self._function_helper_class = WebEduFunctionHelper

    def _prepare_runner_validator_class(self):
        """
        Устанавливает класс валидатора ранера.
        """
        self._runner_validator_class = WebEduRunnerValidator

    def _prepare_function_validator_class(self):
        """
        Устанавливает класс валидатора Функции.
        """
        self._function_validator_class = WebEduFunctionValidator

    def _prepare_runner_cache_storage_class(self):
        """
        Устанавливает класс хранилища кешей ранера.
        """
        self._runner_cache_storage_class = WebEduRunnerCacheStorage

    def _prepare_function_cache_storage_class(self):
        """
        Устанавливает класс хранилища кешей Функции.
        """
        self._function_cache_storage_class = WebEduFunctionCacheStorage

    def _prepare_error_class(self):
        """
        Устанавливает класс ошибки.
        """
        self._error_class = WebEduError

    def _prepare_runner_result_class(self):
        """
        Устанавливает класс результата.
        """
        self._runner_result_class = WebEduRunnerResult

    def _prepare_function_result_class(self):
        """
        Устанавливает класс результата.
        """
        self._function_result_class = WebEduFunctionResult

    def _prepare_result_presenter_class(self):
        """
        Устанавливает класс презентера результата.
        """
        self._result_presenter_class = WebEduResultPresenter


class WebEduSyncBaseRunnerLazySavingPredefinedQueueFunctionImplementationStrategy(
    WebEduFunctionImplementationStrategy,
    metaclass=ABCMeta
):
    """
    Стратегия создания функции с отложенным сохранением и предустановленной очередью объектов на сохранение продуктов Образования.
    """

    def _prepare_key(self) -> str:
        """
        Возвращает уникальный идентификатор стратегии создания функции.
        """
        return 'WEB_EDU_SYNC_LAZY_SAVING_FUNCTION'

    def _prepare_title(self) -> str:
        """
        Возвращает название стратегии создания функции.
        """
        return (
            'Стратегия создания функции с отложенным сохранением и предустановленной очередью объектов на сохранение '
            'продуктов Образования. Сохранение производится после удачной работы функции'
        )

    @classmethod
    def _prepare_function_template_name(cls) -> Optional[str]:
        """
        Формирование названия шаблона создания функции.
        """
        return 'function_sync_template'

    def _prepare_function_class(self):
        """
        Устанавливает класс Функции.
        """
        self._function_class = WebEduLazySavingPredefinedQueueFunction
