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

from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response

from project_task.celery_task.judge_objective import judge_objective

from .constants import STATUS
from .models import ProjectTask, StudentProjectTaskInfo
from .serializer import (
    ProjectTaskDetailForTeacherSerializer,
    StudentPerformTaskSerializer,
    StudentProjectTaskInfoForStuSerializer,
    StudentProjectTaskInfoSerializer,
    TeacherJudgeSerializer,
)


# 答题和判卷的视图集
class PerformAndJudgeViewSet(viewsets.ViewSet):
    queryset = StudentProjectTaskInfo.objects.all()
    serializer_class = StudentPerformTaskSerializer

    @swagger_auto_schema(
        operation_summary="老师获取所有该项目下的任务",
    )
    def get_all_task(self, request, *args, **kwargs):
        project_id = kwargs["project_id"]
        task_id_list = list(
            StudentProjectTaskInfo.objects.filter(project_id=project_id).values_list(
                "project_task_id", flat=True
            )
        )
        tasks = ProjectTask.objects.filter(id__in=task_id_list)
        task_info = ProjectTaskDetailForTeacherSerializer(tasks, many=True)
        return Response(task_info.data)

    @swagger_auto_schema(
        operation_summary="老师获取指定学生关系表",
    )
    def get_stu_info(self, request, *args, **kwargs):
        task_id = kwargs["project_task_id"]
        stu_id = kwargs["student_id"]
        try:
            data = StudentProjectTaskInfo.objects.get(
                Q(project_task_id=task_id),
                Q(student_id=stu_id),
                Q(status=STATUS.SUBMITTED) | Q(status=STATUS.MARKED),
            )
        except StudentProjectTaskInfo.DoesNotExist:
            return Response("当前学生还未提交!!!", exception=True)

        serializer = StudentProjectTaskInfoSerializer(data)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="获取学生的关系表(只能获取自己的)",
    )
    def get_individual_info(self, request, *args, **kwargs):
        project_task_id = kwargs["project_task_id"]
        try:
            relation_info = StudentProjectTaskInfo.objects.get(
                project_task_id=project_task_id, student_id=request.user.id
            )
        except StudentProjectTaskInfo.DoesNotExist:
            return Response("查找的关系表不存在!", exception=True)

        task = ProjectTask.objects.get(id=relation_info.project_task_id)

        # 老师评分学生是否可见
        if not task.students_visible:
            serializer = StudentProjectTaskInfoForStuSerializer(relation_info)
        else:
            serializer = StudentProjectTaskInfoSerializer(relation_info)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=StudentPerformTaskSerializer,
        operation_summary="学生答题以及提交",
    )
    def perform_task(self, request, *args, **kwargs):
        project_task_id = kwargs["project_task_id"]
        try:
            relation_info = StudentProjectTaskInfo.objects.get(
                project_task_id=project_task_id, student_id=request.user.id
            )
        except StudentProjectTaskInfo.DoesNotExist:
            return Response("查找的关系表不存在!", exception=True)

        request.data["updater_id"] = request.user.id
        request.data["updater"] = request.user.username

        data = request.data

        # 更改状态 已保存 ----> 已提交
        if data["status"] == STATUS.SUBMITTED:
            if relation_info.status == STATUS.SAVED:
                temp = StudentPerformTaskSerializer(relation_info, data)
                temp.is_valid(raise_exception=True)
                temp.save()
                return Response()
            else:
                return Response("请先保存再提交!!!", exception=True)

        perform_info = StudentPerformTaskSerializer(relation_info, data)
        perform_info.is_valid(raise_exception=True)
        perform_info.save()

        # celery ----> 客观题评分
        judge_objective.delay(relation_info.id)

        return Response()

    @swagger_auto_schema(
        request_body=TeacherJudgeSerializer,
        operation_summary="老师判卷",
    )
    def judge_task(self, request, *args, **kwargs):
        project_task_id = kwargs["project_task_id"]
        student_id = kwargs["student_id"]

        request.data["updater_id"] = request.user.id
        request.data["updater"] = request.user.username
        data = request.data

        relation_info = StudentProjectTaskInfo.objects.get(
            project_task_id=project_task_id,
            student_id=student_id,
        )

        individual_score = relation_info.individual_score

        for item in individual_score:
            if item["teacher_id"] == request.user.id:
                item["teacher_name"] = request.user.username
                item["score"] = data["score_list"]
                item["is_judge"] = True
                break

        if all(item["is_judge"] for item in individual_score):
            total_score = 0.0
            for item in individual_score:
                total_score += sum(item["score"]) * item["teacher_weight"]

            judge_info = {
                "status": STATUS.MARKED,
                "total_score": total_score,
                "individual_score": individual_score,
                "updater_id": request.user.id,
            }
        else:
            judge_info = {
                "individual_score": individual_score,
                "updater_id": request.user.id,
            }

        ret = StudentPerformTaskSerializer(relation_info, judge_info)
        ret.is_valid(raise_exception=True)
        ret.save()

        return Response()
