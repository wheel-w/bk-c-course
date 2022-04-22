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
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from project_task.models import ProjectTask
from project_task.serilizer import (
    ProjectTaskSerializer,
    StudentProjectTaskInfoSerializer,
    TaskCreateSerializer,
)
from question.serializer import QuestionSerializer


class ProjectTaskList(generics.ListCreateAPIView):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer

    @swagger_auto_schema(
        operation_summary="创建项目任务,和其对应的题目与关系表", request_body=TaskCreateSerializer
    )
    def post(self, request, *args, **kwargs):
        question_data = request.data.pop("questions")
        student_data = request.data.pop("students")

        with transaction.atomic():
            # 创建事务保存点
            save_id = transaction.savepoint()

            # question生成
            for i in range(len(question_data)):
                question_data[i]["project_id"] = request.data["project_id"]
            questions = QuestionSerializer(data=question_data, many=True)

            try:
                questions.is_valid(raise_exception=True)
                questions_id_list = questions.save()
            except ValidationError as e:
                return Response(e.detail, exception=True)

            # 创建任务并写入数据库
            request.data["creator"] = request.user.username
            request.data["updater"] = request.user.username

            order_scores = request.data.pop("questions_order_scores")
            questions_id_order_scores = []

            try:
                for i in range(len(questions_id_list)):
                    questions_temp = {questions_id_list[i].id: order_scores[i]}
                    questions_id_order_scores.append(questions_temp)
            except IndexError:
                return Response("答案与答案分数个数不匹配", exception=True)

            request.data["questions_id_order_scores"] = questions_id_order_scores
            task = ProjectTaskSerializer(data=request.data)

            try:
                task.is_valid(raise_exception=True)
                task_temp = task.save()
            except ValidationError as e:
                return Response(e.detail, exception=True)

            # 创建关系表
            relation = []
            for i in student_data:
                temp = {
                    "student_id": i,
                    "project_id": request.data.get("project_id"),
                    "project_task_id": task_temp.id,
                    "creator_id": request.user.id,
                    "updator_id": request.user.id,
                }
                relation.append(temp)
            taskinfo = StudentProjectTaskInfoSerializer(data=relation, many=True)

            try:
                taskinfo.is_valid(raise_exception=True)
                taskinfo.save()
            except ValidationError as e:
                return Response(e.detail, exception=True)

        transaction.savepoint_commit(save_id)

        headers = self.get_success_headers(task.data)
        return Response(task.data, status=status.HTTP_201_CREATED, headers=headers)
