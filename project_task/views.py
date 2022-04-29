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
from django.db import transaction

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response

from project_task.models import ProjectTask, StudentProjectTaskInfo
from project_task.serializer import (
    ProjectTaskDetailForStuHasNotSubmitSerializer,
    ProjectTaskDetailForStuHasSubmitSerializer,
    ProjectTaskSerializer,
    StudentProjectTaskInfoSerializer,
    TaskCreateSerializer,
)
from question.serializer import QuestionSerializer


class ProjectTaskList(generics.ListCreateAPIView):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer

    @swagger_auto_schema(
        operation_summary="获取学生的任务",
    )
    def get(self, request, *args, **kwargs):
        student_id = request.user.id
        task_id_list = list(
            StudentProjectTaskInfo.objects.filter(student_id=student_id).values_list(
                "project_task_id", flat=True
            )
        )
        task_info = list(ProjectTask.objects.filter(id__in=task_id_list))

        data = []
        relation_info = list(
            StudentProjectTaskInfo.objects.filter(
                student_id=student_id, project_task_id__in=task_id_list
            )
        )

        for relation, task in zip(relation_info, task_info):
            if relation.status == StudentProjectTaskInfo.Status.MARKED:
                serializer = ProjectTaskDetailForStuHasSubmitSerializer(task)
            else:
                serializer = ProjectTaskDetailForStuHasNotSubmitSerializer(task)
            data.append(serializer.data)

        return Response(data)

    @swagger_auto_schema(
        operation_summary="创建项目任务,和其对应的题目与关系表", request_body=TaskCreateSerializer
    )
    def post(self, request, *args, **kwargs):
        request.data["creator"] = request.user.username
        request.data["creator_id"] = request.user.id

        temp = TaskCreateSerializer(data=request.data)
        temp.is_valid(raise_exception=True)

        data = temp.validated_data
        # 构建参数
        questions_id_order_scores = data.pop("questions_id_order_scores")
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

            questions_info = {}
            try:
                for i in range(len(questions_id_list)):
                    questions_temp = {
                        questions_id_list[i].id: questions_id_order_scores[i]
                    }
                    questions_info.update(questions_temp)
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

        transaction.savepoint_commit(save)

        task = ProjectTaskSerializer(instance=task_temp)

        headers = self.get_success_headers(task.data)
        return Response(task.data, status=status.HTTP_201_CREATED, headers=headers)
