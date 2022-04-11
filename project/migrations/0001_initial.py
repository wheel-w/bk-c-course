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
# Generated by Django 3.2.4 on 2022-04-07 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Project",
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
                ("name", models.CharField(max_length=90, verbose_name="项目名称")),
                (
                    "introduction",
                    models.TextField(blank=True, null=True, verbose_name="项目简介"),
                ),
                ("property", models.CharField(max_length=90, verbose_name="项目性质")),
                ("category", models.CharField(max_length=90, verbose_name="项目归属")),
                ("organization", models.CharField(max_length=90, verbose_name="组织名称")),
                ("creator", models.CharField(max_length=90, verbose_name="创建人")),
                (
                    "create_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="项目创建时间"),
                ),
                (
                    "update_time",
                    models.DateTimeField(auto_now=True, verbose_name="项目更新时间"),
                ),
            ],
            options={
                "db_table": "project",
                "ordering": ["-update_time"],
            },
        ),
    ]
