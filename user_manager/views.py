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
from blueapps.account.models import User as Account
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from user_manager import serialize
from user_manager.filters import UserFilter
from user_manager.models import User, UserTag, UserTagContact
from user_manager.Pagination import MyPageNumberPagination


# 用户相关视图
class AccountView(GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = serialize.AccountDeleteSerializer

    # 删除用户
    def destroy(self, request, *args, **kwargs):
        request.data["is_active"] = False
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=["POST"], detail=False)
    def batch_delete(self, request, *args, **kwargs):
        """批量删除"""
        id_list = request.data.get("id_list")
        if not id_list or not isinstance(id_list, list):
            return Response("请传入一个id列表", exception=True)
        queryset = self.get_queryset().filter(id__in=id_list, is_active=True)
        if not queryset:
            return Response("没有找到任何对应用户", exception=True)
        for elem in queryset:
            elem.is_active = False
        Account.objects.bulk_update(queryset, ["is_active"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserView(GenericViewSet):
    """查寻用户信息"""

    queryset = User.objects.all().filter(account_id__is_active=True)  # 只显示非禁用账户
    serializer_class = serialize.UserSerSerializer
    pagination_class = MyPageNumberPagination
    filter_class = UserFilter
    filter_fields = ["name", "gender"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            self.add_tag(serializer.data)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.add_tag(serializer.data)
        return Response(serializer.data)

    def add_tag(self, users):
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


class UserRegisterView(GenericViewSet, CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = serialize.UserCreateSerializer


# 用户, 标签连接视图
class AddTagToUserView(ModelViewSet):
    queryset = UserTagContact.objects.all()
    serializer_class = serialize.UserTagContactSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# 标签相关视图
class UserTagView(ModelViewSet):
    queryset = UserTag.objects.all()
    serializer_class = serialize.UserTagSerializer
