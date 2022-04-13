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


class AccountRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["password", "username", "nickname"]
        extra_kwargs = {
            "is_staff": {"default": False},
            "is_active": {"default": True},
            "is_superuser": {"default": False},
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"

    account = AccountRegisterSerializer(source="account_dict", write_only=True)

    def create(self, validated_data):
        account_data = validated_data.pop("account_dict")
        is_superuser = account_data.get("is_superuser")
        if is_superuser:
            account = Account.objects.create_superuser(**account_data)
        else:
            account = Account.objects.create_user(**account_data)
        user = models.User.objects.create(account_id=account.id, **validated_data)
        return user


class UserTagContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserTagContact
        fields = "__all__"


class UserTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserTag
        fields = "__all__"
