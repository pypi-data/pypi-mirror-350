import logging
from abc import (
    ABC,
    abstractmethod,
)
from collections import (
    defaultdict,
)
from typing import (
    Optional,
)

from django.db.models import (
    Q,
)

from m3_db_utils.consts import (
    DEFAULT_ORDER_NUMBER,
)

from edu_rdm_integration.consts import (
    REGIONAL_DATA_MART_INTEGRATION_COLLECTING_DATA,
    REGIONAL_DATA_MART_INTEGRATION_EXPORTING_DATA,
)
from edu_rdm_integration.helpers import (
    UploadStatusHelper,
    get_collecting_managers_max_period_ended_dates,
    get_exporting_managers_max_period_ended_dates,
    save_command_log_link,
)
from edu_rdm_integration.models import (
    ExportingDataSubStageUploaderClientLog,
    RegionalDataMartEntityEnum,
    TransferredEntity,
)
from edu_rdm_integration.storages import (
    RegionalDataMartEntityStorage,
)


class BaseOperationData(ABC):
    """Базовый класс операций с данными."""

    def __init__(self, **kwargs):
        # Идентификатор команды для передачи сигналу manager_created
        self.command_id: Optional[int] = kwargs.get('command_id')

        self._file_handler: Optional[logging.FileHandler] = None

        self._add_file_handler()

    @property
    @abstractmethod
    def _log_file_path(self) -> str:
        """Путь до лог файла."""

    def _add_file_handler(self) -> None:
        """Добавляет обработчик логов."""
        if self.command_id:
            self._file_handler = logging.FileHandler(self._log_file_path)

            logging.getLogger('info_logger').addHandler(self._file_handler)
            logging.getLogger('exception_logger').addHandler(self._file_handler)

    def _remove_file_handler(self) -> None:
        """Удаляет обработчик логов."""
        if self._file_handler:
            logging.getLogger('info_logger').removeHandler(self._file_handler)
            logging.getLogger('exception_logger').removeHandler(self._file_handler)

            self._file_handler.close()


class BaseTransferLatestEntitiesDataMixin:
    """Миксин сбора и выгрузки данных."""

    def __init__(self) -> None:
        super().__init__()

        self._collecting_data_managers: dict[str, type['RunnerManager']] = {}
        self._collecting_data_manager_to_logs_period_end: dict[str, 'datetime'] = {}

        self._exporting_data_managers: dict[str, type['RunnerManager']] = {}
        self._exporting_data_manager_to_period_end: dict[str, 'datetime'] = {}

        self._transferred_entities = []
        self._entites_models_map = defaultdict(list)

    def get_entity_qs(self) -> 'QuerySet[TransferredEntity]':
        """Возвращает сущностей сбора и выгрузки."""
        raise NotImplementedError

    def _collect_transferred_entities(self) -> None:
        """Собирает сущности РВД, по которым будет произведен сбор и экспорт данных."""

        self._transferred_entities = [
            (RegionalDataMartEntityEnum.get_model_enum_value(key=entity), export_enabled)
            for entity, export_enabled in self.get_entity_qs().values_list('entity', 'export_enabled')
        ]

        # Собираем словарь по сущностям с моделями для сборки
        for entity, _ in self._transferred_entities:
            self._entites_models_map[entity.key].extend(
                (model_enum for model_enum in (*entity.additional_model_enums, entity.main_model_enum)
                 if model_enum.order_number != DEFAULT_ORDER_NUMBER)
            )

    def _collect_managers(self) -> None:
        """Собирает менеджеры Функций для сбора и выгрузки данных."""
        entity_storage = RegionalDataMartEntityStorage()
        entity_storage.prepare()

        collecting_models_data_managers_map = entity_storage.prepare_entities_manager_map(
            tags={REGIONAL_DATA_MART_INTEGRATION_COLLECTING_DATA},
        )
        exporting_entities_data_managers_map = entity_storage.prepare_entities_manager_map(
            tags={REGIONAL_DATA_MART_INTEGRATION_EXPORTING_DATA},
        )

        for entity_key, entity_models in self._entites_models_map.items():
            for entity_model in entity_models:
                collect_manager_class = collecting_models_data_managers_map.get(entity_model.key)
                if collect_manager_class:
                    self._collecting_data_managers[entity_model.key] = collect_manager_class

            export_manager_class = exporting_entities_data_managers_map.get(entity_key)
            if export_manager_class:
                self._exporting_data_managers[entity_key] = export_manager_class

    def _calculate_collecting_managers_logs_period_ended_at(self) -> None:
        """Определяет дату последнего успешного этапа сбора у менеджеров Функций сбора."""
        self._collecting_data_manager_to_logs_period_end = get_collecting_managers_max_period_ended_dates(
            self._collecting_data_managers.values()
        )

    def _calculate_exporting_managers_ended_at(self) -> None:
        """Определяет дату последнего успешного подэтапа экспорта у менеджеров Функций экспорта."""
        self._exporting_data_manager_to_period_end = get_exporting_managers_max_period_ended_dates(
            self._exporting_data_managers.values()
        )

    def prepare_collect_export_managers(self) -> None:
        """Подготовка менджеров сбора и экспорта."""
        self._collect_transferred_entities()
        self._collect_managers()
        self._calculate_collecting_managers_logs_period_ended_at()
        self._calculate_exporting_managers_ended_at()
