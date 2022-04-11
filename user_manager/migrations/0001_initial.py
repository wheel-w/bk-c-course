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
# Generated by Django 3.2.4 on 2022-04-11 10:49

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("account", "0008_userproxy"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "u",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="account.user",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="姓名"
                    ),
                ),
                (
                    "gender",
                    models.CharField(
                        blank=True,
                        choices=[("MALE", "男"), ("FEMALE", "女")],
                        max_length=20,
                        null=True,
                        verbose_name="性别",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True, max_length=30, null=True, verbose_name="手机号"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, verbose_name="邮箱地址"
                    ),
                ),
                (
                    "qq_number",
                    models.CharField(
                        blank=True, max_length=15, null=True, verbose_name="qq号"
                    ),
                ),
                (
                    "vx_number",
                    models.CharField(
                        blank=True, max_length=15, null=True, verbose_name="vx号"
                    ),
                ),
                (
                    "vx_open_id",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="微信Open_id"
                    ),
                ),
                (
                    "time_created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="创建时间"
                    ),
                ),
                (
                    "time_updated",
                    models.DateTimeField(auto_now=True, verbose_name="修改时间"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("tag_value", models.CharField(max_length=20, verbose_name="标签值")),
                ("tag_color", models.CharField(max_length=7, verbose_name="标签颜色")),
                (
                    "is_built_in",
                    models.IntegerField(
                        choices=[(1, "内置"), (2, "非内置")],
                        default=False,
                        verbose_name="是否内置",
                    ),
                ),
                ("sub_project", models.IntegerField(verbose_name="所属项目")),
                (
                    "time_created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="创建时间"
                    ),
                ),
                (
                    "time_updated",
                    models.DateTimeField(auto_now=True, verbose_name="修改时间"),
                ),
                (
                    "tag_comment",
                    models.CharField(max_length=30, null=True, verbose_name="备注"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserTagContact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.BigIntegerField(verbose_name="用户id")),
                ("tag_id", models.BigIntegerField(verbose_name="标签id")),
            ],
            options={
                "db_table": "u_tag_user",
            },
        ),
    ]
