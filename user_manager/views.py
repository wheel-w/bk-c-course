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
from rest_framework.viewsets import ModelViewSet
from user_manager import serialize
from user_manager.models import User, UserTag, UserTagContact


class UserView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serialize.UserRegisterSerializer


class AddTagToUserView(ModelViewSet):
    queryset = UserTagContact.objects.all()
    serializer_class = serialize.UserTagContactSerializer


class UserTagView(ModelViewSet):
    queryset = UserTag.objects.all()
    serializer_class = serialize.UserTagSerializer
