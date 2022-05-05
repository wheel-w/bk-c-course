"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版（BLUEKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. ALL rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MII
Unless required by applicable Law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific Language governing permissions and limitations under the License.
"""

import logging

from celery.task import task

from project_task.constants import CELERY_TASK_TYPE, STATUS
from project_task.models import CeleryTaskInfo, StudentProjectTaskInfo

logger = logging.getLogger("root")


# 任务截止时把所有已保存的relation自动提交
@task()
def auto_submit(project_task_id):
    logger.info("自动提交任务开始执行")

    StudentProjectTaskInfo.objects.filter(
        project_task_id=project_task_id,
        status=STATUS.SAVED,
    ).update(status=STATUS.SUBMITTED)

    try:
        CeleryTaskInfo.objects.get(
            project_task_id=project_task_id,
            celery_task_type=CELERY_TASK_TYPE.AUTO_SUBMIT,
        ).delete()
    except CeleryTaskInfo.DoesNotExist as error:
        logger.exception(error)

    logger.info("自动提交任务执行完毕")
