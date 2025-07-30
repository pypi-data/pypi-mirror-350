from datetime import (
    date,
    datetime,
    time,
    timedelta,
)

from django.conf import (
    settings,
)
from django.db.models import (
    OuterRef,
    Subquery,
    Value,
)
from django.db.models.functions import (
    Coalesce,
)
from django.db.transaction import (
    atomic,
)

from educommon import (
    logger,
)

from edu_rdm_integration.models import (
    ExportingDataStage,
    ExportingDataStageStatus,
    ExportingDataSubStage,
    ExportingDataSubStageStatus,
)


@atomic
def set_failed_status_suspended_exporting_data_stages() -> dict[str, int]:
    """Установить статус 'Завершено с ошибками' для зависших этапов и подэтапов экспорта.

    Экспорт считается зависшим в случае если за определенное в параметре RDM_CHECK_SUSPEND_TASK_STAGE_TIMEOUT время,
    отсутствуют изменения в связанных подэтапах. Параметр RDM_CHECK_SUSPEND_TASK_STAGE_TIMEOUT определяется
    в настройках приложения.
    """
    changed_status_result = {
        'change_stage_count': 0,
        'change_sub_stage_count': 0,
    }

    current_datetime = datetime.now()
    suspended_time_at = current_datetime - timedelta(minutes=settings.RDM_CHECK_SUSPEND_TASK_STAGE_TIMEOUT)

    suspended_stage_ids = set(
        ExportingDataStage.objects.annotate(
            last_sub_stage_started_at=Coalesce(
                Subquery(
                    ExportingDataSubStage.objects.filter(
                        stage_id=OuterRef('pk')
                    ).values('started_at').order_by('-started_at')[:1]
                ),
                Value(datetime.combine(date.min, time.min))
            )
        ).filter(
            last_sub_stage_started_at__lt=suspended_time_at,
            status__in=(
                ExportingDataStageStatus.CREATED.key,
                ExportingDataStageStatus.IN_PROGRESS.key,
            ),
        ).values_list('pk', flat=True)
    )

    if suspended_stage_ids:
        logger.info(f'find suspended ExportingDataStage: {", ".join(map(str, suspended_stage_ids))}..')

        change_stage_count = ExportingDataStage.objects.filter(
            pk__in=suspended_stage_ids,
        ).update(
            status=ExportingDataStageStatus.FAILED.key,
            ended_at=current_datetime,
        )

        change_sub_stage_count = ExportingDataSubStage.objects.filter(
            stage_id__in=suspended_stage_ids,
        ).update(
            status=ExportingDataSubStageStatus.FAILED.key,
            ended_at=current_datetime,
        )

        changed_status_result.update({
            'change_stage_count': change_stage_count,
            'change_sub_stage_count': change_sub_stage_count,
        })

    return changed_status_result
