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
    CollectingDataStageStatus,
    CollectingDataSubStageStatus,
    CollectingExportedDataStage,
    CollectingExportedDataSubStage,
)


@atomic
def set_failed_status_suspended_collecting_data_stages() -> dict[str, int]:
    """Установить статус 'Завершено с ошибками' для зависших этапов и подэтапов сбора.

    Сборка считается зависшей в случае если за определенное в параметре RDM_CHECK_SUSPEND_TASK_STAGE_TIMEOUT время,
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
        CollectingExportedDataStage.objects.annotate(
            last_sub_stage_started_at=Coalesce(
                Subquery(
                    CollectingExportedDataSubStage.objects.filter(
                        stage_id=OuterRef('pk')
                    ).values('started_at').order_by('-started_at')[:1]
                ),
                Value(datetime.combine(date.min, time.min))
            )
        ).filter(
            last_sub_stage_started_at__lt=suspended_time_at,
            status__in=(
                CollectingDataStageStatus.CREATED.key,
                CollectingDataStageStatus.IN_PROGRESS.key,
            ),
        ).values_list('pk', flat=True)
    )

    if suspended_stage_ids:
        logger.info(f'find suspended CollectingExportedDataStage: {", ".join(map(str, suspended_stage_ids))}..')

        change_stage_count = CollectingExportedDataStage.objects.filter(
            pk__in=suspended_stage_ids,
        ).update(
            status=CollectingDataStageStatus.FAILED.key,
            ended_at=current_datetime,
        )

        change_sub_stage_count = CollectingExportedDataSubStage.objects.filter(
            stage_id__in=suspended_stage_ids,
        ).update(
            status=CollectingDataSubStageStatus.FAILED.key,
            ended_at=current_datetime,
        )

        changed_status_result.update({
            'change_stage_count': change_stage_count,
            'change_sub_stage_count': change_sub_stage_count,
        })

    return changed_status_result
