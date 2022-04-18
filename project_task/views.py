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
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from project_task.models import ProjectTask, StudentProjectTaskInfo
from project_task.serilizer import (
    ProjectSearchInfoSerializer,
    ProjectTaskSerializer,
    StudentProjectTaskInfoSerializer,
)


class ProjectTaskPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 30


class ProjectTaskList(generics.ListCreateAPIView):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer
    pagination_class = ProjectTaskPagination

    @swagger_auto_schema(
        operation_summary="创建项目任务",
    )
    def post(self, request, *args, **kwargs):
        request.data["creator"] = request.user.username
        request.data["updater"] = request.user.username
        return super().create(request, *args, **kwargs)


class ProjectTaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectTask.objects.all()
    serializer_class = ProjectTaskSerializer

    @swagger_auto_schema(
        operation_summary="更新项目任务",
    )
    def put(self, request, *args, **kwargs):
        request.data["updater"] = request.user.username
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="更新部分项目任务",
    )
    def patch(self, request, *args, **kwargs):
        request.data["updater"] = request.user.username
        return super().patch(request, *args, **kwargs)


class StudentProjectTaskInfoCreate(generics.CreateAPIView):
    queryset = StudentProjectTaskInfo.objects.all()
    serializer_class = StudentProjectTaskInfoSerializer

    @swagger_auto_schema(
        operation_summary="创建项目任务关系表",
    )
    def post(self, request, *args, **kwargs):
        request.data["creator"] = request.user.username
        request.data["updater"] = request.user.username
        return super().post(request, *args, **kwargs)


class StudentProjectTaskInfoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = StudentProjectTaskInfo.objects.all()
    serializer_class = StudentProjectTaskInfoSerializer
    lookup_field = "project_id"

    # lookup_url_kwarg =

    @swagger_auto_schema(
        operation_summary="修改项目任务关系表",
    )
    def get(self, request, *args, **kwargs):
        a = self.get_object()
        print(a.cumulative_time)
        return super().retrieve(self, request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        request.data["updater"] = request.user.username
        # request.data["cumulative_time"] = StudentProjectTaskInfo.objects.filter(project_id=project_id)
        return self.update(request, *args, **kwargs)


class ProjectSearchInfoList(generics.ListAPIView):
    queryset = StudentProjectTaskInfo.objects.all()
    serializer_class = ProjectSearchInfoSerializer
    pagination_class = ProjectTaskPagination

    @swagger_auto_schema(
        operation_summary="根据项目搜索关系表",
    )
    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(project_id=kwargs["project_id"])
        return super().list(self, request, *args, **kwargs)


class TaskSearchInfoList(generics.ListAPIView):
    queryset = StudentProjectTaskInfo.objects.all()
    serializer_class = ProjectSearchInfoSerializer
    pagination_class = ProjectTaskPagination

    @swagger_auto_schema(
        operation_summary="根据任务搜索关系表",
    )
    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(project_task_id=kwargs["project_task_id"])
        return super().list(self, request, *args, **kwargs)


class StudentSearchInfoList(generics.ListAPIView):
    queryset = StudentProjectTaskInfo.objects.all()
    serializer_class = ProjectSearchInfoSerializer
    pagination_class = ProjectTaskPagination

    @swagger_auto_schema(
        operation_summary="根据学生搜索关系表",
    )
    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(student_id=kwargs["student_id"])
        return super().list(self, request, *args, **kwargs)
