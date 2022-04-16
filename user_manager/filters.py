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
import django_filters
from django_filters.rest_framework import FilterSet

from user_manager.models import User


class UserFilter(FilterSet):
    """user展示的过滤器"""

    name = django_filters.CharFilter(
        field_name="name", lookup_expr="icontains"
    )  # icontains 包含,忽略大小写
    gender = django_filters.CharFilter(field_name="gender")
    min_date = django_filters.DateFilter(
        field_name="account_id__last_login", lookup_expr="gte"
    )
    max_date = django_filters.DateFilter(
        field_name="account_id__last_login", lookup_expr="lte"
    )

    class Meta:
        model = User  # 关联的模型
        fields = ["name", "gender", "min_date", "max_date"]  # 过滤的字段
