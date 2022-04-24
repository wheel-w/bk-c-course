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
from rest_framework.decorators import action
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
    filter_fields = ["property", "category", "organization", "creator"]

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

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["project_id_list"],
            properties={
                "project_id_list": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                )
            },
        ),
        operation_summary="根据project_id_list批量删除项目",
    )
    @action(methods=["DELETE"], detail=False)
    def bulk_delete(self, request, *args, **kwargs):
        project_id_list = request.data["project_id_list"]
        Project.objects.filter(id__in=project_id_list).delete()
        return Response()


class UserProjectContactViewSet(viewsets.ModelViewSet):
    queryset = UserProjectContact.objects.all()
    serializer_class = UserProjectContactSerializer

    @swagger_auto_schema(
        operation_summary="传入project_id和user_id创建一条UserProjectContact记录"
    )
    def create(self, request, *args, **kwargs):
        project_id = request.data["project_id"]
        user_id = request.data["user_id"]
        UserProjectContact.objects.create(project_id=project_id, user_id=user_id)
        return Response()

    @swagger_auto_schema(operation_summary="获取id为project_id的项目下的所有用户信息")
    def list(self, request, *args, **kwargs):
        project_id = kwargs["project_id"]
        data = UserProjectContact.objects.filter(project_id=project_id)
        page = self.paginate_queryset(data)
        user_id_list = [user.user_id for user in page]
        users = User.objects.filter(id__in=user_id_list)
        user_info = [
            {"id": user.id, "user_name": user.name, "gender": user.gender}
            for user in users
        ]
        return self.get_paginated_response(user_info)

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
        if not Project.objects.filter(id=project_id).exists():
            return Response(f"id为{project_id}的项目不存在", exception=True)
        user_id_list = request.data["user_id_list"]
        # 项目下已经存在的用户id
        exist_contacts = set(
            UserProjectContact.objects.filter(project_id=project_id).values_list(
                "user_id", flat=True
            )
        )
        exist_users = set(
            User.objects.filter(id__in=user_id_list).values_list("id", flat=True)
        )
        # 去重
        user_id_list = exist_users.difference(exist_contacts)
        queryset_list = []
        for user_id in user_id_list:
            queryset_list.append(
                UserProjectContact(project_id=project_id, user_id=user_id)
            )
        UserProjectContact.objects.bulk_create(queryset_list)
        return Response(status=status.HTTP_201_CREATED)

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
        user_id_list = UserProjectContact.objects.values_list(
            "user_id", flat=True
        ).filter(project_id=project_id)
        users = User.objects.filter(id__in=user_id_list)
        # 添加记录
        for user in users:
            record = [user.name, user.get_gender_display(), user.phone_number]
            records.append(record)
        return export_excel(head_data, records, title)
