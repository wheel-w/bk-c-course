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
# Create your views here.
# from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.response import Response

from project_task.models import ProjectTask
from project_task.pagination import ProjectTaskPagination
from project_task.serilizer import (
    ProjectTaskSerializer,
    StudentProjectTaskInfoSerializer,
    TaskCreateSerializer,
)
from question.serializer import QuestionSerializer


class ProjectTaskList(generics.ListCreateAPIView):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer
    pagination_class = ProjectTaskPagination

    @swagger_auto_schema(
        operation_summary="创建项目任务,和其对应的题目与关系表",
        request_body=TaskCreateSerializer,
        # responses=ProjectTaskSerializer
    )
    def post(self, request, *args, **kwargs):
        question_data = request.data.pop("questions")
        student_data = request.data.pop("students")
        # 创建任务
        request.data["creator"] = request.user.username
        request.data["updater"] = request.user.username
        task = ProjectTaskSerializer(data=request.data)
        task.is_valid(raise_exception=True)
        task_temp = task.save()

        # question生成
        questions = QuestionSerializer(data=question_data, many=True)
        questions.is_valid(raise_exception=True)

        questions_order = ""
        comma_flag = True
        for i in questions.save():
            if comma_flag:
                questions_order += f"{i.id}"
                comma_flag = False
                continue
            questions_order += f",{i.id}"

        # question列表进入task_temp
        task = ProjectTaskSerializer(
            instance=task_temp, data={"questions_order": questions_order}, partial=True
        )
        task.is_valid(raise_exception=True)
        task_temp = task.save()

        # 创建关系表
        relation = []
        for i in student_data:
            temp = {
                "student_id": i,
                "project_id": request.data.get("project_id"),
                "project_task_id": task_temp.id,
                "created_id": request.user.id,
                "updated_id": request.user.id,
            }
            relation.append(temp)
        taskinfo = StudentProjectTaskInfoSerializer(data=relation, many=True)
        taskinfo.is_valid(raise_exception=True)
        taskinfo.save()

        headers = self.get_success_headers(task.data)
        return Response(task.data, status=status.HTTP_201_CREATED, headers=headers)
