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
from rest_framework import serializers

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


class AccountCreateSerializer(serializers.ModelSerializer):
    """账户创建"""

    class Meta:
        model = Account
        fields = ["password", "username", "nickname"]
        extra_kwargs = {
            "is_staff": {"default": False},
            "is_active": {"default": True},
            "is_superuser": {"default": False},
        }


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


class UserCreateSerializer(serializers.ModelSerializer):
    """创建帐号及用户"""

    account = AccountCreateSerializer(source="account_dict", write_only=True)

    role = serializers.CharField(
        min_length=2, max_length=2, required=True, write_only=True
    )

    class Meta:
        model = models.User
        fields = "__all__"

    def validate(self, attrs):
        print("invalidate")
        tag = models.UserTag.objects.filter(tag_value=attrs.pop("role")).first()
        if not tag:
            raise serializers.ValidationError("请输入存在的标签")
        attrs["role"] = tag
        return attrs

    def create(self, validated_data):
        account_data = validated_data.pop("account_dict")
        role = validated_data.pop("role")
        is_superuser = account_data.get("is_superuser")
        if is_superuser:
            account = Account.objects.create_superuser(**account_data)
        else:
            account = Account.objects.create_user(**account_data)
        user = models.User.objects.create(
            id=account.id, account_id=account.id, **validated_data
        )
        models.UserTagContact.objects.create(user_id=user.id, tag_id=role.id)
        return user


class AccountSerializer(serializers.ModelSerializer):
    """用于显示的账户序列化器"""

    class Meta:
        model = Account
        fields = ["last_login", "is_active", "username"]
        extra_kwargs = {
            "username": {"allow_null": True, "allow_blank": True, "required": False}
        }


class UserSerSerializer(serializers.ModelSerializer):
    """查找用户信息"""

    account = AccountSerializer(
        required=False
    )  # ["last_login", "is_active", 'username']

    role = serializers.CharField(
        min_length=2, max_length=2, required=True, write_only=True
    )

    class Meta:
        model = models.User
        fields = [
            "id",
            "account",
            "role",
            "name",
            "gender",
            "phone_number",
            "email",
            "qq_number",
            "vx_number",
            "vx_open_id",
        ]
