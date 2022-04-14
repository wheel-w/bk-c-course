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
from rest_framework import status
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from user_manager import serialize
from user_manager.filters import UserFilter
from user_manager.models import User, UserTag, UserTagContact
from user_manager.Pagination import MyPageNumberPagination


# 用户相关视图
class AccountView(GenericViewSet, UpdateModelMixin):
    queryset = Account.objects.all()
    serializer_class = serialize.AccountSerializer

    def destroy(self, request, *args, **kwargs):
        request.data["is_active"] = False
        self.partial_update(request, *args)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserView(GenericViewSet, ListModelMixin, RetrieveModelMixin):
    queryset = User.objects.all()
    serializer_class = serialize.UserSerSerializer
    pagination_class = MyPageNumberPagination
    filter_class = UserFilter
    filter_fields = ["name", "gender"]


class RegisterView(GenericViewSet, CreateModelMixin, UpdateModelMixin):
    queryset = User.objects.all()
    serializer_class = serialize.UserRegisterSerializer


# 用户, 标签连接视图
class AddTagToUserView(ModelViewSet):
    queryset = UserTagContact.objects.all()
    serializer_class = serialize.UserTagContactSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


# 标签相关视图
class UserTagView(ModelViewSet):
    queryset = UserTag.objects.all()
    serializer_class = serialize.UserTagSerializer
