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
from rest_framework import serializers

from blueapps.account.models import User as Account

from . import models


class UserTagSerializer(serializers.ModelSerializer):
    """用户的标签的序列化器"""

    class Meta:
        model = models.UserTag
        fields = "__all__"


class UserTagContactSerializer(serializers.ModelSerializer):
    """用户-用户标签多对多关系序列化器"""

    class Meta:
        model = models.UserTagContact
        fields = ["id", "user_id", "tag_id"]


class UserBaseSerializer(serializers.ModelSerializer):
    """用户信息, 更新"""

    class Meta:
        model = models.User
        fields = [
            "id",
            "name",
            "gender",
            "phone_number",
            "email",
            "qq_number",
            "vx_number",
            "vx_open_id",
        ]


class AccountSerializer(serializers.ModelSerializer):
    """用于显示的账户序列化器"""

    class Meta:
        model = Account
        fields = ["last_login", "username"]
        extra_kwargs = {
            "username": {"allow_null": True, "allow_blank": True, "required": False}
        }


class AccountGetSerializer(serializers.ModelSerializer):
    id_list = serializers.ListField()

    class Meta:
        model = Account
        fields = ["id_list"]


class UserSerSerializer(serializers.ModelSerializer):
    """查找用户信息"""

    # 上一次登录信息
    last_login = serializers.CharField(source="account.last_login", read_only=True)
    # 用户名
    username = serializers.CharField(source="account.username", read_only=True)
    # 标签
    role = serializers.CharField(min_length=2, max_length=4, read_only=True)

    class Meta:
        model = models.User
        fields = [
            "id",
            "username",
            "last_login",
            "role",
            "name",
            "gender",
            "phone_number",
            "email",
            "qq_number",
            "vx_number",
            "vx_open_id",
        ]


class OriginAccountSerilizer(serializers.Serializer):
    """蓝鲸账户信息"""

    username = serializers.CharField()
    departments = serializers.ListField()
    display_name = serializers.CharField()
    leader = serializers.ListField()
