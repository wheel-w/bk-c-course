# -*- coding: utf-8 -*-
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
import json

import requests
from django.core.exceptions import ObjectDoesNotExist
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from blueapps.account.models import User as Account
from user_manager import serialize
from user_manager.filters import UserFilter
from user_manager.models import User, UserTag, UserTagContact
from user_manager.pagination import MyPageNumberPagination

from .static_var import PROFILES_LIST_URL, REQUEST_PARAMS


# 用户相关视图
class AccountView(GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = serialize.AccountGetSerializer


class OriginAccountView(ViewSet):
    queryset = Account.objects.all()
    serialize_class = serialize.OriginAccountSerilizer

    @action(methods=["GET"], detail=False)
    def get_account_list(self, request, *args, **kwargs):
        """获取蓝鲸账户列表"""
        params = request.query_params
        REQUEST_PARAMS["wildcard_search"] = params.get("key", "")
        data = requests.get(PROFILES_LIST_URL, params=REQUEST_PARAMS)
        # 解析数据
        data = json.loads(data.content)
        # 数据校验
        if not data["result"]:
            return Response(data["message"], exception=True)
        if data["data"]["count"] == 0:
            return Response("没有找到您想找的用户", exception=True)
        # 添加字段 is_import
        src_data = data["data"]["results"]
        # 获取返回的用户名列表
        account_username = {account["username"] for account in src_data}
        # 获取存在本系统中的用户列表
        exist_user = User.objects.filter(
            account_id__username__in=account_username
        ).values_list("account_id__username", flat=True)
        # 重构数据
        store_list = []
        for elem in src_data:
            store_list.append(
                {
                    "username": elem["username"],
                    "name": elem["display_name"],
                    "departments": elem["departments"][0]["name"],
                    "is_import": True if elem["username"] in exist_user else False,
                }
            )

        return Response(store_list)

    @action(methods=["GET"], detail=False)
    def get_user(self, request, *args, **kwargs):
        """获取用户信息, 如果没有则自动创建一个将username当做name的user"""
        username = request.query_params.get("username")
        # 确保用户传入了一个username
        if not username:
            return Response("请传递一个用户名", exception=True)
        # 判断该用户是否存在于本地account中
        try:
            instance = self.queryset.get(username=username)
        except ObjectDoesNotExist:
            return Response("用户不存在", exception=True)
        # 获取user信息
        try:
            user = User.objects.get(account_id=instance.id)
        except ObjectDoesNotExist:
            return Response("您尚未被导入到当前系统中", exception=True)
        serializer = serialize.UserSerSerializer(user)
        return Response(serializer.data)


class BatchView(ViewSet):
    queryset = User.objects.all()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username_name_map", "tag_value"],
            properties={
                "username_name_map": openapi.Schema(type=openapi.TYPE_OBJECT),
                "tag_value": openapi.Schema(type=openapi.TYPE_STRING),
            },
        ),
    )
    @action(methods=["POST"], detail=False)
    def add(self, request, *args, **kwargs):
        """
        批量增加用户
        return:
            existent: 已经存在于user里面的用户名
            add: 新增加到account和user里的用户名
            pre_exist: 已经存在于account但时新增到user里面的用户名
        """
        # 参数校验
        username_name_map = request.data.get("username_name_map")
        if not username_name_map or not isinstance(username_name_map, dict):
            return Response("请传入一个用户名-姓名映射字典", exception=True)
        tag_value = request.data.get("tag_value")
        if not tag_value:
            return Response("请制定一个标签")
        tag = UserTag.objects.filter(tag_value=tag_value).first()
        # 获取已经存在的用户, 并在usernames列表中删除这些用户
        export_usernames = set(username_name_map.keys())
        exist_users = set(
            User.objects.filter(account__username__in=export_usernames).values_list(
                "account__username", flat=True
            )
        )
        exist_accounts = set(
            Account.objects.filter(username__in=export_usernames).values_list(
                "username", flat=True
            )
        )
        # 删除已经存在于账号中的用户名
        export_usernames = set(export_usernames) - exist_accounts
        # 从已存在用户名列表中 删除未在user中出现的用户名
        exist_accounts = exist_accounts - exist_users
        if not (export_usernames or exist_accounts):
            # 如果所有用户都在user中存在则返回
            return Response("所选用户已经添加到本系统", exception=True)
        # 批量增加 Account
        new_account_list = []
        for username in export_usernames:
            new_account_list.append(
                Account(
                    username=username,
                    password="",
                    is_superuser=False,
                    is_active=True,
                    is_staff=False,
                )
            )
        Account.objects.bulk_create(new_account_list)
        # 将只有账户没有User的用户加入到要增加User的列表中
        new_user_usernames = export_usernames | exist_accounts
        # 批量增加 User
        new_user_account = Account.objects.filter(
            username__in=new_user_usernames
        ).values("id", "username")
        new_user_list = []
        new_tag_list = []
        for account in new_user_account:
            new_user_list.append(
                User(
                    id=account.get("id"),
                    account_id=account.get("id"),
                    name=username_name_map.get(account.get("username")),
                )
            )
            new_tag_list.append(
                UserTagContact(user_id=account.get("id"), tag_id=tag.id)
            )

        User.objects.bulk_create(new_user_list)
        UserTagContact.objects.bulk_create(new_tag_list)
        return Response(
            {
                "existent": exist_users,
                "add": new_user_usernames,
                "pre_exist": exist_accounts,
            }
        )

    @action(methods=["POST"], detail=False)
    def delete(self, request, *args, **kwargs):
        """批量删除User"""
        # 参数校验
        id_list = request.data.get("id_list")
        if not id_list or not isinstance(id_list, list):
            return Response("请传入一个id列表", exception=True)
        # 获取要删除的用户列表
        queryset = self.queryset.filter(id__in=id_list)
        delete_users = []
        for i in queryset:
            # 记录删除的用户姓名
            delete_users.append(i.name)
            # 在删除列表中删除已经找到的用户名
            id_list.remove(i.id)
        if not queryset:
            return Response("没有找到任何对应用户", exception=True)
        # 统一删除
        queryset.delete()
        return Response(
            {
                "delete_count": len(delete_users),
                "delete": delete_users,
                "not_found": id_list,
            },
            status=status.HTTP_204_NO_CONTENT,
        )


class UserView(GenericViewSet):
    """查询用户信息"""

    queryset = User.objects.all().filter(account_id__is_active=True)  # 只显示非禁用账户
    serializer_class = serialize.UserSerSerializer
    pagination_class = MyPageNumberPagination
    filter_class = UserFilter
    filter_fields = ["name", "gender"]

    def list(self, request, *args, **kwargs):
        """获取用户信息, 并返回"""
        queryset = self.get_queryset()
        # 根据 tag_value 筛选
        role = request.query_params.get("role")
        if role:
            if isinstance(role, list):
                role_ids = UserTag.objects.filter(tag_value__in=role).values("id")
            elif isinstance(role, str):
                role_ids = UserTag.objects.filter(tag_value=role).values("id")
            else:
                return Response("请返回一个tag_value列表或者一个tag_value", exception=True)
            user_ids = (
                UserTagContact.objects.filter(tag_id__in=role_ids)
                .values("user_id")
                .distinct()
            )
            queryset = queryset.filter(id__in=user_ids)
        # 根据 filter_class 进行筛选
        queryset = self.filter_queryset(queryset)
        # 分页
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # 在返回的字段中添加tag字段(与 listMixin 的唯一区别)
            self.add_tag(serializer.data)
            return self.get_paginated_response(serializer.data)
        # 序列化信息
        serializer = self.get_serializer(queryset, many=True)
        self.add_tag(serializer.data)
        return Response(serializer.data)

    def add_tag(self, users):
        """给每一个返回的 User 增加一个tag字段"""
        user_ids = [user.get("id") for user in users]
        user_tag_dic = self.get_user_tag_map(user_ids)
        for user in users:
            # 遍历每一个获取到user 查看其是否有标签
            if user.get("id") in user_tag_dic:
                user["tag"] = user_tag_dic.get(user.get("id"))
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
            tags_dic[tag.id] = {"tag_value": tag.tag_value, "tag_color": tag.tag_color}
        user_tag_dic = {}  # key: user_id  value: {tags_dic ...}
        for tag_conn in tag_conns:
            if user_tag_dic.get(tag_conn.user_id):
                user_tag_dic[tag_conn.user_id][tag_conn.tag_id] = tags_dic[
                    tag_conn.tag_id
                ]
            else:
                user_tag_dic[tag_conn.user_id] = {
                    tag_conn.tag_id: tags_dic[tag_conn.tag_id]
                }
        return user_tag_dic

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = dict(serializer.data)
        data["tag"] = self.get_user_tag_map([data.get("id")]).get(instance.id)
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        instance.delete()
        return Response(serializer.data)


class UserUpdateView(GenericViewSet, UpdateModelMixin, RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = serialize.UserBaseSerializer
