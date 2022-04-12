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

from rest_framework import serializers

from project.models import Project, UserProjectContact
from user_manager.models import User


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class UserProjectContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProjectContact
        fields = "__all__"

    # 校验传来的项目id和学生id是否存在
    def validate(self, attrs):
        if not Project.objects.filter(id=attrs["project_id"]).exists():
            raise serializers.ValidationError(f"id为{attrs['project_id']}的项目不存在!")
        if not User.objects.filter(id=attrs["user_id"]).exists():
            raise serializers.ValidationError(f"id为{attrs['user_id']}的学生不存在!")
        return attrs
