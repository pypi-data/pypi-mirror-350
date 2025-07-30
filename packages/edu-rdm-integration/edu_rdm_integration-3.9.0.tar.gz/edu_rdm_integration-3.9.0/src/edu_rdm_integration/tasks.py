from collections import (
    defaultdict,
)
from typing import (
    TYPE_CHECKING,
    Optional,
)

import celery
from celery.schedules import (
    crontab,
)
from django.conf import (
    settings,
)
from django.core.cache import (
    cache,
)
from django.utils import (
    timezone,
)

from educommon.async_task.models import (
    AsyncTaskType,
    RunningTask,
)
from educommon.async_task.tasks import (
    UniquePeriodicAsyncTask,
)
from educommon.utils.date import (
    get_today_min_datetime,
)

from edu_rdm_integration.base import (
    BaseTransferLatestEntitiesDataMixin,
)
from edu_rdm_integration.collect_and_export_data.models import (
    EduRdmCollectDataCommandProgress,
    EduRdmExportDataCommandProgress,
)
from edu_rdm_integration.collect_data.collect import (
    BaseCollectLatestModelsData,
)
from edu_rdm_integration.collect_data.helpers import (
    set_failed_status_suspended_collecting_data_stages,
)
from edu_rdm_integration.consts import (
    FAST_TRANSFER_TASK_QUEUE_NAME,
    LONG_TRANSFER_TASK_QUEUE_NAME,
    TASK_QUEUE_NAME,
)
from edu_rdm_integration.enums import (
    CommandType,
    EntityLevelQueueTypeEnum,
    FileUploadStatusEnum,
)
from edu_rdm_integration.export_data.export import (
    ExportLatestEntitiesData,
    UploadData,
)
from edu_rdm_integration.export_data.helpers import (
    set_failed_status_suspended_exporting_data_stages,
)
from edu_rdm_integration.export_data.queue import (
    RdmRedisSubStageAttachmentQueue,
)
from edu_rdm_integration.helpers import (
    UploadStatusHelper,
    save_command_log_link,
)
from edu_rdm_integration.models import (
    ExportingDataSubStageUploaderClientLog,
    TransferredEntity,
)


if TYPE_CHECKING:
    from datetime import (
        datetime,
    )


class RDMCheckUploadStatus(UniquePeriodicAsyncTask):
    """Периодическая задача для сбора статусов по загрузке файла в витрину."""

    queue = TASK_QUEUE_NAME
    routing_key = TASK_QUEUE_NAME
    description = 'Сбор статусов загрузки данных в витрину "Региональная витрина данных"'
    lock_expire_seconds = settings.RDM_UPLOAD_STATUS_TASK_LOCK_EXPIRE_SECONDS
    task_type = AsyncTaskType.UNKNOWN
    run_every = crontab(
        minute=settings.RDM_UPLOAD_STATUS_TASK_MINUTE,
        hour=settings.RDM_UPLOAD_STATUS_TASK_HOUR,
        day_of_week=settings.RDM_UPLOAD_STATUS_TASK_DAY_OF_WEEK,
    )

    def process(self, *args, **kwargs):
        """Выполнение."""
        super().process(*args, **kwargs)

        # Получаем незавершенные загрузки данных в витрину
        in_progress_uploads = ExportingDataSubStageUploaderClientLog.objects.filter(
            file_upload_status=FileUploadStatusEnum.IN_PROGRESS,
            is_emulation=False,
        ).select_related('attachment')

        UploadStatusHelper(in_progress_uploads, cache).run()


class CheckSuspendedExportedStagePeriodicTask(UniquePeriodicAsyncTask):
    """Периодическая задача поиска зависших этапов/подэтапов экспорта."""

    queue = TASK_QUEUE_NAME
    routing_key = TASK_QUEUE_NAME
    description = 'Поиск зависших этапов/подэтапов экспорта в "Региональная витрина данных"'
    lock_expire_seconds = settings.RDM_CHECK_SUSPEND_TASK_LOCK_EXPIRE_SECONDS
    task_type = AsyncTaskType.SYSTEM
    run_every = crontab(
        minute=settings.RDM_CHECK_SUSPEND_TASK_MINUTE,
        hour=settings.RDM_CHECK_SUSPEND_TASK_HOUR,
        day_of_week=settings.RDM_CHECK_SUSPEND_TASK_DAY_OF_WEEK,
    )

    def process(self, *args, **kwargs):
        """Выполнение задачи."""
        super().process(*args, **kwargs)

        change_status_collecting_result = set_failed_status_suspended_collecting_data_stages()
        change_status_exporting_result = set_failed_status_suspended_exporting_data_stages()

        task_result = {
            'Прервано сборок': (
                f'Этапов {change_status_collecting_result["change_stage_count"]}'
                f' и подэтапов {change_status_collecting_result["change_sub_stage_count"]}'
            ),
            'Прервано выгрузок': (
                f'Этапов {change_status_exporting_result["change_stage_count"]}'
                f' и подэтапов {change_status_exporting_result["change_sub_stage_count"]}'
            ),
        }

        self.set_progress(
            values=task_result
        )


class BaseTransferLatestEntitiesDataPeriodicTask(BaseTransferLatestEntitiesDataMixin, UniquePeriodicAsyncTask):
    """Базовая периодическая задача сбора и выгрузки данных для переиспользования в разных очередях."""

    def __init__(self) -> None:
        super().__init__()

        self._period_ended_at: Optional[datetime] = None

    def _get_period_ended_at(self):
        """Определяет единую дату окончания периода сбора.

        Это нужно для исключения разного времени окончания сбора при явном запуске функции - чтобы
        избежать ошибки экспорта при недосборе данных.
        """
        if not self._period_ended_at:
            self._period_ended_at = timezone.now()

        return self._period_ended_at

    def _run_collect_model_data(self, model: str, task_id: str) -> None:
        """Запускает сбор данных модели РВД."""
        command = self._create_collect_command(model, task_id)
        collect_model_data = self._prepare_collect_model_data_class(command)
        collect_model_data.collect()

        command.refresh_from_db(fields=['stage_id'])
        save_command_log_link(command, settings.RDM_COLLECT_LOG_DIR)

    def _run_export_entity_data(self, entity: str, task_id: str) -> None:
        """Запускает экспорт данных сущности РВД."""
        command = self._create_export_command(entity, task_id)
        if command:
            export_entity_data = self._prepare_export_entity_data_class(command)
            export_entity_data.export()

            command.refresh_from_db(fields=['stage_id'])
            save_command_log_link(command, settings.RDM_EXPORT_LOG_DIR)

    def _create_collect_command(self, model: str, task_id: str) -> EduRdmCollectDataCommandProgress:
        """Создает команду сбора данных моделей РВД."""
        manager = self._collecting_data_managers[model]
        manager_last_collected = (
            self._collecting_data_manager_to_logs_period_end.get(manager.uuid)
            or get_today_min_datetime()
        )

        period_started_at = manager_last_collected
        period_ended_at = self._get_period_ended_at()

        return EduRdmCollectDataCommandProgress.objects.create(
            model_id=model,
            logs_period_started_at=period_started_at,
            logs_period_ended_at=period_ended_at,
            task_id=task_id,
            type=CommandType.AUTO,
        )

    def _create_export_command(self, entity: str, task_id: str) -> Optional[EduRdmExportDataCommandProgress]:
        """Создает команду экспорта данных сущностей РВД."""
        manager = self._exporting_data_managers[entity]
        manager_last_exported = self._exporting_data_manager_to_period_end.get(manager.uuid)

        if manager_last_exported:
            period_started_at = manager_last_exported
            period_ended_at = timezone.now()

            return EduRdmExportDataCommandProgress.objects.create(
                entity_id=entity,
                period_started_at=period_started_at,
                period_ended_at=period_ended_at,
                task_id=task_id,
                type=CommandType.AUTO,
            )

    def _prepare_collect_model_data_class(
        self,
        command: EduRdmCollectDataCommandProgress
    ) -> BaseCollectLatestModelsData:
        """Подготавливает объект класса сбора данных моделей РВД."""
        return BaseCollectLatestModelsData(
            models=[command.model_id],
            logs_period_started_at=command.logs_period_started_at,
            logs_period_ended_at=command.logs_period_ended_at,
            command_id=command.id,
            use_times_limit=True,
        )

    def _prepare_export_entity_data_class(self, command: EduRdmExportDataCommandProgress) -> ExportLatestEntitiesData:
        """Подготавливает объект класса экспорта данных сущностей РВД.

        При экспорте данных передаем параметр task_id для обновления поля "Описание"
        наименованиями выгруженных сущностей.
        """
        return ExportLatestEntitiesData(
            entities=[command.entity_id],
            period_started_at=command.period_started_at,
            period_ended_at=command.period_ended_at,
            command_id=command.id,
            task_id=self.request.id,
        )

    def process(self, *args, **kwargs):
        """Выполняет задачу."""
        super().process(*args, **kwargs)

        self._period_ended_at = None
        self.prepare_collect_export_managers()

        task_id = RunningTask.objects.filter(
            pk=self.request.id,
        ).values_list('pk', flat=True).first()

        collected_entity_models = set()

        for entity_enum, export_enabled in sorted(
            self._transferred_entities, key=lambda entity: entity[0].order_number
        ):
            entity_models = self._entites_models_map.get(entity_enum.key, ())
            for model_enum_value in entity_models:
                if model_enum_value.key not in collected_entity_models:
                    collected_entity_models.add(model_enum_value.key)
                    try:
                        self._run_collect_model_data(model_enum_value.key, task_id)
                    except Exception:
                        continue

            try:
                if export_enabled:
                    self._run_export_entity_data(entity_enum.key, task_id)
            except Exception:
                continue


class TransferLatestEntitiesDataPeriodicTask(BaseTransferLatestEntitiesDataPeriodicTask):
    """Периодическая задача сбора и выгрузки данных."""

    queue = TASK_QUEUE_NAME
    routing_key = TASK_QUEUE_NAME
    description = 'Периодическая задача сбора и экспорта данных РВД'
    lock_expire_seconds = settings.RDM_TRANSFER_TASK_LOCK_EXPIRE_SECONDS
    task_type = AsyncTaskType.UNKNOWN
    run_every = crontab(
        minute=settings.RDM_TRANSFER_TASK_MINUTE,
        hour=settings.RDM_TRANSFER_TASK_HOUR,
        day_of_week=settings.RDM_TRANSFER_TASK_DAY_OF_WEEK,
    )

    def get_entity_qs(self) -> 'QuerySet[TransferredEntity]':
        return TransferredEntity.objects.filter(queue_level=EntityLevelQueueTypeEnum.BASE)


class TransferLatestEntitiesDataFastPeriodicTask(BaseTransferLatestEntitiesDataPeriodicTask):
    """Периодическая задача сбора и выгрузки данных для быстрого уровня очереди."""

    queue = FAST_TRANSFER_TASK_QUEUE_NAME
    routing_key = FAST_TRANSFER_TASK_QUEUE_NAME
    description = 'Периодическая задача сбора и экспорта данных РВД (быстрый уровень)'
    lock_expire_seconds = settings.RDM_FAST_TRANSFER_TASK_LOCK_EXPIRE_SECONDS
    task_type = AsyncTaskType.UNKNOWN
    run_every = crontab(
        minute=settings.RDM_FAST_TRANSFER_TASK_MINUTE,
        hour=settings.RDM_FAST_TRANSFER_TASK_HOUR,
        day_of_week=settings.RDM_FAST_TRANSFER_TASK_DAY_OF_WEEK,
    )

    def get_entity_qs(self) -> 'QuerySet[TransferredEntity]':
        return TransferredEntity.objects.filter(queue_level=EntityLevelQueueTypeEnum.FAST)


class TransferLatestEntitiesDataLongPeriodicTask(BaseTransferLatestEntitiesDataPeriodicTask):
    """Периодическая задача сбора и выгрузки данных для долгого уровня очереди."""

    queue = LONG_TRANSFER_TASK_QUEUE_NAME
    routing_key = LONG_TRANSFER_TASK_QUEUE_NAME
    description = 'Периодическая задача сбора и экспорта данных РВД (долгий уровень)'
    lock_expire_seconds = settings.RDM_LONG_TRANSFER_TASK_LOCK_EXPIRE_SECONDS
    task_type = AsyncTaskType.UNKNOWN
    run_every = crontab(
        minute=settings.RDM_LONG_TRANSFER_TASK_MINUTE,
        hour=settings.RDM_LONG_TRANSFER_TASK_HOUR,
        day_of_week=settings.RDM_LONG_TRANSFER_TASK_DAY_OF_WEEK,
    )

    def get_entity_qs(self) -> 'QuerySet[TransferredEntity]':
        return TransferredEntity.objects.filter(queue_level=EntityLevelQueueTypeEnum.LONG)


class UploadDataAsyncTask(UniquePeriodicAsyncTask):
    """Формирование очереди файлов и их отправка."""

    queue = TASK_QUEUE_NAME
    routing_key = TASK_QUEUE_NAME
    description = 'Отправка данных в витрину "Региональная витрина данных"'
    lock_expire_seconds = settings.RDM_UPLOAD_DATA_TASK_LOCK_EXPIRE_SECONDS
    task_type = AsyncTaskType.SYSTEM
    run_every = crontab(
        minute=settings.RDM_UPLOAD_DATA_TASK_MINUTE,
        hour=settings.RDM_UPLOAD_DATA_TASK_HOUR,
        day_of_week=settings.RDM_UPLOAD_DATA_TASK_DAY_OF_WEEK,
    )

    def process(self, *args, **kwargs):
        """Выполнение."""
        super().process(*args, **kwargs)

        queue = RdmRedisSubStageAttachmentQueue()
        upload_data = UploadData(
            data_cache=cache,
            queue=queue,
        )

        upload_result = upload_data.upload_data()

        task_result = {
            'Общий объем отправленных файлов': f"{upload_result['total_file_size']}",
            'Очередь отправки переполнена': 'Да' if upload_result['queue_is_full'] else 'Нет',
            'Сущности, отправленные в витрину': upload_result['uploaded_entities']
        }

        self.set_progress(
            values=task_result
        )


celery_app = celery.app.app_or_default()
celery_app.register_task(RDMCheckUploadStatus)
celery_app.register_task(CheckSuspendedExportedStagePeriodicTask)
celery_app.register_task(TransferLatestEntitiesDataPeriodicTask)
celery_app.register_task(UploadDataAsyncTask)
celery_app.register_task(TransferLatestEntitiesDataFastPeriodicTask)
celery_app.register_task(TransferLatestEntitiesDataLongPeriodicTask)