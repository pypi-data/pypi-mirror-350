from django.apps import (
    AppConfig,
)


class UploaderLoggerConfig(AppConfig):  # noqa D101

    name = 'regional_data_mart_integration.uploader_log'
    label = 'regional_data_mart_integration_uploader_log'
    verbose_name = 'Журнал логов РВД'
