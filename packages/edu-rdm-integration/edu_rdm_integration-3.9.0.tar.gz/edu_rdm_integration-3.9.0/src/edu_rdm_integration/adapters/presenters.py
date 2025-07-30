from abc import (
    ABCMeta,
)

from function_tools.presenters import (
    ResultPresenter,
)


class WebEduResultPresenter(ResultPresenter, metaclass=ABCMeta):
    """
    Базовый класс презентеров результатов работы функций продуктов Образования.
    """
