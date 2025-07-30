from abc import (
    ABCMeta,
)

from function_tools.results import (
    BaseRunnableResult,
)


class WebEduRunnerResult(BaseRunnableResult, metaclass=ABCMeta):
    """
    Базовый класс результатов работы ранеров функций продуктов Образования.
    """


class WebEduFunctionResult(BaseRunnableResult, metaclass=ABCMeta):
    """
    Базовый класс результатов функций продуктов Образования.
    """
