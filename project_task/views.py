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
import datetime

from celery.result import AsyncResult
from django.db import transaction

# Create your views here.
from django.utils.timezone import utc
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from project_task.constants import CELERY_TASK_TYPE
from project_task.models import CeleryTaskInfo, ProjectTask, StudentProjectTaskInfo
from project_task.serializer import (
    CeleryTaskInfoCreateSerializer,
    ProjectTaskSerializer,
    ProjectTaskUpdateSerializer,
    StudentProjectTaskInfoSerializer,
    TaskCreateSerializer,
    TaskDeleteSerializer,
    TimeTransferSerializer,
)
from question.models import Question
from question.serializer import QuestionSerializer

from .celery_task.auto_submit import auto_submit
from .celery_task.scheduled_publish import scheduled_publish


# 出题接口
class ProjectTaskList(viewsets.ViewSet):
    """任务管理"""

    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer

    @swagger_auto_schema(
        operation_summary="创建项目任务,和其对应的题目与关系表", request_body=TaskCreateSerializer
    )
    def create_task(self, request, *args, **kwargs):
        request.data["creator"] = request.user.username
        request.data["creator_id"] = request.user.id

        temp = TaskCreateSerializer(data=request.data)
        temp.is_valid(raise_exception=True)

        data = temp.validated_data
        # 构建参数
        questions_detail = data.pop("questions_detail")
        questions_detail = sorted(
            questions_detail, key=lambda question: question["index"]
        )
        questions_temp = data.pop("questions")

        project_id = data["project_id"]
        id = data.pop("creator_id")

        data["updater"] = data["creator"]
        with transaction.atomic():
            save = transaction.savepoint()
            # 生成question
            # 确保问题的项目id何project的项目id一致
            for i in range(len(questions_temp)):
                questions_temp[i]["project_id"] = project_id
            questions = QuestionSerializer(data=questions_temp, many=True)
            questions.is_valid(raise_exception=True)
            questions_id_list = questions.save()

            questions_info = []
            try:
                for i in range(len(questions_id_list)):
                    questions_detail[i]["id"] = questions_id_list[i].id
                    questions_info.append(questions_detail[i])
            except IndexError:
                return Response("答案与答案分数个数不匹配", exception=True)

            data["questions_info"] = questions_info
            task = ProjectTaskSerializer(data=data)
            task.is_valid(raise_exception=True)
            task_temp = task.save()

            relation = []
            for i in data["students"]:
                temp = {
                    "student_id": i,
                    "project_id": data.get("project_id"),
                    "project_task_id": task_temp.id,
                    "creator": request.user.username,
                    "updater": request.user.username,
                    "creator_id": id,
                    "updater_id": id,
                    "stu_answers": [],
                    "individual_score": [],
                }
                relation.append(temp)
            task_info = StudentProjectTaskInfoSerializer(data=relation, many=True)
            task_info.is_valid(raise_exception=True)
            task_info.save()

            # celery ----> 截止时自动提交所有已保存的记录
            auto_submit_task = auto_submit.apply_async(
                args=[task_temp.id], eta=task_temp.end_time
            )

            celery_task_data = {
                "project_task_id": task_temp.id,
                "celery_task_id": auto_submit_task.id,
                "celery_task_type": CELERY_TASK_TYPE.AUTO_SUBMIT,
            }

            celery_task = CeleryTaskInfoCreateSerializer(data=celery_task_data)
            celery_task.is_valid(raise_exception=True)
            celery_task.save()

        transaction.savepoint_commit(save)

        return Response(status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary="更新任务的信息",
        request_body=ProjectTaskUpdateSerializer,
    )
    def update_task(self, request, *args, **kwargs):
        project_task_id = kwargs["project_task_id"]
        try:
            task = ProjectTask.objects.get(id=project_task_id)
        except ProjectTask.DoesNotExist:
            return Response("该任务不存在!!!", exception=True)

        data = request.data

        # 设置定时发布
        if "scheduled_publish_time" in data:
            scheduled_publish_time = data.pop("scheduled_publish_time")
            if datetime.datetime.strptime(
                scheduled_publish_time, "%Y-%m-%dT%H:%M:%S"
            ).replace(tzinfo=utc) < datetime.datetime.now().replace(tzinfo=utc):
                return Response("任务计划发布时间不能早于当前!!!", exception=True)

            time_transfer = TimeTransferSerializer(
                data={"scheduled_publish_time": scheduled_publish_time}
            )
            time_transfer.is_valid(raise_exception=True)
            # 定时发布celery任务
            scheduled_publish_task = scheduled_publish.apply_async(
                args=[project_task_id], eta=time_transfer.data["scheduled_publish_time"]
            )

            celery_task_info = CeleryTaskInfo.objects.filter(
                project_task_id=project_task_id,
                celery_task_type=CELERY_TASK_TYPE.SCHEDULED_PUBLISH,
            )

            if celery_task_info.exists():
                celery_id = celery_task_info[0].celery_task_id
                AsyncResult(celery_id).revoke()
                celery_task_info.update(celery_task_id=scheduled_publish_task.id)
            else:
                celery_task_data = {
                    "project_task_id": project_task_id,
                    "celery_task_id": scheduled_publish_task.id,
                    "celery_task_type": CELERY_TASK_TYPE.SCHEDULED_PUBLISH,
                }
                celery_task = CeleryTaskInfoCreateSerializer(data=celery_task_data)
                celery_task.is_valid(raise_exception=True)
                celery_task.save()

        # questions 和 questions_detail 必须一块传
        if "questions" in data:
            questions = data.pop("questions")
            questions_detail = data.pop("questions_detail")

            questions = QuestionSerializer(data=questions, many=True)
            questions.is_valid(raise_exception=True)
            questions_id_list = questions.save()

            questions_info = []
            try:
                for i in range(len(questions_id_list)):
                    questions_detail[i]["id"] = questions_id_list[i].id
                    questions_info.append(questions_detail[i])
            except IndexError:
                return Response("信息中的答案与答案分数个数不匹配", exception=True)

            data["questions_info"] = questions_info

        if "end_time" in data:
            if datetime.datetime.strptime(
                data["end_time"], "%Y-%m-%dT%H:%M:%S"
            ).replace(tzinfo=utc) < datetime.datetime.now().replace(tzinfo=utc):
                return Response("任务截止时间不能早于当前!!!", exception=True)

        info = ProjectTaskUpdateSerializer(task, data)
        info.is_valid(raise_exception=True)
        task_info = info.save()

        # 如果更改截止时间，更新celery任务id并把原来的任务revoke
        if "end_time" in data:
            auto_submit_task = auto_submit.apply_async(
                args=[task_info.id], eta=task_info.end_time
            )

            celery_task = CeleryTaskInfo.objects.filter(
                project_task_id=project_task_id,
                celery_task_type=CELERY_TASK_TYPE.AUTO_SUBMIT,
            )
            celery_id = celery_task[0].celery_task_id

            AsyncResult(celery_id).revoke()
            celery_task.update(celery_task_id=auto_submit_task.id)

        return Response()

    @swagger_auto_schema(
        operation_summary="删除单个任务",
    )
    def delete_task(self, request, *args, **kwargs):
        project_task_id = kwargs["project_task_id"]
        try:
            task = ProjectTask.objects.get(id=project_task_id)
            question_id_list = [question["id"] for question in task.questions_info]
            task.delete()
            StudentProjectTaskInfo.objects.filter(
                project_task_id=project_task_id
            ).delete()
            Question.objects.filter(id__in=question_id_list).delete()
            # 都删
            celery_task_info = CeleryTaskInfo.objects.filter(
                project_task_id=project_task_id
            )
            if celery_task_info.exists():
                for celery_id in celery_task_info.values_list(
                    "celery_task_id", flat=True
                ):
                    AsyncResult(celery_id).revoke()
                celery_task_info.delete()
        except ProjectTask.DoesNotExist:
            return Response("任务不存在!!!", exception=True)

        return Response("删除成功!")

    @swagger_auto_schema(
        operation_summary="根据传入的任务id列表批量删除任务",
        request_body=TaskDeleteSerializer,
    )
    def bulk_delete_task(self, request, *args, **kwargs):
        task_id_list = request.data["task_id_list"]
        tasks_questions_info = list(
            ProjectTask.objects.filter(id__in=task_id_list).values_list(
                "questions_info", flat=True
            )
        )
        question_id_list = []
        for question_info in tasks_questions_info:
            question_id_list.extend([question["id"] for question in question_info])
        ProjectTask.objects.filter(id__in=task_id_list).delete()
        Question.objects.filter(id__in=question_id_list).delete()
        StudentProjectTaskInfo.objects.filter(project_task_id__in=task_id_list).delete()

        celery_task_info = CeleryTaskInfo.objects.filter(
            project_task_id__in=task_id_list
        )
        # 都删
        if celery_task_info.exists():
            celery_id_list = list(
                celery_task_info.values_list("celery_task_id", flat=True)
            )
            for celery_id in celery_id_list:
                celery_task = AsyncResult(celery_id)
                celery_task.revoke()
            celery_task_info.delete()

        return Response("删除成功!")
