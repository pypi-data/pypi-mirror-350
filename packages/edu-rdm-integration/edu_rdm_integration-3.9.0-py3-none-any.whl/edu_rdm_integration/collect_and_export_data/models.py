from django.db.models import (
    SET_NULL,
    FileField,
    ForeignKey,
    PositiveSmallIntegerField,
)

from edu_rdm_integration.enums import (
    CommandType,
)
from edu_rdm_integration.models import (
    AbstractCollectDataCommandProgress,
    AbstractExportDataCommandProgress,
)
from edu_rdm_integration.utils import (
    get_data_command_progress_attachment_path,
)


class EduRdmCollectDataCommandProgress(AbstractCollectDataCommandProgress):
    """
    Модель, хранящая данные для формирования и отслеживания асинхронных задач по сбору данных.
    """

    task = ForeignKey(
        to='async_task.RunningTask',
        verbose_name='Асинхронная задача',
        blank=True,
        null=True,
        on_delete=SET_NULL,
    )
    logs_link = FileField(
        upload_to=get_data_command_progress_attachment_path,
        max_length=255,
        verbose_name='Ссылка на файл логов',
    )
    type = PositiveSmallIntegerField(  # noqa: A003
        verbose_name='Тип команды',
        choices=CommandType.get_choices(),
    )

    class Meta(AbstractCollectDataCommandProgress.Meta):
        db_table = 'edu_rdm_collecting_data_command_progress'


class EduRdmExportDataCommandProgress(AbstractExportDataCommandProgress):
    """Команда экспорта данных."""

    task = ForeignKey(
        to='async_task.RunningTask',
        verbose_name='Асинхронная задача',
        null=True,
        blank=True,
        on_delete=SET_NULL,
    )
    logs_link = FileField(
        upload_to=get_data_command_progress_attachment_path,
        max_length=255,
        verbose_name='Файл лога',
    )
    type = PositiveSmallIntegerField(  # noqa: A003
        verbose_name='Тип команды',
        choices=CommandType.get_choices(),
    )

    class Meta(AbstractExportDataCommandProgress.Meta):
        db_table = 'edu_rdm_exporting_data_command_progress'
