from abc import (
    ABCMeta,
)

from function_tools.validators import (
    BaseValidator,
)


class WebEduRunnerValidator(BaseValidator, metaclass=ABCMeta):
    """
    Базовый класс валидаторов ранеров функций продуктов Образования.
    """


class WebEduFunctionValidator(BaseValidator, metaclass=ABCMeta):
    """
    Базовый класс валидаторов функций продуктов Образования.
    """
