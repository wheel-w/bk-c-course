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

from django.conf.urls import include, url
from django.contrib import admin

from home_application.views import django_admin_static_serve

urlpatterns = [
    url(r"^django_admin/", admin.site.urls),
    url(
        r"^django_admin/(?P<path>.*)$",
        django_admin_static_serve,
        {"document_root": "static"},
    ),
    url(r"^course/", include("course.urls")),
    url(r"^account/", include("blueapps.account.urls")),
    # 如果你习惯使用 Django 模板，请在 home_application 里开发你的应用，
    # 这里的 home_application 可以改成你想要的名字
    url(r"^", include("home_application.urls")),
    # 如果你习惯使用 mako 模板，请在 mako_application 里开发你的应用，
    # 这里的 mako_application 可以改成你想要的名字
    url(r"^mako/", include("mako_application.urls")),
    url(r"^i18n/", include("django.conf.urls.i18n")),
    url(r"course/", include("course.urls")),
    url(r"^api/", include("project.urls")),
    url(r"^api/", include("user_manager.urls")),
    url(r"^api/", include("project_task.urls")),
    url(r"^api/", include("question.urls")),
    # swagger-ui
    url(r"^", include("common.urls")),
]
