from typing import (
    Optional,
)

from m3.db import (
    BaseEnumerate,
)

from edu_rdm_integration.consts import (
    FAST_TRANSFER_TASK_QUEUE_NAME,
    LONG_TRANSFER_TASK_QUEUE_NAME,
    TASK_QUEUE_NAME,
)


class ValueCodeEnumerate(BaseEnumerate):
    """
    Добавляет к перечислению метод возвращающий наименование кода по константе.
    """

    _codes_cache = None
    _values_cache = None

    @classmethod
    def get_code_by_constant(cls, constant: int, delimiter: Optional[str] = None) -> Optional[str]:
        """Возвращает наименование кода по значению константы."""
        if cls._codes_cache is None:
            cls._codes_cache = {
                v: k.lower().replace('_', delimiter) if delimiter else k.lower()
                for k, v in cls.__dict__.items()
                if isinstance(v, int) and v in cls.values
            }

        return cls._codes_cache.get(constant)

    @classmethod
    def get_value_by_description(cls, name: str, default: Optional[int] = None) -> Optional[int]:
        """Возвращает значение по описанию этого значения."""
        if cls._values_cache is None:
            cls._values_cache = {v: k for k, v in cls.values.items() if isinstance(v, str)}

        return cls._values_cache.get(name, default)


class EntityStatusEnum(ValueCodeEnumerate):
    """Статус сущности."""

    ACTIVE = 1
    CANCELLED = 2
    ENTERED_IN_ERROR = 3

    values = {
        ACTIVE: 'Действует',
        CANCELLED: 'Отменено',
        ENTERED_IN_ERROR: 'Внесено по ошибке',
    }


class FileUploadStatusEnum(BaseEnumerate):
    """Действие по отслеживаемым данным."""

    IN_PROGRESS = 1
    FINISHED = 2
    ERROR = 3

    values = {
        IN_PROGRESS: 'В процессе загрузки в витрину',
        FINISHED: 'Загрузка в витрину закончена',
        ERROR: 'Ошибка загрузки в витрину',
    }


class AddressUse(ValueCodeEnumerate):
    """Использование адреса."""

    HOME = 1
    WORK = 2
    TEMP = 3
    OLD = 4
    BILLING = 5

    values = {
        HOME: 'Домашний',
        WORK: 'Рабочий',
        TEMP: 'Временный',
        OLD: 'Устаревший',
        BILLING: 'Для счетов',
    }


class AddressType(ValueCodeEnumerate):
    """Тип адреса."""

    POSTAL = 1
    RESIDENCE = 2
    TEMPORARY = 3
    LOCATION = 4
    JURISTICAL = 5

    values = {
        POSTAL: 'Почтовый',
        RESIDENCE: 'Место жительства',
        TEMPORARY: 'Место пребывания',
        LOCATION: 'Местонахождение',
        JURISTICAL: 'Юридический',
    }

    active_types = (POSTAL, LOCATION, JURISTICAL)


class TelecomTypeEnum(ValueCodeEnumerate):
    """Тип контактных данных."""

    PHONE = 1
    FAX = 2
    EMAIL = 3
    PAGER = 4
    URL = 5
    SMS = 6
    OTHER = 7

    values = {
        PHONE: 'Телефон',
        FAX: 'Факс',
        EMAIL: 'Электронная почта',
        PAGER: 'Пейджер',
        URL: 'Ссылка',
        SMS: 'СМС',
        OTHER: 'Иное',
    }


class TelecomUseEnum(ValueCodeEnumerate):
    """Код использования контактных данных."""

    HOME = 1
    WORK = 2
    TEMP = 3
    OLD = 4
    MOBILE = 5

    values = {
        HOME: 'Домашний',
        WORK: 'Рабочий',
        TEMP: 'Временный',
        OLD: 'Устаревший',
        MOBILE: 'Мобильный',
    }


class EntityRetiredStatusEnum(ValueCodeEnumerate):
    """Статус сущности действие которой может быть прекращено."""

    ACTIVE = 1
    RETIRED = 2
    ENTERED_IN_ERROR = 3

    values = {
        ACTIVE: 'Действует',
        RETIRED: 'Прекращена',
        ENTERED_IN_ERROR: 'Создана по ошибке',
    }


class CommandType(BaseEnumerate):
    """Тип команды."""

    AUTO = 1
    MANUAL = 2

    values = {
        AUTO: 'Автоматический',
        MANUAL: 'Ручной',
    }


class EntityLevelQueueTypeEnum(BaseEnumerate):
    """Тип уровня очереди сущности."""

    FAST = 1
    BASE = 2
    LONG = 3

    values = {
        FAST: 'Быстрая',
        BASE: 'Основная',
        LONG: 'Долгая'
    }

    celery_queue_maps = {
        FAST: FAST_TRANSFER_TASK_QUEUE_NAME,
        BASE: TASK_QUEUE_NAME,
        LONG: LONG_TRANSFER_TASK_QUEUE_NAME
    }

    @classmethod
    def get_queue_name(cls, level: int) -> Optional[str]:
        """Возвращает очередь."""
        return cls.celery_queue_maps.get(level)
