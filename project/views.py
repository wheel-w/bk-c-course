# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community
Edition) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from project.models import Project
from project.serializer import PartialProjectSerializer, ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @swagger_auto_schema(
        request_body=ProjectSerializer,
        operation_summary="创建项目",
    )
    def create(self, request, *args, **kwargs):
        request.data["creator"] = request.user.username
        request.data["updater"] = request.user.username
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @swagger_auto_schema(
        request_body=ProjectSerializer,
        operation_summary="更新项目信息",
        responses={201: ProjectSerializer},
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        request.data["updater"] = request.user.username
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=PartialProjectSerializer,
        operation_summary="局部更新项目信息",
        responses={201: PartialProjectSerializer},
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        request.data["updater"] = request.user.username
        return super().update(request, *args, **kwargs)
