import logging

from celery.task import task

from project_task.constants import CELERY_TASK_TYPE, TASK_STATUS
from project_task.models import CeleryTaskInfo, ProjectTask

logger = logging.getLogger("root")


# 定时发布
@task()
def scheduled_publish(project_task_id):
    logger.info(f"id为{project_task_id}的任务的定时发布异步任务开始执行")
    try:
        ProjectTask.objects.filter(id=project_task_id).update(
            status=TASK_STATUS.RELEASE
        )
    except ProjectTask.DoesNotExist as error:
        logger.exception(error)

    try:
        CeleryTaskInfo.objects.get(
            project_task_id=project_task_id,
            celery_task_type=CELERY_TASK_TYPE.SCHEDULED_PUBLISH,
        ).delete()
    except CeleryTaskInfo.DoesNotExist as error:
        logger.exception(error)

    logger.info(f"id为{project_task_id}的任务的定时发布异步任务执行完毕")
