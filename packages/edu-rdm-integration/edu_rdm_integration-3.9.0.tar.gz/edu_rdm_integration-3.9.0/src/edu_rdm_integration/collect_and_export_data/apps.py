from django.apps import (
    AppConfig as AppConfigBase,
)


class AppConfig(AppConfigBase):

    name = __package__
    label = 'rdm_collect_and_export_data'
