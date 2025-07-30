from edu_rdm_integration.adapters.validators import (
    WebEduFunctionValidator,
    WebEduRunnerValidator,
)


class BaseCollectingCalculatedExportedDataRunnerValidator(WebEduRunnerValidator):
    """
    Базовый класс валидаторов ранеров функций сбора расчетных данных для интеграции с "Региональная витрина данных".
    """

    def validate(self, runnable):
        """
        Расширение метода валидации.
        """
        super().validate(runnable=runnable)


class BaseCollectingCalculatedExportedDataFunctionValidator(WebEduFunctionValidator):
    """
    Базовый класс валидаторов функций сбора расчетных данных для интеграции с "Региональная витрина данных".
    """

    def validate(self, runnable):
        """
        Расширение метода валидации.
        """
        super().validate(runnable=runnable)
