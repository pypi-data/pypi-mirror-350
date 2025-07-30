from abc import (
    ABCMeta,
    abstractmethod,
)
from typing import (
    Union,
)

from redis import (
    Redis,
    ResponseError,
)


def get_redis_version(connection: 'Redis') -> tuple[int, int, int]:
    """Возвращает кортеж с версией сервера Redis."""
    try:
        version = getattr(connection, '__redis_server_version', None)
        if not version:
            version = tuple([int(n) for n in connection.info('server')['redis_version'].split('.')[:3]])
            setattr(connection, '__redis_server_version', version)
    except ResponseError:
        version = (0, 0, 0)

    return version


def as_text(v: Union[bytes, str]) -> str:
    """Конвертирует последовательность байт в строку."""
    if isinstance(v, bytes):
        return v.decode('utf-8')
    elif isinstance(v, str):
        return v
    else:
        raise ValueError('Неизвестный тип %r' % type(v))


class AbstractCache(metaclass=ABCMeta):
    """Абстрактный интерфейс для кеша отправки."""

    @abstractmethod
    def get(self, key, default=None, **kwargs):
        """Возвращает значение из кеша по ключу."""

    @abstractmethod
    def set(self, key, value, timeout=None, **kwargs):
        """Сохраняет значение в кеш по ключу."""

    @abstractmethod
    def lock(self, name, timeout=None, **kwargs):
        """Захватывает блокировку."""
