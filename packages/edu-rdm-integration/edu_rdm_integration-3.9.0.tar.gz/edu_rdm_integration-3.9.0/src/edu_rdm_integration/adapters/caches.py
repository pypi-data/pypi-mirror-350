from abc import (
    ABCMeta,
)

from function_tools.caches import (
    CacheStorage,
    EntityCache,
    PatchedGlobalCacheStorage,
    PeriodicalEntityCache,
)


class WebEduEntityCache(EntityCache, metaclass=ABCMeta):
    """
    Базовый класс кеша объектов сущности продуктов Образования.
    """


class WebEduPeriodicalEntityCache(PeriodicalEntityCache, metaclass=ABCMeta):
    """
    Базовый класс периодического кеша продуктов Образования.

    Кеш создается для определенной модели с указанием двух дат, на которые
    должны быть собраны кеши актуальных объектов модели.
    """


class WebEduRunnerCacheStorage(CacheStorage, metaclass=ABCMeta):
    """
    Базовый класс кешей помощников ранеров функций продуктов Образования.
    """


class WebEduFunctionCacheStorage(CacheStorage, metaclass=ABCMeta):
    """
    Базовый класс кешей функций продуктов Образования.
    """


class WebEduFunctionPatchedGlobalCacheStorage(PatchedGlobalCacheStorage, metaclass=ABCMeta):
    """
    Базовый класс кешей функций продуктов Образования с возможностью патчинга кешем глобального хелпера.
    """
