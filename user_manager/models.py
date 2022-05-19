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
from django.conf import settings
from django.db import models
from django.utils import timezone


class User(models.Model):
    class Gender:
        MALE = "MALE"
        FEMALE = "FEMALE"

    GENDER = [(Gender.MALE, "男"), (Gender.FEMALE, "女")]
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
    )
    name = models.CharField("姓名", max_length=20, blank=True, null=True)
    gender = models.CharField(
        "性别", max_length=20, choices=GENDER, blank=True, null=True
    )
    phone_number = models.CharField("手机号", max_length=30, blank=True, null=True)
    email = models.EmailField("邮箱地址", blank=True, null=True)
    qq_number = models.CharField("qq号", max_length=15, blank=True, null=True)
    vx_number = models.CharField("vx号", max_length=15, blank=True, null=True)
    vx_open_id = models.CharField("微信Open_id", max_length=20, blank=True, null=True)
    time_created = models.DateTimeField("创建时间", default=timezone.now)
    time_updated = models.DateTimeField("修改时间", auto_now=True)

    def __str__(self):
        return f"{self.name}"


class UserTag(models.Model):
    class BuiltIn:
        BUILT_IN = 1
        NON_INTRINSIC = 2

    BUILTIN = [(BuiltIn.BUILT_IN, "内置"), (BuiltIn.NON_INTRINSIC, "非内置")]
    tag_value = models.CharField("标签值", max_length=20)
    tag_color = models.CharField("标签颜色", max_length=7)
    is_built_in = models.IntegerField("是否内置", choices=BUILTIN, default=False)
    sub_project = models.IntegerField("所属项目")
    time_created = models.DateTimeField("创建时间", default=timezone.now)
    time_updated = models.DateTimeField("修改时间", auto_now=True)
    tag_comment = models.CharField("备注", max_length=30, null=True)
    created_by = models.CharField("创建者", max_length=30, null=True)

    def __str__(self):
        return f"{self.tag_value}_{self.tag_color}"


class UserTagContact(models.Model):
    user_id = models.BigIntegerField("用户id")
    tag_id = models.BigIntegerField("标签id")

    def __str__(self):
        return "{}-{}".format(self.user_id, self.tag_id)
