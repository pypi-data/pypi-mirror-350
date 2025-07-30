import inspect
import sys
from importlib import (
    import_module,
)
from operator import (
    attrgetter,
)
from typing import (
    Iterable,
)

from django.apps import (
    apps,
)
from django.db import (
    models,
)

from educommon.integration_entities.entities import (
    BaseEntity,
)
from m3_db_utils.mixins import (
    BaseEnumRegisterMixin,
)

from edu_rdm_integration.enum_register.mixins import (
    EntityEnumRegisterMixin,
    ModelEnumRegisterMixin,
)


def register_classes(classes: Iterable[type[BaseEnumRegisterMixin]]) -> None:
    """Вызывает метод регистрации в модель-перечисление
    у переданных классов.

    Args:
        classes: Классы, поддерживающие интерфейс регистрации.
    """
    classes = sorted(classes, key=attrgetter('order_number'))

    for enum_class in classes:
        enum_class.register()


def is_register_model(model: models.Model) -> bool:
    """Проверяет, является ли класс регистрируемой моделью."""
    return issubclass(model, ModelEnumRegisterMixin)


def is_register_entity(class_) -> bool:
    """Проверяет, является ли класс регистрируемой сущностью."""
    return (
        inspect.isclass(class_) and
        issubclass(class_, BaseEntity) and
        issubclass(class_, EntityEnumRegisterMixin)
    )


def register_models() -> None:
    """Регистрирует модели в RegionalDataMartModelEnum."""
    register_classes([
        m for m in apps.get_models() if is_register_model(m)
    ])


def register_entities(import_path: str) -> None:
    """Находит регистрируемые сущности в модуле по переданному пути и
    регистрирует в RegionalDataMartEntityEnum.

    Args:
        import_path: Путь до пакета, хранящего классы сущностей;
    """
    import_module(import_path)
    entities_module = sys.modules[import_path]

    register_classes([
        c[1] for c in inspect.getmembers(entities_module, is_register_entity)
    ])
