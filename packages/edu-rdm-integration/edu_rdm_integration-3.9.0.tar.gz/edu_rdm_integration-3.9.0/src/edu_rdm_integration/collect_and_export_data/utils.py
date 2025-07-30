from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Dict,
    Iterable,
    Optional,
)

from django.db.models import (
    QuerySet,
)

from educommon.async_task.exceptions import (
    TaskUniqueException,
)
from educommon.async_task.models import (
    AsyncTaskType,
)
from educommon.async_task.tasks import (
    AsyncTask,
)

from edu_rdm_integration.collect_and_export_data.models import (
    EduRdmCollectDataCommandProgress,
    EduRdmExportDataCommandProgress,
)
from edu_rdm_integration.collect_data.collect import (
    BaseCollectModelsDataByGeneratingLogs,
)
from edu_rdm_integration.consts import (
    TASK_QUEUE_NAME,
)
from edu_rdm_integration.enums import (
    EntityLevelQueueTypeEnum,
)
from edu_rdm_integration.export_data.export import (
    ExportEntitiesData,
)
from edu_rdm_integration.helpers import (
    save_command_log_link,
)


class CollectCommandMixin:
    """Класс-примесь для запуска команды сборки моделей."""

    queue = TASK_QUEUE_NAME
    routing_key = TASK_QUEUE_NAME
    description = 'Сбор данных моделей РВД'
    task_type = AsyncTaskType.SYSTEM

    def get_collect_command(self, command_id: int) -> EduRdmCollectDataCommandProgress:
        """Возвращает экземпляр модели команды запуска."""
        command = EduRdmCollectDataCommandProgress.objects.get(id=command_id)

        return command

    def get_collect_models_class(self):
        """Возвращает класс для сбора данных."""
        return BaseCollectModelsDataByGeneratingLogs

    def run_collect_command(self, command) -> None:
        """Запуск команды сбора."""
        collect_models_data_class = self.get_collect_models_class()
        collect_models_data_class(
            models=(command.model_id,),
            logs_period_started_at=command.logs_period_started_at,
            logs_period_ended_at=command.logs_period_ended_at,
            command_id=command.id,
            institute_ids=tuple(command.institute_ids or ()),
        ).collect()

    def save_collect_command_logs(self, command_id: int, log_dir: str):
        """Сохранение ссылки на файл логов в команде."""
        try:
            command = self.get_collect_command(command_id)
        except EduRdmCollectDataCommandProgress.DoesNotExist:
            command = None

        if command:
            save_command_log_link(command, log_dir)


class ExportCommandMixin:
    """Класс-примесь для запуска команды выгрузки сущностей."""

    queue = TASK_QUEUE_NAME
    routing_key = TASK_QUEUE_NAME
    description = 'Экспорт данных сущностей РВД'
    task_type = AsyncTaskType.SYSTEM

    def get_export_command(self, command_id: int) -> EduRdmExportDataCommandProgress:
        """Возвращает экземпляр модели команды запуска."""
        command = EduRdmExportDataCommandProgress.objects.get(id=command_id)

        return command

    def run_export_command(self, command: EduRdmExportDataCommandProgress) -> None:
        """Запуск команды выгрузки."""
        ExportEntitiesData(
            entities=(command.entity_id,),
            period_started_at=command.period_started_at,
            period_ended_at=command.period_ended_at,
            command_id=command.id,
        ).export()

    def save_export_command_logs(self, command_id: int, log_dir: str):
        """Сохранение ссылки на файл логов в команде."""
        try:
            command = self.get_export_command(command_id)
        except EduRdmExportDataCommandProgress.DoesNotExist:
            command = None

        if command:
            save_command_log_link(command, log_dir)


class BaseTaskProgressUpdater(ABC):
    """Базовый класс, который обновляет данные в таблицах, хранящих команды сбора/экспорта."""

    @property
    @abstractmethod
    def update_model(self):
        """
        Основная модель для обновления.

        Необходимо задать в дочернем классе.
        """

    @property
    @abstractmethod
    def async_model(self):
        """
        Модель асинхронных задач.

        Необходимо задать в дочернем классе.
        """

    def set_async_task(self, commands_to_update: Dict[EduRdmCollectDataCommandProgress, str]) -> None:
        """Устанавливает ссылку на асинхронную задачу."""
        for command, task_uuid in commands_to_update.items():
            command.task_id = task_uuid

        self.update_model.objects.bulk_update(
            commands_to_update,
            ['task_id'],
        )

    def set_stage(self, command_id: int, stage_id: int) -> None:
        """Устанавливает ссылку на stage."""
        self.update_model.objects.filter(
            id=command_id,
        ).update(
            stage_id=stage_id,
        )


class BaseTaskStarter(ABC):
    """Запускает асинхронные задачи."""

    updater: BaseTaskProgressUpdater = None
    async_task: AsyncTask = None
    model_only_fields: Iterable[str] = ()

    def run(self, command_ids: Iterable[int], queue_level: Optional[int] = None) -> str:
        """Создает задачи и ставит их в очередь."""
        commands_to_update = {}
        skipped_commands_count = 0
        commands = self._get_commands(command_ids)
        queue_name = None

        if queue_level:
            queue_name = EntityLevelQueueTypeEnum.get_queue_name(level=queue_level)

        if not queue_name:
            queue_name = TASK_QUEUE_NAME

        for command in commands:
            if command.task_id:
                # Повторный запуск команды не допускается
                skipped_commands_count += 1
                continue

            try:
                async_result = self.async_task().apply_async(  # noqa pylint: disable=not-callable
                    args=None,
                    queue=queue_name,
                    routing_key=queue_name,
                    kwargs={
                        'command_id': command.id,
                    },
                    lock_data={
                        'lock_params': {
                            'command_id': f'{self.updater.update_model.__name__}_{command.id}',
                        },
                    },
                )
            except TaskUniqueException:
                skipped_commands_count += 1
                continue
            else:
                commands_to_update[command] = async_result.task_id

        if commands_to_update:
            self.updater().set_async_task(commands_to_update)  # noqa pylint: disable=not-callable

        message = f'Поставлено задач в очередь: {len(commands_to_update)} из {len(commands)}.'
        if skipped_commands_count:
            message += (
                f' Кол-во задач, которые были запущены ранее: {skipped_commands_count}. '
                'Однажды запущенные задачи не могут быть запущены снова!'
            )

        return message

    def _get_commands(self, command_ids: Iterable[int]) -> 'QuerySet':
        """Возвращает Queryset команд для создания задач."""
        return self.updater.update_model.objects.filter(
            id__in=command_ids,
        ).only(
            *self.model_only_fields,
        )
