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
from project_task.serilizer import ProjectTaskSerializer, TaskCreateSerializer


class ProjectTaskList(generics.ListCreateAPIView):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer

    @swagger_auto_schema(
        operation_summary="创建项目任务,和其对应的题目与关系表", request_body=TaskCreateSerializer
    )
    def post(self, request, *args, **kwargs):
        request.data["creator"] = request.user.username
        request.data["creator_id"] = request.user.id

        temp = TaskCreateSerializer(data=request.data)
        temp.is_valid(raise_exception=True)
        task = ProjectTaskSerializer(instance=temp.save())

        headers = self.get_success_headers(task.data)
        return Response(task.data, status=status.HTTP_201_CREATED, headers=headers)
