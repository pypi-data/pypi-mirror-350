import logging
import os
from collections import (
    defaultdict,
)
from datetime import (
    date,
    datetime,
    time,
    timedelta,
)
from typing import (
    TYPE_CHECKING,
    Iterable,
    Union,
)

from django.conf import (
    settings,
)
from django.db.models import (
    F,
    Model,
    Value,
)
from django.db.models.base import (
    ModelBase,
)
from django.db.models.functions import (
    Concat,
)
from django.db.transaction import (
    atomic,
)
from django.utils import (
    timezone,
)
from django.utils.datastructures import (
    OrderedSet,
)

from educommon import (
    logger,
)
from educommon.async_task.models import (
    RunningTask,
)
from educommon.utils.date import (
    get_today_max_datetime,
)
from educommon.utils.seqtools import (
    make_chunks,
)
from m3_db_utils.consts import (
    DEFAULT_ORDER_NUMBER,
)
from m3_db_utils.models import (
    ModelEnumValue,
)

from edu_rdm_integration.base import (
    BaseOperationData,
)
from edu_rdm_integration.consts import (
    REGIONAL_DATA_MART_INTEGRATION_EXPORTING_DATA,
)
from edu_rdm_integration.export_data.consts import (
    TOTAL_ATTACHMENTS_SIZE_KEY,
)
from edu_rdm_integration.export_data.export_manager import (
    ExportQueueSender,
    WorkerSender,
)
from edu_rdm_integration.export_data.queue import (
    Queue,
)
from edu_rdm_integration.helpers import (
    get_exporting_managers_max_period_ended_dates,
)
from edu_rdm_integration.models import (
    ExportingDataStage,
    ExportingDataSubStageStatus,
    RegionalDataMartEntityEnum,
)
from edu_rdm_integration.redis_cache import (
    AbstractCache,
)
from edu_rdm_integration.signals import (
    manager_created,
)
from edu_rdm_integration.storages import (
    RegionalDataMartEntityStorage,
)


if TYPE_CHECKING:
    from function_tools.managers import (
        RunnerManager,
    )


class BaseExportEntitiesData(BaseOperationData):
    """Базовый класс экспорта сущностей РВД за указанных период."""

    def __init__(
        self,
        entities: Iterable[str],
        period_started_at=datetime.combine(date.today(), time.min),
        period_ended_at=datetime.combine(date.today(), time.min),
        **kwargs,
    ):
        super().__init__(**kwargs)

        # Если сущности не указаны, берется значение по умолчанию - все сущности:
        entities = entities if entities else RegionalDataMartEntityEnum.get_enum_data().keys()
        self.entities: list[ModelEnumValue] = [
            RegionalDataMartEntityEnum.get_model_enum_value(entity) for entity in entities
        ]

        self.period_started_at = period_started_at
        self.period_ended_at = period_ended_at

        # Классы менеджеров Функций, которые должны быть запущены для выгрузки данных
        self._exporting_data_managers: set[type['RunnerManager']] = set()

        # Результаты работы Функций выгрузки данных
        self._exporting_data_results = []

        # Карта соответствия manager_id сущности и его основной модели
        self.manager_main_model_map: dict[str, ModelBase] = {}

    @property
    def _log_file_path(self) -> str:
        """
        Путь до лог файла.
        """
        return os.path.join(settings.MEDIA_ROOT, settings.RDM_EXPORT_LOG_DIR, f'{self.command_id}.log')

    def _has_stage_created_or_in_progress(self, manager_id: str, entity: str) -> bool:
        """Проверяет есть ли готовый к работе stage или в работе для данной сущности."""
        stage_created_or_in_progress = ExportingDataStage.objects.filter(
            manager_id=manager_id,
            status_id__in=(ExportingDataSubStageStatus.CREATED.key, ExportingDataSubStageStatus.IN_PROGRESS.key),
        ).exists()

        if stage_created_or_in_progress:
            logger.info(f'entity {entity} is skipped because it is already created or in progress!')

        return stage_created_or_in_progress

    def _fill_manager_entities_map(self, entity_storage: RegionalDataMartEntityStorage) -> None:
        """
        Заполнение словаря данных с классами менеджеров и их сущностями.
        """

    def _find_exporting_entities_data_managers(self):
        """
        Поиск менеджеров Функций выгрузки данных по сущностям РВД.
        """
        logger.info('find exporting entities data manager..')

        entity_storage = RegionalDataMartEntityStorage()
        entity_storage.prepare()

        exporting_entities_data_managers_map = entity_storage.prepare_entities_manager_map(
            tags={REGIONAL_DATA_MART_INTEGRATION_EXPORTING_DATA},
        )
        self._fill_manager_entities_map(entity_storage)

        entities = filter(lambda entity: entity.order_number != DEFAULT_ORDER_NUMBER, self.entities)

        for entity_enum in entities:
            manager_class = exporting_entities_data_managers_map.get(entity_enum.key)

            if manager_class and not self._has_stage_created_or_in_progress(manager_class.uuid, entity_enum.key):
                self.manager_main_model_map[manager_class.uuid] = entity_enum.main_model_enum.model
                self._exporting_data_managers.add(manager_class)

        logger.info('finding exporting entities data manager finished.')

    def _export_entities_data(self, *args, **kwargs):
        """
        Выгрузка данных по указанным сущностям.
        """
        logger.info('start exporting entities data..')

        kwargs['period_started_at'] = self.period_started_at
        kwargs['period_ended_at'] = self.period_ended_at

        for manager_class in self._exporting_data_managers:
            manager = manager_class(*args, is_only_main_model=True, **kwargs)

            if self.command_id:
                # Подается сигнал, что менеджер создан:
                manager_created.send(sender=manager, command_id=self.command_id)

            manager.run()

            self._exporting_data_results.append(manager.result)

        logger.info('exporting entities data finished.')

    def _export(self, *args, **kwargs):
        """
        Выполнение действий команды.
        """
        logger.info(f'start exporting data of entities - {", ".join([entity.key for entity in self.entities])}..')

        self._find_exporting_entities_data_managers()
        self._export_entities_data(*args, **kwargs)

        logger.info('exporting entities data finished.')

    def export(self, *args, **kwargs):
        """
        Запускает экспорт данных.
        """
        try:
            self._export(*args, **kwargs)
        except Exception as err:
            logger.exception(err)
            raise err
        finally:
            self._remove_file_handler()


class BaseExportLatestEntitiesData(BaseExportEntitiesData):
    """Базовый класс выгрузки сущностей с момента последней успешной выгрузки."""

    def __init__(
        self,
        entities: Iterable[str],
        period_started_at=datetime.combine(date.today(), time.min),
        period_ended_at=datetime.combine(date.today(), time.min),
        update_modified: bool = True,
        **kwargs,
    ):
        super().__init__(entities, period_started_at, period_ended_at, **kwargs)

        self._exporting_data_managers: set[type['RunnerManager']] = OrderedSet()

        # Словарь данных с классами менеджеров и их сущностями
        self._manager_entities_map: dict[type[object], list[str]] = defaultdict(set)

        self.async_task = self._get_async_task()
        self.task_id = kwargs.get('task_id')

        self.update_modified = update_modified

    def _get_async_task(self) -> Model:
        """Возвращает модель асинхронной задачи."""
        raise NotImplementedError

    def _set_description_to_async_task(self, exported_entities: Iterable[str]) -> None:
        """Добавляет в описание асинхронной задачи список выгруженных сущностей."""
        if exported_entities and self.task_id:
            self.async_task.objects.filter(
                pk=self.task_id,
            ).update(
                description=Concat(
                    'description',
                    Value(f': {", ".join(exported_entities)}')
                ),
            )

    def _fill_manager_entities_map(self, entity_storage: RegionalDataMartEntityStorage) -> None:
        """
        Заполнение словаря данных с классами менеджеров и их сущностями.
        """
        self._manager_entities_map = entity_storage.prepare_manager_entities_map(
            tags={REGIONAL_DATA_MART_INTEGRATION_EXPORTING_DATA},
        )

    def _update_model_modified_field(self, manager_id: str, last_finished_export_data: datetime) -> None:
        """Обновляет поле modified у невыгруженных записей."""
        if not self.update_modified:
            return

        model = self.manager_main_model_map[manager_id]
        now = timezone.now()

        querysets_to_update = (
            # Не заполнен подэтап выгрузки и modified записи модели < левой границы периода команды latest:
            model.objects.filter(
                exporting_sub_stage_id__isnull=True,
                modified__lt=last_finished_export_data,
            ),
            # Подэтап выгрузки указанной в записи модели имеет статус FAILED
            # и modified записи > даты выгрузки указанной в записи модели сбора (ended_at подэтапа выгрузки)
            # и modified записи модели < левой границы периода команды latest (даты последней удачной выгрузки):
            model.objects.filter(
                exporting_sub_stage__ended_at__gt=now - timedelta(days=365),
                exporting_sub_stage__status_id=ExportingDataSubStageStatus.FAILED.key,
                modified__gt=F('exporting_sub_stage__ended_at'),
                modified__lt=last_finished_export_data,
            ),
        )

        for queryset in querysets_to_update:
            not_exported_model_ids = queryset.values_list('id', flat=True).iterator()

            with atomic():

                for model_ids in make_chunks(
                    iterable=not_exported_model_ids,
                    size=settings.RDM_UPDATE_NON_EXPORTED_CHUNK_SIZE,
                ):
                    queryset.filter(id__in=model_ids).update(modified=now)

    def _export_entities_data(self, *args, **kwargs) -> None:
        """
        Запуск Функций по для экспорта данных.
        """
        logger.info('export entities data..')

        # Массив с выгружаемыми сущностями для поля "Описание" в асинхронной задаче
        exported_entities = []

        managers_max_period_ended = get_exporting_managers_max_period_ended_dates(
            self._exporting_data_managers
        )

        for manager_class in self._exporting_data_managers:
            manager_last_exported = managers_max_period_ended.get(manager_class.uuid)

            kwargs['period_started_at'] = manager_last_exported or timezone.now()
            kwargs['period_ended_at'] = get_today_max_datetime()

            # Обновить поля modified у модели сущности:
            self._update_model_modified_field(
                manager_id=manager_class.uuid,
                last_finished_export_data=kwargs['period_started_at'],
            )

            manager = manager_class(*args, **kwargs)

            if self.command_id:
                # Подается сигнал, что менеджер создан:
                manager_created.send(sender=manager, command_id=self.command_id)

            manager.run()

            self._exporting_data_results.append(manager.result)

            # Если сущность была выгружена, то добавим ее в список exported_entities
            if manager.result.entities and self.task_id:
                exported_entities.extend(self._manager_entities_map.get(manager_class))

        self._set_description_to_async_task(exported_entities)

        logger.info('collecting entities data finished.')


class ExportEntitiesData(BaseExportEntitiesData):
    """Экспорт сущностей РВД за указанных период."""


class ExportLatestEntitiesData(BaseExportLatestEntitiesData):
    """Класс выгрузки сущностей с момента последней успешной выгрузки."""

    def _get_async_task(self) -> Model:
        """Возвращает модель асинхронной задачи."""
        return RunningTask


class UploadData(BaseOperationData):
    """Класс отправки файлов в витрину."""

    def __init__(
        self,
        data_cache: AbstractCache,
        queue: Queue,
        **kwargs,
    ):
        super().__init__(**kwargs)

        self.data_cache = data_cache
        self.queue = queue

        self._configure_agent_client()
        self.result = {
            'total_file_size': 0,  # Общий размер отправленных файлов
            'queue_is_full': False,  # Признак переполнения очереди
            'uploaded_entities': ''  # Список сущностей, попавших в выгрузку
        }

    @property
    def _log_file_path(self) -> Union[str, bytes]:
        """
        Путь до лог файла.
        """
        return os.path.join(settings.MEDIA_ROOT, settings.RDM_UPLOAD_LOG_DIR, 'upload_entity.log')

    def _add_file_handler(self) -> None:
        """Добавляет обработчик логов."""

        self._file_handler = logging.FileHandler(self._log_file_path)

        logging.getLogger('info_logger').addHandler(self._file_handler)
        logging.getLogger('exception_logger').addHandler(self._file_handler)

    # TODO https://jira.bars.group/browse/EDUSCHL-22492. Вынужденная мера, т.к. при запуске команды не производится
    #  проверка готовности конфигов приложений. Нужно переработать механизм конфигурирования клиента загрузчика.
    def _configure_agent_client(self):
        """
        Конфигурирование клиента загрузчика данных в Витрину.
        """
        import uploader_client
        from django.core.cache import (
            DEFAULT_CACHE_ALIAS,
            caches,
        )
        from uploader_client.contrib.rdm.interfaces.configurations import (
            RegionalDataMartEmulationUploaderConfig,
            RegionalDataMartUploaderConfig,
        )
        if settings.RDM_UPLOADER_CLIENT_ENABLE_REQUEST_EMULATION:
            uploader_client.set_config(
                RegionalDataMartEmulationUploaderConfig(
                    interface='uploader_client.contrib.rdm.interfaces.rest.OpenAPIInterfaceEmulation',
                    url=settings.RDM_UPLOADER_CLIENT_URL,
                    datamart_name=settings.RDM_UPLOADER_CLIENT_DATAMART_NAME,
                    timeout=1,
                    request_retries=1,
                    file_status=settings.RDM_RESPONSE_FILE_STATUS
                )
            )
        elif settings.RDM_UPLOADER_CLIENT_USE_PROXY_API:
            uploader_client.set_config(
                RegionalDataMartUploaderConfig(
                    interface='uploader_client.contrib.rdm.interfaces.rest.ProxyAPIInterface',
                    cache=caches[DEFAULT_CACHE_ALIAS],
                    url=settings.RDM_UPLOADER_CLIENT_URL,
                    datamart_name=settings.RDM_UPLOADER_CLIENT_DATAMART_NAME,
                    timeout=settings.RDM_UPLOADER_CLIENT_REQUEST_TIMEOUT,
                    request_retries=settings.RDM_UPLOADER_CLIENT_REQUEST_RETRIES,
                    organization_ogrn=settings.RDM_UPLOADER_CLIENT_ORGANIZATION_OGRN,
                    installation_name=settings.RDM_UPLOADER_CLIENT_INSTALLATION_NAME,
                    installation_id=settings.RDM_UPLOADER_CLIENT_INSTALLATION_ID,
                    username=settings.RDM_UPLOADER_CLIENT_USERNAME,
                    password=settings.RDM_UPLOADER_CLIENT_PASSWORD,
                )
            )
        else:
            uploader_client.set_config(
                RegionalDataMartUploaderConfig(
                    url=settings.RDM_UPLOADER_CLIENT_URL,
                    datamart_name=settings.RDM_UPLOADER_CLIENT_DATAMART_NAME,
                    timeout=settings.RDM_UPLOADER_CLIENT_REQUEST_TIMEOUT,
                    request_retries=settings.RDM_UPLOADER_CLIENT_REQUEST_RETRIES,
                )
            )

    def update_total_queue_size_in_cache(self, received_files_size: int):
        """Обновление размера файлов в кеш."""
        with self.data_cache.lock(f'{TOTAL_ATTACHMENTS_SIZE_KEY}:lock', timeout=300):
            queue_total_file_size = self.data_cache.get(TOTAL_ATTACHMENTS_SIZE_KEY) or 0
            if queue_total_file_size:
                queue_total_file_size -= received_files_size
                if queue_total_file_size > 0:
                    self.data_cache.set(
                        TOTAL_ATTACHMENTS_SIZE_KEY,
                        queue_total_file_size,
                        timeout=settings.RDM_REDIS_CACHE_TIMEOUT_SECONDS
                    )

    def upload_data(self, *args, **kwargs):
        """
        Запускает отправку данных в витрину.
        """
        try:
            exporter = ExportQueueSender(self.data_cache, self.queue, settings.RDM_UPLOAD_DATA_TASK_EXPORT_STAGES)
            exporter.run()

            self.result['queue_is_full'] = exporter.queue_is_full
            self.result['total_file_size'] = exporter.queue_total_file_size

            # Если очередь не переполнена - то отправляем данные в витрину
            if not exporter.queue_is_full:
                sender = WorkerSender(self.queue)
                sender.run()

                if sender.entities:
                    self.result['uploaded_entities'] = ','.join(sender.entities)

                if sender.received_file_size:
                    self.update_total_queue_size_in_cache(sender.received_file_size)

        except Exception as err:
            logger.exception(err)
            raise err
        finally:
            self._remove_file_handler()

        return self.result
