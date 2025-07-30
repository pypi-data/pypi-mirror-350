from abc import (
    ABCMeta,
)

from function_tools.errors import (
    BaseError,
)


class WebEduError(BaseError, metaclass=ABCMeta):
    """
    Базовый класс ошибок функций продуктов Образования.
    """
