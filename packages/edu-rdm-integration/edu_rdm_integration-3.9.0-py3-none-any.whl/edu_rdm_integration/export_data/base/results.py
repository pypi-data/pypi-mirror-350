from edu_rdm_integration.adapters.results import (
    WebEduFunctionResult,
    WebEduRunnerResult,
)


class BaseExportDataRunnerResult(WebEduRunnerResult):
    """
    Базовый класс результатов работы ранеров функций выгрузки данных для интеграции с "Региональная витрина данных".
    """


class BaseExportDataFunctionResult(WebEduFunctionResult):
    """
    Базовый класс результатов работы функций выгрузки данных для интеграции с "Региональная витрина данных".
    """
