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

from django.db import models


class Project(models.Model):
    name = models.CharField("项目名称", max_length=90)
    introduction = models.TextField("项目简介", blank=True, null=True)
    property = models.CharField("项目性质", max_length=90)
    category = models.CharField("项目归属", max_length=90)
    organization = models.CharField("组织名称", max_length=90)
    creator = models.CharField("创建人", max_length=90)
    create_time = models.DateTimeField("项目创建时间", auto_now_add=True)
    update_time = models.DateTimeField("项目更新时间", auto_now=True)

    class Meta:
        db_table = "project"
        ordering = ["-update_time"]

    def __str__(self):
        return self.name
