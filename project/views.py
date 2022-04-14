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

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from common.export_excel import export_excel
from project.models import Project, UserProjectContact
from project.serializer import (
    PartialProjectSerializer,
    ProjectSerializer,
    UserProjectContactSerializer,
)
from user_manager.models import User


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


class UserProjectContactViewSet(viewsets.ModelViewSet):
    queryset = UserProjectContact.objects.all()
    serializer_class = UserProjectContactSerializer

    @swagger_auto_schema(
        operation_summary="传入project_id和user_id创建一条UserProjectContact记录"
    )
    def create(self, request, *args, **kwargs):
        project_id = request.data["project_id"]
        user_id = request.data["user_id"]
        data = UserProjectContact.objects.create(project_id=project_id, user_id=user_id)
        serializer = UserProjectContactSerializer(data)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="获取id为project_id的项目下的所有用户信息")
    def retrieve(self, request, *args, **kwargs):
        project_id = kwargs["project_id"]
        data = UserProjectContact.objects.filter(project_id=project_id)
        serializer = super().get_serializer(data, many=True)
        return Response(serializer.data)

    # 向项目中批量导入用户
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user_id_list"],
            properties={
                "user_id_list": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                )
            },
        ),
        operation_summary="根据user_id批量导入项目下的用户",
    )
    def bulk_import(self, request, *args, **kwargs):
        project_id = kwargs["project_id"]
        user_id_list = request.data["user_id_list"]
        queryset_list = []
        for user_id in user_id_list:
            queryset_list.append(
                UserProjectContact(project_id=project_id, user_id=user_id)
            )
        data = UserProjectContact.objects.bulk_create(queryset_list)
        serializer = UserProjectContactSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # 传入一个数组user_id_list，批量删除项目下的用户
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user_id_list"],
            properties={
                "user_id_list": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                )
            },
        ),
        operation_summary="根据user_id批量删除项目下的用户",
    )
    def destroy(self, request, *args, **kwargs):
        project_id = kwargs["project_id"]
        user_id_list = request.data["user_id_list"]
        UserProjectContact.objects.filter(
            project_id=project_id, user_id__in=user_id_list
        ).delete()
        return Response()

    # 导出用户名单
    @swagger_auto_schema(operation_summary="导出id为project_id的项目的用户名单")
    def export_info(self, request, *args, **kwargs):
        # 表头数据
        head_data = ["姓名", "性别", "手机号"]
        # 查询记录数据
        records = []
        project_id = kwargs["project_id"]
        title = f"{Project.objects.get(id=project_id).name}用户名单"
        user_id_list = []
        user_ids = UserProjectContact.objects.filter(project_id=project_id)
        for u_i in user_ids:
            user_id_list.append(u_i.user_id)
        users = User.objects.filter(id__in=user_id_list)
        obj = {"MALE": "男", "FEMALE": "女"}
        # 添加记录
        for user in users:
            record = [user.name, obj[user.gender], user.phone_number]
            records.append(record)
        return export_excel(head_data, records, title)
