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

from django.urls import include, path
from rest_framework.routers import DefaultRouter, SimpleRouter

from user_manager import views

# users
router = DefaultRouter()
router.register("", views.UserView)
router.register("batch", views.UserBatchView)
# accounts
router_account = DefaultRouter()
router_account.register("", views.OriginAccountView)
# tags
router_tag = DefaultRouter()
router_tag.register("", views.TagView)
# UserTagContacts
UserTagContacts = SimpleRouter(False)  # 解决 batch post 方法不可用
UserTagContacts.register("", views.UserTagContactView)
urlpatterns = [
    path("users/", include(router.urls)),
    path("accounts/", include(router_account.urls)),
    path("tags/", include(router_tag.urls)),
    path("UserTagContacts/", include(UserTagContacts.urls)),
    path(
        "UserTagContacts/batch/<int:type>",
        views.ContactBatch.as_view(
            {
                "post": "create",
            }
        ),
    ),
    path(
        "UserTagContacts/batch/<int:type>/<int:id>",
        views.ContactBatch.as_view({"delete": "destroy"}),
    ),
]
