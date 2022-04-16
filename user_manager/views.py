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
from blueapps.account.models import User as Account
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from user_manager import serialize
from user_manager.filters import UserFilter
from user_manager.models import User, UserTag, UserTagContact
from user_manager.pagination import MyPageNumberPagination

from .static_var import PROFILES_LIST_URL, REQUEST_PARAMS


# 用户相关视图
class AccountView(GenericViewSet):
    """用户登录之后自动获取用户信息"""

    queryset = Account.objects.all()
    serializer_class = serialize.AccountGetSerializer

    def retrieve(self, request, *args, **kwargs):
        """进入页面后获取用户信息, 如果没有则自动创建一个将username当做name的user"""
        instance = self.get_object()
        user = User.objects.filter(id=instance.id)
        if not user:
            self.create_user(instance)
            user = User.objects.filter(id=instance.id)
        serializer = serialize.UserSerSerializer(user.first())
        return Response(serializer.data)

    @staticmethod
    def create_user(instance):
        user = User.objects.create(
            id=instance.id, account_id=instance.id, name=instance.username
        )

        return user


class OriginAccountView(ViewSet):
    queryset = Account.objects.all()
    serialize_class = serialize.OriginAccountSerilizer

    @action(methods=["GET"], detail=False)
    def get_account_list(self, request, *args, **kwargs):
        """获取蓝鲸账户列表"""
        params = request.query_params
        REQUEST_PARAMS["page"] = params.get("page", 1)
        REQUEST_PARAMS["wildcard_search"] = params.get("key", "")
        data = requests.get(PROFILES_LIST_URL, params=REQUEST_PARAMS)
        data = json.loads(data.content)
        return Response(data["data"])


class BatchView(ViewSet):
    queryset = User.objects.all()

    @action(methods=["POST"], detail=False)
    def add(self, request, *args, **kwargs):
        """批量增加用户"""
        # 参数校验
        usernames = request.data.get("usernames")
        if not usernames or not isinstance(usernames, list):
            return Response("请传入一个用户名列表", exception=True)
        # 获取已经存在的用户, 并在usernames列表中删除这些用户
        accounts = Account.objects.filter(username__in=usernames).values("username")

        exist_accounts = []
        for account in accounts:
            usernames.remove(account["username"])
            exist_accounts.append(account["username"])
        if not usernames:
            return Response("所选用户已经添加到本系统", exception=True)
        # 批量增加 Account
        account_list = []
        for username in usernames:
            account_list.append(
                Account(
                    username=username,
                    password="",
                    is_superuser=False,
                    is_active=True,
                    is_staff=False,
                )
            )
        Account.objects.bulk_create(account_list)
        # 批量增加 User
        account_ids = Account.objects.filter(username__in=usernames).values(
            "username", "id"
        )
        user_list = [
            User(id=account["id"], account_id=account["id"], name=account["username"])
            for account in account_ids
        ]
        User.objects.bulk_create(user_list)
        return Response({"existent": exist_accounts, "add": usernames})

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
            # 纪录删除的用户姓名
            delete_users.append(i.name)
            # 在删除列表中删除已经删除的用户名
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


class UserView(GenericViewSet, DestroyModelMixin):
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
                Response("请返回一个tag_value列表或者一个tag_value", exception=True)
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
        """获取每一个返回的 User 所拥有的标签"""
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
        data["tag"] = self.get_user_tag_map([data.get("id")]).pop(instance.id)
        return Response(data)


class UserUpdateView(GenericViewSet, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = serialize.UserBaseSerializer
