from typing import (
    Any,
    NamedTuple,
    Optional,
)

from django.db import (
    models,
)

from m3_db_utils.mixins import (
    BaseEnumRegisterMixin,
)
from m3_db_utils.models import (
    ModelEnumValue,
)
from m3_django_compat import (
    classproperty,
)

from edu_rdm_integration.models import (
    RegionalDataMartEntityEnum,
    RegionalDataMartModelEnum,
)
from edu_rdm_integration.typing import (
    MODEL_TYPE_VAR,
)
from edu_rdm_integration.utils import (
    camel_to_underscore,
)


class EntityEnumRegisterMixin(BaseEnumRegisterMixin):
    """Миксин, для регистрации сущности в RegionalDataMartEntityEnum."""

    enum = RegionalDataMartEntityEnum
    """Модель-перечисление в которую регистрируется сущность."""

    main_model_enum: ModelEnumValue
    """Значение RegionalDataMartModelEnum,
    основной модели РВД для формирования сущности."""

    additional_model_enums: tuple[ModelEnumValue] = ()
    """Перечень дополнительных значений RegionalDataMartModelEnum,
    которые участвуют в формировании записей сущностей"""

    title: str
    """Расшифровка сущности модели-перечисления"""

    @classproperty
    def key(cls) -> str:
        return camel_to_underscore(cls.__name__.rsplit('Entity', 1)[0], upper=True)

    @classmethod
    def get_register_params(cls) -> dict[str, Any]:
        register_params = super().get_register_params()

        register_params['main_model_enum'] = getattr(cls, 'main_model_enum', None) or cls.get_main_model_enum()
        register_params['entity'] = cls
        register_params['additional_model_enums'] = cls.additional_model_enums or cls.get_additional_model_enums()

        return register_params

    # TODO EDUSCHL-20938 Удалить в рамках задачи
    @classmethod
    def get_main_model_enum(cls) -> Optional[ModelEnumValue]:
        """Возвращает значение модели перечисление основной модели сущности.

        В классе определяется поле main_model_enum или данный метод.

        !!! Временное решение. Будет удалено в рамках EDUSCHL-20938.
        """

    # TODO EDUSCHL-20938 Удалить в рамках задачи
    @classmethod
    def get_additional_model_enums(cls) -> Optional[tuple[ModelEnumValue]]:
        """Возвращает кортеж значений модели-перечисления основной модели сущности.

        В классе определяется поле additional_model_enums или данный метод.

        !!! Временное решение. Будет удалено в рамках EDUSCHL-20938.
        """


class ModelEnumRegisterMixin(BaseEnumRegisterMixin):
    """Миксин, для регистрации модели в RegionalDataMartModelEnum."""

    enum = RegionalDataMartModelEnum
    """Модель-перечисление в которую регистрируется модель."""

    creating_trigger_models: tuple[models.Model, ...] = ()
    """Перечень моделей по которым генерируются логи."""

    loggable_models: tuple[models.Model, ...] = ()
    """Перечень моделей по которым собираются логи."""

    @classproperty
    def key(cls) -> str:
        return camel_to_underscore(cls.__name__).upper()

    @classproperty
    def title(cls):
        return cls._meta.verbose_name

    @classmethod
    def get_register_params(cls) -> dict[str, Any]:
        register_params = super().get_register_params()
        register_params['model'] = cls
        register_params['creating_trigger_models'] = cls.creating_trigger_models
        register_params['loggable_models'] = cls.loggable_models

        return register_params


class FromNamedTupleMixin:
    """Миксин получения экземпляра модели из получаемого кэша значений."""

    @classmethod
    def from_namedtuple(cls: type[MODEL_TYPE_VAR], namedtuple: NamedTuple) -> MODEL_TYPE_VAR:
        """Создает экземпляр класса из NamedTuple."""
        return cls(
            **{
                field: getattr(namedtuple, field)
                for field in [f.column for f in cls._meta.get_fields()]
            }
        )
