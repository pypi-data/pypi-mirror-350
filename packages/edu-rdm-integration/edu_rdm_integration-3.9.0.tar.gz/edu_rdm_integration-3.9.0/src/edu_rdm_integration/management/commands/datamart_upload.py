from pathlib import (
    Path,
)

from edu_rdm_integration.export_data.base.requests import (
    RegionalDataMartEntityRequest,
)
from edu_rdm_integration.management.general import (
    BaseDatamartClientCommand,
)


class Command(BaseDatamartClientCommand):

    help = 'Команда для загрузки csv-файла в РВД с использованием uploader-client.'  # noqa A003

    def add_arguments(self, parser):
        """Добавление параметров."""
        super().add_arguments(parser)

        parser.add_argument(
            '--table_name',
            type=str,
            required=True,
            help='название таблицы внутри витрины данных',
        )
        parser.add_argument(
            '--file_path',
            type=str,
            required=True,
            help='путь до csv-файла с данными',
        )

    def _get_request(self, **options):
        """Возвращает запрос для отправки в РВД."""
        request = RegionalDataMartEntityRequest(
            datamart_name=options['datamart_mnemonic'],
            table_name=options['table_name'],
            method='POST',
            operation='upload',
            parameters={},
            headers={
                'Content-Type': 'text/csv',
            },
            files=[],
            data=Path(options['file_path']).open('rb').read(),
        )

        return request
