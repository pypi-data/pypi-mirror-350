from datetime import (
    date,
    datetime,
    time,
)
from typing import (
    TYPE_CHECKING,
)

import uploader_client
from django.core.cache import (
    DEFAULT_CACHE_ALIAS,
    caches,
)
from django.core.management.base import (
    BaseCommand,
)
from uploader_client.adapters import (
    UploaderAdapter,
)
from uploader_client.contrib.rdm.interfaces.configurations import (
    RegionalDataMartUploaderConfig,
)

from edu_rdm_integration.collect_data.collect import (
    BaseCollectModelsData,
)
from edu_rdm_integration.consts import (
    DATETIME_FORMAT,
)
from edu_rdm_integration.export_data.export import (
    BaseExportEntitiesData,
)
from edu_rdm_integration.models import (
    RegionalDataMartEntityEnum,
    RegionalDataMartModelEnum,
)


if TYPE_CHECKING:
    from django.core.management.base import (
        CommandParser,
    )
    from uploader_client.interfaces import (
        OpenAPIRequest,
    )


class BaseCollectModelDataCommand(BaseCommand):
    """
    Базовая команда для выполнения сбора данных моделей РВД.
    """

    def add_arguments(self, parser: 'CommandParser'):
        """
        Добавление параметров.
        """
        models = ', '.join([
            f'{key} - {value.title}'
            for key, value in RegionalDataMartModelEnum.get_enum_data().items()
        ])
        models_help_text = (
            f'Значением параметра является перечисление моделей РВД, для которых должен быть произведен сбор данных. '
            f'Перечисление моделей:\n{models}. Если модели не указываются, то сбор данных производится для всех '
            f'моделей. Модели перечисляются через запятую без пробелов.'
        )
        parser.add_argument(
            '--models',
            action='store',
            dest='models',
            type=lambda e: e.split(','),
            help=models_help_text,
        )

        parser.add_argument(
            '--logs_period_started_at',
            action='store',
            dest='logs_period_started_at',
            type=lambda started_at: datetime.strptime(started_at, DATETIME_FORMAT),
            default=datetime.combine(date.today(), time.min),
            help=(
                'Дата и время начала периода обрабатываемых логов. Значение предоставляется в формате '
                '"дд.мм.гггг чч:мм:сс". По умолчанию, сегодняшний день, время 00:00:00.'
            ),
        )

        parser.add_argument(
            '--logs_period_ended_at',
            action='store',
            dest='logs_period_ended_at',
            type=lambda ended_at: datetime.strptime(ended_at, DATETIME_FORMAT),
            default=datetime.combine(date.today(), time.max),
            help=(
                'Дата и время конца периода обрабатываемых логов. Значение предоставляется в формате '
                '"дд.мм.гггг чч:мм:сс". По умолчанию, сегодняшний день, время 23:59:59.'
            ),
        )

    def _prepare_collect_models_data_class(self, *args, **kwargs) -> BaseCollectModelsData:
        """Возвращает объект класса сбора данных моделей РВД."""
        raise NotImplementedError

    def handle(self, *args, **kwargs):
        """
        Выполнение действий команды.
        """
        collect_models_data = self._prepare_collect_models_data_class(*args, **kwargs)
        collect_models_data.collect()


class BaseExportEntityDataCommand(BaseCommand):
    """
    Базовая команда для выполнения выгрузки данных сущностей РВД за указанный период.
    """

    def add_arguments(self, parser: 'CommandParser'):
        """
        Добавление параметров.
        """
        entities = ', '.join([
            f'{key} - {value.title}'
            for key, value in RegionalDataMartEntityEnum.get_enum_data().items()
        ])
        entities_help_text = (
            f'Значением параметра является перечисление сущностей РВД, для которых должена быть произведена выгрузка '
            f'данных. Перечисление сущностей:\n{entities}. Если сущности не указываются, то выгрузка данных '
            f'производится для всех сущностей. Сущности перечисляются через запятую без пробелов.'
        )
        parser.add_argument(
            '--entities',
            action='store',
            dest='entities',
            type=lambda e: e.split(','),
            help=entities_help_text,
        )

        parser.add_argument(
            '--period_started_at',
            action='store',
            dest='period_started_at',
            type=lambda started_at: datetime.strptime(started_at, DATETIME_FORMAT),
            default=datetime.combine(date.today(), time.min),
            help=(
                'Дата и время начала периода сбора записей моделей РВД. Значение предоставляется в формате '
                '"дд.мм.гггг чч:мм:сс". По умолчанию, сегодняшний день, время 00:00:00.'
            ),
        )

        parser.add_argument(
            '--period_ended_at',
            action='store',
            dest='period_ended_at',
            type=(
                lambda ended_at: datetime.strptime(ended_at, DATETIME_FORMAT).replace(microsecond=time.max.microsecond)
            ),
            default=datetime.combine(date.today(), time.max),
            help=(
                'Дата и время конца периода сбора записей моделей РВД. Значение предоставляется в формате '
                '"дд.мм.гггг чч:мм:сс". По умолчанию, сегодняшний день, время 23:59:59.'
            ),
        )
        parser.add_argument(
            '--task_id',
            action='store',
            dest='task_id',
            type=str,
            default=None,
            help='task_id для поиска асинхронной задачи',
        )
        parser.add_argument(
            '--no-update-modified',
            dest='update_modified',
            action='store_false',
            default=True,
            help='Не обновлять поле modified моделей',
        )

    def _prepare_export_entities_data_class(self, *args, **kwargs) -> BaseExportEntitiesData:
        """Возвращает объект класса экспорта данных сущностей РВД."""
        raise NotImplementedError

    def handle(self, *args, **kwargs):
        """
        Выполнение действий команды.
        """
        export_entities_data = self._prepare_export_entities_data_class(*args, **kwargs)
        export_entities_data.export()


class BaseCollectModelsDataByGeneratingLogsCommand(BaseCollectModelDataCommand):
    """
    Команда сбора данных моделей РВД на основе существующих в БД данных моделей ЭШ.

    Можно регулировать, для каких моделей должен быть произведен сбор данных, и период, за который должны
    быть собраны логи. Логи формируются в процессе выполнения команды при помощи генератора логов LogGenerator для
    указанной модели.
    """

    # flake8: noqa: A003
    help = 'Команда сбора данных моделей РВД на основе существующих в БД данных моделей продукта'

    def add_arguments(self, parser: 'CommandParser'):
        """
        Добавление параметров.
        """
        super().add_arguments(parser=parser)

        parser.add_argument(
            '--institute_ids',
            action='store',
            dest='institute_ids',
            type=lambda v: tuple(map(int, v.split(','))),
            default=(),
            help='Идентификаторы учебных заведений, для которых производится выгрузка.',
        )


class BaseDatamartClientCommand(BaseCommand):
    """Базовая команда для загрузки данных/получение статуса в РВД с использованием uploader_client."""

    TIMEOUT = 300
    REQUEST_RETRIES = 1

    def add_arguments(self, parser):
        """Добавление параметров."""
        parser.add_argument(
            '--url',
            type=str,
            required=True,
            help='url хоста Datamart Studio',
        )
        parser.add_argument(
            '--datamart_mnemonic',
            type=str,
            required=True,
            help='мнемоника Витрины',
        )
        parser.add_argument(
            '--organization_ogrn',
            type=str,
            required=True,
            help='ОГРН организации, в рамках которой развёрнута Витрина',
        )
        parser.add_argument(
            '--installation_name',
            type=str,
            required=True,
            help='имя инсталляции в целевой Витрине',
        )
        parser.add_argument(
            '--installation_id',
            type=int,
            required=True,
            help='идентификатор инсталляции (присутствует в её названии)',
        )
        parser.add_argument(
            '--username',
            type=str,
            required=True,
            help='имя пользователя IAM',
        )
        parser.add_argument(
            '--password',
            type=str,
            required=True,
            help='пароль пользователя IAM',
        )

    def _configure_agent_client(
        self,
        url,
        datamart_mnemonic,
        organization_ogrn,
        installation_name,
        installation_id,
        username,
        password,
    ):
        """Конфигурирование клиента загрузчика данных в Витрину."""
        uploader_client.set_config(
            RegionalDataMartUploaderConfig(
                interface='uploader_client.contrib.rdm.interfaces.rest.ProxyAPIInterface',
                cache=caches[DEFAULT_CACHE_ALIAS],
                url=url,
                datamart_name=datamart_mnemonic,
                organization_ogrn=organization_ogrn,
                installation_name=installation_name,
                installation_id=installation_id,
                username=username,
                password=password,
                timeout=self.TIMEOUT,
                request_retries=self.REQUEST_RETRIES,
            )
        )

    def _get_request(self, **options) -> 'OpenAPIRequest':
        """Возвращает запрос для отправки в РВД."""
        raise NotImplementedError

    def handle(self, *args, **options):
        """Выполнение действий команды."""
        self._configure_agent_client(
            url=options['url'],
            datamart_mnemonic=options['datamart_mnemonic'],
            organization_ogrn=options['organization_ogrn'],
            installation_name=options['installation_name'],
            installation_id=options['installation_id'],
            username=options['username'],
            password=options['password'],
        )

        request = self._get_request(**options)

        result = UploaderAdapter().send(request)

        if result.error:
            self.stdout.write(self.style.ERROR(f'ERROR:\n'))
            self.stdout.write(
                f'{result.error}\n'
                f'REQUEST:\n"{result.log.request}"\n\n'
                f'RESPONSE:\n"{result.log.response}"\n'
            )
        else:
            self.stdout.write(self.style.SUCCESS(f'SUCCESS:\n'))
            self.stdout.write(
                f'Response with {result.response.status_code} code and content:\n{result.response.text}\n'
            )
