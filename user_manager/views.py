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
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from blueapps.account.models import User as Account
from project.models import Project
from user_manager import serialize
from user_manager.filters import TagFilter, UserFilter, filter_by_role
from user_manager.models import User, UserTag, UserTagContact

from .static_var import PROFILES_LIST_URL, REQUEST_PARAMS, UserTagContactFindType


# 用户相关视图
class AccountView(GenericViewSet):
    queryset = Account.objects.all()
    serializer_class = serialize.AccountGetSerializer


class OriginAccountView(ViewSet):
    queryset = Account.objects.all()
    serialize_class = serialize.OriginAccountSerilizer
    lookup_url_kwarg = "username"

    def list(self, request, *args, **kwargs):
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
        exist_user_list = []
        for elem in src_data:
            if elem["username"] in exist_user:
                exist_user_list.append(
                    {
                        "username": elem["username"],
                        "display_name": elem["display_name"],
                        "departments": elem["departments"][0]["name"],
                        "is_import": True,
                    }
                )
            else:
                store_list.append(
                    {
                        "username": elem["username"],
                        "display_name": elem["display_name"],
                        "departments": elem["departments"][0]["name"],
                        "is_import": False,
                    }
                )
        store_list.extend(exist_user_list)
        return Response(store_list)

    def retrieve(self, request, *args, **kwargs):
        """获取用户信息, 如果没有则自动创建一个将username当做name的user"""
        username = kwargs.get("username")
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
        serializer = serialize.UserSerializer(user)
        return Response(serializer.data)


class UserBatchView(ViewSet):
    queryset = User.objects.all()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username_name_map", "tag_id"],
            properties={
                "username_name_map": openapi.Schema(type=openapi.TYPE_OBJECT),
                "tag_id": openapi.Schema(type=openapi.TYPE_INTEGER),
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
        tag_id = request.data.get("tag_id")
        if not UserTag.objects.filter(id=tag_id).exists():
            return Response("请指定一个有效标签", exception=True)
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
                UserTagContact(user_id=account.get("id"), tag_id=tag_id)
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
        tag_conn_queryset = UserTagContact.objects.filter(user_id__in=id_list)
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
        tag_conn_queryset.delete()
        return Response(
            {
                "delete_count": len(delete_users),
                "delete": delete_users,
                "not_found": id_list,
            },
            status=status.HTTP_204_NO_CONTENT,
        )

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["usernames", "tag_id"],
            properties={
                "usernames": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_STRING),
                ),
                "tag_id": openapi.Schema(type=openapi.TYPE_INTEGER),
            },
        ),
    )
    @action(methods=["POST"], detail=False)
    def add_tag(self, request, *args, **kwargs):
        """批量给用户添加标签"""
        tag_id = request.data.get("tag_id")
        # 查询数据库查看标签是否存在,病获得标签数据
        user_tag = UserTag.objects.filter(id=tag_id).first()
        if not user_tag:
            return Response("请指定一个有效标签", exception=True)
        # 获取要添加标签的用户信息
        usernames = request.data.get("usernames")
        users = set(
            self.queryset.filter(account_id__username__in=usernames).values_list(
                "id", "name"
            )
        )
        if not users:  # 用户校验: 是否存在有效用户
            return Response("请返回一个有效的用户名列表", exception=True)
        # 获取已经存在该标签的用户集合
        has_cur_tag_users = (
            UserTagContact.objects.filter(user_id__in=set(map(lambda x: x[0], users)))
            .values_list("user_id", flat=True)
            .distinct()
        )

        user_tag_contact_list = []
        exist_user_tag = set()
        # 给用户添加标签
        for user in users:
            if user[0] in has_cur_tag_users:  # 如果已经有了标签
                exist_user_tag.add(user)
            else:
                user_tag_contact_list.append(
                    UserTagContact(user_id=user[0], tag_id=tag_id)
                )
        # 批量增加
        UserTagContact.objects.bulk_create(user_tag_contact_list)

        return Response({"exist": exist_user_tag, "add": set(users) - exist_user_tag})


class UserView(GenericViewSet, UpdateModelMixin):
    """查询用户信息"""

    queryset = User.objects.all().filter(account_id__is_active=True)  # 只显示非禁用账户
    serializer_class = serialize.UserSerializer
    filter_class = UserFilter

    def list(self, request, *args, **kwargs):
        """获取用户信息, 并返回"""
        queryset = self.get_queryset()
        # 根据 tag_value 筛选
        tag_ids = set(request.query_params.get("tag_ids", {}))
        tag_ids |= set(request.data.get("tag_ids", {}))
        if tag_ids:
            flag, queryset_or_msg = filter_by_role(tag_ids, queryset)
            if not flag:
                return Response(queryset_or_msg, exception=True)
            else:
                queryset = queryset_or_msg
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

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = dict(serializer.data)
        data["tag"] = self.get_user_tag_map([data.get("id")]).get(instance.id).values()
        return Response(data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 删除标签
        UserTagContact.objects.filter(user_id=instance.id).delete()
        # 删除用户
        instance.delete()
        return Response(serializer.data)


class TagView(
    GenericViewSet,
    CreateModelMixin,
    RetrieveModelMixin,
):
    queryset = UserTag.objects.all()
    serializer_class = serialize.UserTagSerializer
    filter_class = TagFilter
    pagination_class = None  # 关闭分页

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        # 获取prj_id : prj_name 映射 方法一:
        # project_ids = queryset.values_list("sub_project", flat=1).distinct()
        # prj_map = Project.objects.filter(id__in=project_ids).values_list("id", "name")
        # 获取prj_id : prj_name 映射 方法二:
        prj_map = Project.objects.filter().values_list("id", "name")
        prj_map = {i[0]: i[1] for i in prj_map}

        serializer = self.get_serializer(queryset, many=True)
        for i in serializer.data:
            i["sub_project"] = prj_map.get(i["sub_project"])
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_built_in == UserTag.BuiltIn.BUILT_IN:
            return Response("内置标签不可删除", exception=True)
        if UserTagContact.objects.filter(tag_id=instance.id):
            return Response("当前标签已经绑定了用户, 请解除绑定用户后再进行删除", exception=True)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        if request.data.get("sub_project"):
            return Response("所属项目不允许修改", exception=True)
        if request.data.get("created_by"):
            return Response("创建者不允许修改", exception=True)
        instance = self.get_object()
        if instance.is_built_in == UserTag.BuiltIn.BUILT_IN:
            return Response("内置标签不允许修改", exception=True)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserTagContactView(GenericViewSet, CreateModelMixin, DestroyModelMixin):
    queryset = UserTagContact.objects.all()
    serializer_class = serialize.UserTagContactSerializer


class ContactBatch(GenericViewSet):
    queryset = UserTagContact.objects.all()
    serializer_class = serialize.UserTagContactSerializer

    def destroy(self, request, *args, **kwargs):
        id_ = kwargs.get("id")
        type_ = kwargs.get("type")
        if type_ == UserTagContactFindType.USER:
            self.queryset.filter(user_id=id_).delete()
        elif type_ == UserTagContactFindType.TAG:
            self.queryset.filter(tag_id=id_).delete()
        else:
            return Response("未查到对应项", exception=True)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user_ids", "tag_id"],
            properties={
                "users": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                ),
                "tags": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Items(type=openapi.TYPE_INTEGER),
                ),
            },
        ),
    )
    def create(self, request, *args, **kwargs):
        type_ = kwargs.get("type")
        user_ids = request.data.get("users")
        tag_ids = request.data.get("tags")
        insert_arr = []
        if type_ == UserTagContactFindType.TAG:
            # 给多个用户打同一个标签
            if not UserTag.objects.filter(id=tag_ids[0]).exists():
                return Response("标签不存在", exception=True)
            exist_contact = set(
                UserTagContact.objects.filter(tag_id__in=tag_ids).values_list(
                    "user_id", flat=True
                )
            )
            exist_user = set(
                User.objects.filter(id__in=user_ids).values_list("id", flat=True)
            )
            if not exist_user:
                return Response("用户不存在")
            for user_id in exist_user - exist_contact:
                insert_arr.append(UserTagContact(tag_id=tag_ids[0], user_id=user_id))
        elif type_ == UserTagContactFindType.USER:
            # 给一个用户打多个标签
            if not User.objects.filter(id=user_ids[0]).exists():
                return Response("用户不存在", exception=True)
            exist_contact = set(
                UserTagContact.objects.filter(user_id=user_ids[0]).values_list(
                    "tag_id", flat=True
                )
            )
            exist_tag = set(
                UserTag.objects.filter(id__in=tag_ids).values_list("id", flat=True)
            )
            if not exist_tag:
                return Response("标签不存在", exception=True)
            for tag_id in exist_tag - exist_contact:
                insert_arr.append(UserTagContact(tag_id=tag_id, user_id=user_ids[0]))
        else:
            return Response("未查到对应项", exception=True)
        UserTagContact.objects.bulk_create(insert_arr)
        return Response("successful", status=status.HTTP_201_CREATED)
