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
from project.constants import USER_TYPE
from project.models import Project, UserProjectContact
from project.serializer import (
    PartialProjectSerializer,
    ProjectSerializer,
    UserProjectContactSerializer,
)
from user_manager.models import User, UserTag, UserTagContact
from user_manager.serialize import UserSerSerializer

from .filters import ProjectUserFilter


class ProjectViewSet(viewsets.ModelViewSet):
    """项目管理"""

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
        UserProjectContact.objects.create(
            project_id=serializer.data["id"], user_id=request.user.id
        )
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
    """项目人员管理"""

    queryset = UserProjectContact.objects.all()
    serializer_class = UserProjectContactSerializer
    filter_class = ProjectUserFilter

    @swagger_auto_schema(
        operation_summary="传入project_id和user_id创建一条UserProjectContact记录"
    )
    def create(self, request, *args, **kwargs):
        project_id = request.data["project_id"]
        user_id = request.data["user_id"]
        UserProjectContact.objects.create(project_id=project_id, user_id=user_id)
        return Response()

    @swagger_auto_schema(operation_summary="获取id为project_id的项目下的所有用户信息")
    def get_all_user_info(self, request, *args, **kwargs):
        project_id = kwargs["project_id"]
        data = UserProjectContact.objects.filter(project_id=project_id)
        user_id_list = [user.user_id for user in data]
        # 过滤
        users = self.filter_queryset(User.objects.filter(id__in=user_id_list))
        # 分页
        page = self.paginate_queryset(users)
        user_info = UserSerSerializer(page, many=True)
        self.add_tag(user_info.data)
        return self.get_paginated_response(user_info.data)

    def add_tag(self, users):
        """给每一个返回的 User 增加一个tag字段"""
        user_ids = [user.get("id") for user in users]
        user_tag_dic = self.get_user_tag_map(user_ids)
        for user in users:
            # 遍历每一个获取到user 查看其是否有标签
            if user.get("id") in user_tag_dic:
                user["tag"] = user_tag_dic.get(user.get("id")).values()
            else:
                user["tag"] = None
        return users

    @staticmethod
    def get_user_tag_map(user_ids):
        """获取每一个返回的 User 所拥有的标签列表"""
        tag_conns = UserTagContact.objects.filter(user_id__in=user_ids)
        tag_ids = {tag_conn.tag_id for tag_conn in tag_conns}
        tags = UserTag.objects.filter(id__in=tag_ids)
        tags_dic = {}  # key: 标签id  value: tag_value, tag_color
        for tag in tags:
            tags_dic[tag.id] = {
                "tag_id": tag.id,
                "tag_value": tag.tag_value,
                "tag_color": tag.tag_color,
            }
        user_tag_dic = {}  # key: user_id  value: {tags_dic ...}
        for tag_conn in tag_conns:
            if user_tag_dic.get(tag_conn.user_id):
                user_tag_dic[tag_conn.user_id][tag_conn.tag_id] = tags_dic.get(
                    tag_conn.tag_id
                )
            else:
                user_tag_dic[tag_conn.user_id] = {
                    tag_conn.tag_id: tags_dic.get(tag_conn.tag_id)
                }
        return user_tag_dic

    # 获取拥有指定的tag_value的用户的信息
    def get_user_info(self, project_id, scope):
        data = UserProjectContact.objects.filter(project_id=project_id)
        user_id_list = [relation.user_id for relation in data]
        users = User.objects.filter(id__in=user_id_list)
        user_info = UserSerSerializer(users, many=True)
        self.add_tag(user_info.data)
        actual_user_id_list = []
        for user in user_info.data:
            if user["tag"]:
                for tag_info in user["tag"]:
                    if tag_info["tag_value"] == scope:
                        actual_user_id_list.append(user["id"])
        # 过滤
        users = self.filter_queryset(User.objects.filter(id__in=actual_user_id_list))
        # 分页
        page = self.paginate_queryset(users)
        user_info = [
            {"id": user.id, "name": user.name, "gender": user.get_gender_display()}
            for user in page
        ]
        return user_info

    @swagger_auto_schema(operation_summary="获取id为project_id的项目下的所有的学生的信息")
    def get_all_stu_info(self, request, *args, **kwargs):
        project_id = kwargs["project_id"]
        user_info = self.get_user_info(project_id, USER_TYPE.STUDENT)
        return self.get_paginated_response(user_info)

    @swagger_auto_schema(operation_summary="获取id为project_id的项目下的所有的老师的信息")
    def get_all_tea_info(self, request, *args, **kwargs):
        project_id = kwargs["project_id"]
        user_info = self.get_user_info(project_id, USER_TYPE.TEACHER)
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
