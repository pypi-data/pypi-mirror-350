import uuid
from datetime import (
    datetime,
)
from io import (
    StringIO,
)
from typing import (
    Optional,
)

from edu_rdm_integration.uploader_log.enums import (
    RequestResultStatus,
)

from django.db.models import (
    CASCADE,
    PROTECT,
    SET_NULL,
    BooleanField,
    CharField,
    DateTimeField,
    FileField,
    ForeignKey,
    JSONField,
    Manager,
    OneToOneField,
    PositiveIntegerField,
    PositiveSmallIntegerField,
    SmallIntegerField,
    UUIDField,
)
from django.utils import (
    timezone,
)
from django.utils.functional import (
    cached_property,
)
from m3 import (
    json_encode,
)
from m3.db import (
    BaseObjectModel,
)
from uploader_client.models import (
    Entry,
)

from educommon.django.db.mixins import (
    ReprStrPreModelMixin,
)
from educommon.integration_entities.enums import (
    EntityLogOperation,
)
from educommon.utils.date import (
    get_today_max_datetime,
    get_today_min_datetime,
)
from function_tools.models import (
    Entity,
)
from m3_db_utils.models import (
    ModelEnumValue,
    TitledIntegerModelEnum,
    TitledModelEnum,
)

from edu_rdm_integration.enums import (
    CommandType,
    EntityLevelQueueTypeEnum,
    FileUploadStatusEnum,
)
from edu_rdm_integration.uploader_log.managers import (
    UploaderClientLogManager,
)
from edu_rdm_integration.utils import (
    get_data_command_progress_attachment_path,
    get_exporting_data_stage_attachment_path,
)


class CollectingDataStageStatus(TitledModelEnum):
    """Статус этапа сбора данных."""

    CREATED = ModelEnumValue(
        title='Создан',
    )

    IN_PROGRESS = ModelEnumValue(
        title='В процессе сбора',
    )

    FAILED = ModelEnumValue(
        title='Завершено с ошибками',
    )

    FINISHED = ModelEnumValue(
        title='Завершено',
    )

    class Meta:
        db_table = 'rdm_collecting_data_stage_status'
        verbose_name = 'Модель-перечисление статусов этапа сбора данных'
        verbose_name_plural = 'Модели-перечисления статусов этапов сбора данных'


class CollectingExportedDataStage(ReprStrPreModelMixin, BaseObjectModel):
    """Этап подготовки данных в рамках Функций. За работу Функции отвечает ранер менеджер."""

    manager = ForeignKey(
        to=Entity,
        verbose_name='Менеджер ранера Функции',
        on_delete=PROTECT,
        null=True,
        blank=True,
    )

    logs_period_started_at = DateTimeField(
        'Левая граница периода обрабатываемых логов',
        db_index=True,
        default=get_today_min_datetime,
    )

    logs_period_ended_at = DateTimeField(
        'Правая граница периода обрабатываемых логов',
        db_index=True,
        default=get_today_max_datetime,
    )

    started_at = DateTimeField(
        'Время начала сбора данных',
        auto_now_add=True,
        db_index=True,
    )

    ended_at = DateTimeField(
        'Время завершения сбора данных',
        null=True,
        blank=True,
        db_index=True,
    )

    status = ForeignKey(
        to=CollectingDataStageStatus,
        verbose_name='Статус',
        on_delete=PROTECT,
        default=CollectingDataStageStatus.CREATED.key,
    )

    class Meta:
        db_table = 'rdm_collecting_exported_data_stage'
        verbose_name = 'Этап формирования данных для выгрузки'
        verbose_name_plural = 'Этапы формирования данных для выгрузки'

    @property
    def attrs_for_repr_str(self):
        """Список атрибутов для отображения экземпляра модели."""
        return ['manager_id', 'logs_period_started_at', 'logs_period_ended_at', 'started_at', 'ended_at', 'status_id']

    def save(self, *args, **kwargs):
        if (
            self.status_id in (CollectingDataStageStatus.FAILED.key, CollectingDataStageStatus.FINISHED.key)
            and not self.ended_at
        ):
            self.ended_at = datetime.now()

        super().save(*args, **kwargs)


class CollectingDataSubStageStatus(TitledModelEnum):
    """Статус этапа сбора данных."""

    CREATED = ModelEnumValue(
        title='Создан',
    )

    IN_PROGRESS = ModelEnumValue(
        title='В процессе сбора',
    )

    READY_TO_EXPORT = ModelEnumValue(
        title='Готово к выгрузке',
    )

    FAILED = ModelEnumValue(
        title='Завершено с ошибками',
    )

    EXPORTED = ModelEnumValue(
        title='Выгружено',
    )

    NOT_EXPORTED = ModelEnumValue(
        title='Не выгружено',
    )

    class Meta:
        db_table = 'rdm_collecting_data_sub_stage_status'
        verbose_name = 'Модель-перечисление статусов подэтапа сбора данных'
        verbose_name_plural = 'Модели-перечисления статусов подэтапов сбора данных'


class CollectingExportedDataSubStage(ReprStrPreModelMixin, BaseObjectModel):
    """Подэтап сбора данных для сущностей в рамках функции."""

    stage = ForeignKey(
        to=CollectingExportedDataStage,
        verbose_name='Этап подготовки данных для экспорта',
        on_delete=PROTECT,
    )

    function = ForeignKey(
        to=Entity,
        verbose_name='Функция',
        on_delete=PROTECT,
    )

    started_at = DateTimeField(
        'Время начала сбора данных',
        auto_now_add=True,
        db_index=True,
    )

    ended_at = DateTimeField(
        'Время завершения сбора данных',
        null=True,
        blank=True,
        db_index=True,
    )

    previous = ForeignKey(
        'self',
        null=True,
        blank=True,
        verbose_name='Предыдущий сбор данных',
        on_delete=CASCADE,
    )

    status = ForeignKey(
        to=CollectingDataSubStageStatus,
        verbose_name='Статус',
        on_delete=PROTECT,
        default=CollectingDataSubStageStatus.CREATED.key,
    )

    class Meta:
        db_table = 'rdm_collecting_exported_data_sub_stage'
        verbose_name = 'Подэтап формирования данных для выгрузки'
        verbose_name_plural = 'Подэтапы формирования данных для выгрузки'

    @property
    def attrs_for_repr_str(self):
        """Список атрибутов для отображения экземпляра модели."""
        return ['stage_id', 'function_id', 'started_at', 'ended_at', 'previous_id', 'status_id']

    def save(self, *args, **kwargs):
        if (
            self.status_id in (
                CollectingDataSubStageStatus.FAILED.key,
                CollectingDataSubStageStatus.READY_TO_EXPORT.key
            )
            and not self.ended_at
        ):
            self.ended_at = datetime.now()

        super().save(*args, **kwargs)


class ExportingDataStageStatus(TitledModelEnum):
    """
    Статус этапа выгрузки данных.
    """

    CREATED = ModelEnumValue(
        title='Создан',
    )

    IN_PROGRESS = ModelEnumValue(
        title='В процессе',
    )

    FAILED = ModelEnumValue(
        title='Завершено с ошибками',
    )

    FINISHED = ModelEnumValue(
        title='Завершено',
    )

    class Meta:
        db_table = 'rdm_exporting_data_stage_status'
        verbose_name = 'Модель-перечисление статусов этапа выгрузки данных'
        verbose_name_plural = 'Модели-перечисления статусов этапов выгрузки данных'


class ExportingDataStage(ReprStrPreModelMixin, BaseObjectModel):
    """
    Этап выгрузки данных.
    """

    manager = ForeignKey(
        to=Entity,
        verbose_name='Менеджер ранера Функции',
        on_delete=PROTECT,
        null=True,
        blank=True,
    )

    period_started_at = DateTimeField(
        'Левая граница периода выборки данных для выгрузки',
        db_index=True,
    )

    period_ended_at = DateTimeField(
        'Правая граница периода выборки данных для выгрузки',
        db_index=True,
    )

    started_at = DateTimeField(
        'Время начала выгрузки данных',
        auto_now_add=True,
    )

    ended_at = DateTimeField(
        'Время завершения выгрузки данных',
        null=True,
        blank=True,
    )

    status = ForeignKey(
        to=ExportingDataStageStatus,
        verbose_name='Статус',
        on_delete=PROTECT,
        default=ExportingDataStageStatus.CREATED.key,
    )

    class Meta:
        db_table = 'rdm_exporting_data_stage'
        verbose_name = 'Этап формирования данных для выгрузки'
        verbose_name_plural = 'Этапы формирования данных для выгрузки'

    @property
    def attrs_for_repr_str(self):
        """Список атрибутов для отображения экземпляра модели."""
        return ['manager_id', 'started_at', 'ended_at', 'status_id']

    def save(self, *args, **kwargs):
        if (
            self.status_id in (ExportingDataStageStatus.FAILED.key, ExportingDataStageStatus.FINISHED.key)
            and not self.ended_at
        ):
            self.ended_at = datetime.now()

        super().save(*args, **kwargs)


class ExportingDataSubStageStatus(TitledModelEnum):
    """Модель-перечисление статусов этапа выгрузки данных."""

    CREATED = ModelEnumValue(
        title='Создан',
    )

    IN_PROGRESS = ModelEnumValue(
        title='Запущен',
    )

    FAILED = ModelEnumValue(
        title='Завершено с ошибками',
    )

    FINISHED = ModelEnumValue(
        title='Завершен',
    )
    READY_FOR_EXPORT = ModelEnumValue(
        title='Готов к выгрузке',
    )
    PROCESS_ERROR = ModelEnumValue(
        title='Ошибка обработки витриной'
    )

    class Meta:
        db_table = 'rdm_exporting_data_sub_stage_status'
        verbose_name = 'Модель-перечисление статусов подэтапа выгрузки данных'
        verbose_name_plural = 'Модели-перечисления статусов подэтапов выгрузки данных'


class ExportingDataSubStage(ReprStrPreModelMixin, BaseObjectModel):
    """
    Подэтап выгрузки данных.
    """

    function = ForeignKey(
        to=Entity,
        verbose_name='Функция',
        on_delete=PROTECT,
        null=True,
        blank=True,
    )

    stage = ForeignKey(
        to=ExportingDataStage,
        verbose_name='Этап выгрузки данных',
        on_delete=CASCADE,
    )

    started_at = DateTimeField(
        verbose_name='Время начала сбора данных',
        auto_now_add=True,
        db_index=True,
    )

    ended_at = DateTimeField(
        verbose_name='Время завершения сбора данных',
        null=True,
        blank=True,
        db_index=True,
    )

    status = ForeignKey(
        to=ExportingDataSubStageStatus,
        verbose_name='Статус',
        on_delete=PROTECT,
        default=ExportingDataSubStageStatus.CREATED.key,
    )

    class Meta:
        db_table = 'rdm_exporting_data_sub_stage'
        verbose_name = 'Стадия выгрузки данных'
        verbose_name_plural = 'Стадии выгрузки данных'

    @property
    def attrs_for_repr_str(self):
        """Список атрибутов для отображения экземпляра модели."""
        return ['function_id', 'collecting_data_sub_stage_id', 'stage_id', 'started_at', 'ended_at', 'status_id']

    def save(self, *args, **kwargs):
        """Сохранение экземпляра модели."""
        if (
            self.status_id in {
                ExportingDataSubStageStatus.FAILED.key,
                ExportingDataSubStageStatus.FINISHED.key,
                ExportingDataSubStageStatus.READY_FOR_EXPORT.key,
            }
            and not self.ended_at
        ):
            self.ended_at = datetime.now()

        super().save(*args, **kwargs)


class ExportingDataSubStageAttachment(ReprStrPreModelMixin, BaseObjectModel):
    """
    Сгенерированный файл для дальнейшей выгрузки в "Региональная витрина данных".
    """

    exporting_data_sub_stage = ForeignKey(
        to=ExportingDataSubStage,
        verbose_name='Подэтап выгрузки данных',
        on_delete=CASCADE,
    )

    # TODO PYTD-22 В зависимости от принятого решения по инструменту ограничения доступа к media-файлам, нужно будет
    #  изменить тип поля или оставить как есть
    attachment = FileField(
        verbose_name='Сгенерированный файл',
        upload_to=get_exporting_data_stage_attachment_path,
        max_length=512,
        null=True,
        blank=True,
    )

    operation = SmallIntegerField(
        verbose_name='Действие',
        choices=EntityLogOperation.get_choices(),
    )

    created = DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        null=True,
        blank=True,
    )
    modified = DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True,
        null=True,
        blank=True,
    )
    attachment_size = PositiveIntegerField(
        null=True,
        verbose_name='Размер файла (байт)'
    )

    class Meta:
        db_table = 'rdm_exporting_data_sub_stage_attachment'
        verbose_name = 'Сгенерированный файл для дальнейшей выгрузки в "Региональная витрина данных"'
        verbose_name_plural = 'Сгенерированные файлы для дальнейшей выгрузки в "Региональная витрина данных"'

    @property
    def attrs_for_repr_str(self):
        """Список атрибутов для отображения экземпляра модели."""
        return ['exporting_data_sub_stage_id', 'attachment', 'operation', 'created', 'modified']


class DataMartRequestStatus(TitledIntegerModelEnum):
    """Модель-перечисление статусов загрузки данных в Витрину."""

    UPLOAD_TO_BUFFER = ModelEnumValue(
        value=-1,
        title='Загрузка данных в буффер',
    )

    BUFFERED = ModelEnumValue(
        value=0,
        title='Запрос буфферизирован',
    )

    WAIT_FOR_OPEN_DELTA = ModelEnumValue(
        value=1,
        title='Ожидает открытия дельты',
    )

    IN_PROCESSING = ModelEnumValue(
        value=2,
        title='В обработке',
    )

    SUCCESSFULLY_PROCESSED = ModelEnumValue(
        value=3,
        title='Успешно обработан',
    )

    FAILED_PROCESSING = ModelEnumValue(
        value=4,
        title='Ошибка обработки запроса',
    )

    REQUEST_ID_NOT_FOUND = ModelEnumValue(
        value=5,
        title='Идентификатор запроса не обнаружен',
    )

    FORMAT_LOGICAL_CONTROL = ModelEnumValue(
        value=6,
        title='Форматно-логический контроль',
    )

    FLC_ERROR = ModelEnumValue(
        value=7,
        title='Ошибки ФЛК',
    )

    class Meta:
        db_table = 'rdm_request_status'
        verbose_name = 'Статус загрузки данных в Витрину'
        verbose_name_plural = 'Статусы загрузки данных в Витрину'


class ExportingDataSubStageUploaderClientLog(ReprStrPreModelMixin, BaseObjectModel):
    """
    Связь лога Загрузчика данных с подэтапом выгрузки данных.
    """

    entry = ForeignKey(
        to=Entry,
        verbose_name='Лог запроса и ответа',
        on_delete=CASCADE,
        related_name='uploader_client_log',
    )

    sub_stage = ForeignKey(
        to=ExportingDataSubStage,
        verbose_name='Подэтап выгрузки данных',
        on_delete=CASCADE,
    )

    attachment = ForeignKey(
        to=ExportingDataSubStageAttachment,
        verbose_name='Прикрепленный файл',
        on_delete=CASCADE,
    )

    request_id = CharField(
        verbose_name='Id запроса загрузки в витрину',
        max_length=100,
        blank=True,
        db_index=True,
    )

    is_emulation = BooleanField(
        verbose_name='Включен режим эмуляции',
        default=False,
    )

    file_upload_status = SmallIntegerField(
        verbose_name='Общий статус загрузки файла в витрину',
        choices=FileUploadStatusEnum.get_choices(),
        null=True,
        blank=True,
    )

    created = DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        null=True,
        blank=True,
        db_index=True,
    )
    modified = DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True,
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        db_table = 'rdm_exporting_data_sub_stage_uploader_client_log'
        verbose_name = 'Лог запроса подэтапа выгрузки данных'
        verbose_name_plural = 'Лог запроса подэтапа выгрузки данных'


class UploadStatusRequestLog(ReprStrPreModelMixin, BaseObjectModel):
    """
    Модель связывающая статусы, загрузку файла в витрину и http-запрос к витрине.
    """

    upload = ForeignKey(
        verbose_name='Cвязь запроса статуса с загрузкой файла в витрину',
        to=ExportingDataSubStageUploaderClientLog,
        on_delete=CASCADE,
    )
    entry = ForeignKey(
        verbose_name='Cвязь запроса статуса с запросом в витрину',
        to=Entry,
        on_delete=CASCADE,
        related_name='upload_status_request_log',
    )
    request_status = ForeignKey(
        verbose_name='Статус запроса в витрине',
        to=DataMartRequestStatus,
        on_delete=PROTECT,
        null=True,
        blank=True,
    )

    class Meta:
        db_table = 'rdm_upload_status_request_log'
        verbose_name = 'Лог запроса подэтапа выгрузки данных'
        verbose_name_plural = 'Логи запроса подэтапа выгрузки данных'


class BaseEntityModel(ReprStrPreModelMixin, BaseObjectModel):
    """Базовая модель сущности."""

    collecting_sub_stage = ForeignKey(
        verbose_name='Подэтап сбора данных сущности',
        to=CollectingExportedDataSubStage,
        on_delete=CASCADE,
    )
    exporting_sub_stage = ForeignKey(
        verbose_name='Подэтап выгрузки',
        to=ExportingDataSubStage,
        blank=True,
        null=True,
        on_delete=CASCADE,
    )
    operation = SmallIntegerField(
        verbose_name='Действие',
        choices=EntityLogOperation.get_choices(),
    )

    created = DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
        null=True,
        blank=True,
        db_index=True,
    )
    modified = DateTimeField(
        verbose_name='Дата изменения',
        auto_now=True,
        null=True,
        blank=True,
        db_index=True,
    )

    @property
    def attrs_for_repr_str(self):
        """Список атрибутов для отображения экземпляра модели."""
        return ['collecting_sub_stage', 'exporting_sub_stage', 'operation', 'created', 'modified']

    class Meta:
        abstract = True


class RegionalDataMartModelEnum(TitledModelEnum):
    """Модель-перечисление моделей "Региональная витрина данных"."""

    class Meta:
        db_table = 'rdm_model'
        extensible = True
        verbose_name = 'Модель-перечисление моделей "Региональной витрины данных"'
        verbose_name_plural = 'Модели-перечисления моделей "Региональной витрины данных"'


class RegionalDataMartEntityEnum(TitledModelEnum):
    """Модель-перечисление сущностей выгрузки в Региональная витрина данных.

    Поля:
        entity - data-класс сущности;
        main_model_enum - значение модели-перечисления RegionalDataMartModelEnum основной модели РВД для формирования
            данных сущности. Обычно это модель идентификаторы записей которой соответствуют идентификаторам в записях
            сущности. У этих записей проставляется подэтап выгрузки данных;
        additional_model_enums - кортеж значений модели-перечисления RegionalDataMartModelEnum с дополнительными
            моделями РВД, которые участвуют в формировании записей сущностей. Они показывают, что перед запуском
            экспорта данных сущности по ним и основной модели должен быть запущен сбор данных.
    """

    class Meta:
        db_table = 'rdm_entity'
        extensible = True
        verbose_name = 'Модель-перечисление сущностей "Региональной витрины данных"'
        verbose_name_plural = 'Модели-перечисления сущностей "Региональной витрины данных"'

    @property
    def model_enums(self):
        """Возвращает модели, от которых зависит сущность."""
        value = self.model_enum_value

        return self.get_model_enums_from_value(value=value)

    @staticmethod
    def get_model_enums_from_value(value: ModelEnumValue):
        """Получение значений модели-перечисления моделей по значению модели-перечисления сущностей."""
        model_enums = [value.main_model_enum, *value.additional_model_enums]

        return model_enums

    @classmethod
    def get_entities_model_enums(
        cls,
        entity_enums: list[ModelEnumValue],
        is_sorted: bool = True,
    ) -> list[ModelEnumValue]:
        """Получение списка значений модели-перечисления моделей RegionalDataMartModelEnum.

        Args:
            entity_enums: Список значений модели-перечисления сущностей RegionalDataMartEntityEnum;
            is_sorted: Необходимость сортировки значений модели-перечисления RegionalDataMartModelEnum по полю
                order_number.
        """
        model_enums = set()

        for entity_enum_value in entity_enums:
            model_enums.update(cls.get_model_enums_from_value(value=entity_enum_value))

        model_enums = list(model_enums)

        if is_sorted:
            model_enums = sorted(model_enums, key=lambda value: value.order_number)

        return model_enums


class AbstractCollectDataCommandProgress(ReprStrPreModelMixin, BaseObjectModel):
    """
    Модель, хранящая данные для формирования и отслеживания асинхронных задач по сбору данных.

    В реализации необходимо определить поля:
        1. Ссылку на асинхронную задачу, например:
            task = ForeignKey(
                to=RunningTask,
                verbose_name='Асинхронная задача',
                blank=True, null=True,
                on_delete=SET_NULL,
            )
        2. Поле хранения лога:
            logs_link = FileField(
                upload_to=upload_file_handler,
                max_length=255,
                verbose_name='Ссылка на файл логов',
            )
    """

    task = ...

    logs_link = ...

    stage = ForeignKey(
        to=CollectingExportedDataStage,
        verbose_name='Этап формирования данных для выгрузки',
        blank=True,
        null=True,
        on_delete=SET_NULL,
    )
    model = ForeignKey(
        to=RegionalDataMartModelEnum,
        verbose_name='Модель РВД',
        on_delete=PROTECT,
    )
    created = DateTimeField(
        verbose_name='Дата создания',
        default=timezone.now,
    )
    logs_period_started_at = DateTimeField(
        'Левая граница периода обрабатываемых логов',
    )
    logs_period_ended_at = DateTimeField(
        'Правая граница периода обрабатываемых логов',
    )
    generation_id = UUIDField(
        'Идентификатор генерации',
        default=uuid.uuid4,
    )
    institute_ids = JSONField(
        'id учебного заведения',
        blank=True,
        null=True,
        default=list,
    )

    class Meta:
        abstract = True
        db_table = 'rdm_collecting_data_command_progress'
        verbose_name = 'Задача по сбору данных'
        verbose_name_plural = 'Задачи по сбору данных'


class AbstractExportDataCommandProgress(ReprStrPreModelMixin, BaseObjectModel):
    """Команда экспорта данных."""

    task = ...

    logs_link = ...

    stage = ForeignKey(
        to=ExportingDataStage,
        verbose_name='Этап выгрузки данных',
        null=True,
        blank=True,
        on_delete=SET_NULL,
    )
    entity = ForeignKey(
        to=RegionalDataMartEntityEnum,
        verbose_name='Сущность РВД',
        on_delete=PROTECT,
    )
    created = DateTimeField(
        verbose_name='Дата создания',
        default=timezone.now,
    )
    period_started_at = DateTimeField(
        'Левая граница периода выборки данных для выгрузки',
    )
    period_ended_at = DateTimeField(
        'Правая граница периода выборки данных для выгрузки',
    )
    generation_id = UUIDField(
        'Идентификатор генерации',
        default=uuid.uuid4,
    )

    class Meta:
        abstract = True
        db_table = 'rdm_exporting_data_command_progress'
        verbose_name = 'Команда экспорта данных'
        verbose_name_plural = 'Команды экспорта данных'


class UploaderClientLog(Entry):
    """Прокси модель Загрузчика данных в витрину."""

    objects = UploaderClientLogManager()
    base_objects = Manager()

    @cached_property
    def http_method_and_url(self) -> tuple[str, str]:
        """Возвращает http-метод и url из поля запроса Entry.request."""
        request = StringIO(self.request)
        request_first_line = request.readline()
        request.close()

        method, url = request_first_line.split(' ')[:2]
        if not (method and url.startswith('http')):
            method = url = ''

        return method.strip('[]'), url

    @cached_property
    def http_response_status(self) -> Optional[str]:
        """Статус-код запроса к витрине."""
        try:
            http_status = self.response.split(' ')[0].strip('[]')

            if not http_status:
                return None

            if 200 <= int(http_status) < 300:
                http_status = 'Успех'
            elif int(http_status) >= 400:
                http_status = 'Ошибка'
        except (IndexError, AttributeError):
            http_status = None

        return http_status

    @property
    def http_method(self) -> str:
        """Значение http-метода."""
        return self.http_method_and_url[0]

    @property
    def request_url(self) -> str:
        """URL запроса."""
        return self.http_method_and_url[1]

    @property
    def request_error(self) -> Optional[str]:
        """Ошибка запроса."""
        return self.error

    @property
    def result_status_display(self) -> str:
        """Результат запроса."""
        result_status = getattr(self, 'result_status', RequestResultStatus.ERROR)

        return RequestResultStatus.values.get(result_status) or RequestResultStatus.values[RequestResultStatus.ERROR]

    class Meta:
        proxy = True


class TransferredEntity(BaseObjectModel):
    """Сущность, по которой должен быть произведен сбор и экспорт данных."""

    entity = OneToOneField(
        to=RegionalDataMartEntityEnum,
        verbose_name='Сущность',
        on_delete=CASCADE,
    )
    export_enabled = BooleanField(
        verbose_name='Включение экспорта для сущности',
        default=True,
    )
    queue_level = PositiveIntegerField(
        choices=EntityLevelQueueTypeEnum.get_choices(),
        default=EntityLevelQueueTypeEnum.BASE,
        verbose_name='Уровень очереди',
    )

    class Meta:
        db_table = 'rdm_transferred_entity'
        verbose_name = 'Сущность, по которой должен быть произведен сбор и экспорт данных'
        verbose_name_plural = 'Сущности, по которым должен быть произведен сбор и экспорт данных'

    @json_encode
    def no_export(self):
        """Формирует отображение признака отключения экспорта."""
        return 'Нет' if self.export_enabled else 'Да'


class ExportingDataSubStageEntity(BaseObjectModel):
    """Модель связи сущности и подэтапа выгрузки."""

    entity = ForeignKey(
        to=RegionalDataMartEntityEnum,
        verbose_name='Сущность РВД',
        on_delete=PROTECT,
    )

    exporting_data_sub_stage = ForeignKey(
        to=ExportingDataSubStage,
        verbose_name='Подэтап выгрузки данных',
        on_delete=CASCADE,
    )

    class Meta:
        db_table = 'rdm_exporting_data_sub_stage_entity'
        verbose_name = 'Связь сущности и подэтапа выгрузки'
        verbose_name_plural = 'Связи сущности и подэтапа выгрузки'
