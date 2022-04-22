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
import json
import logging
import math
import time
from concurrent.futures import ThreadPoolExecutor

import requests
from celery.task import task

from user_manager.models import User
from user_manager.static_var import PROFILES_LIST_URL, REQUEST_PARAMS

logger = logging.getLogger("root")


@task()
def judge_objective():
    """
    return:
        蓝鲸账号所有数据
    """
    # 创建线程池
    pool = ThreadPoolExecutor(5)
    # 设置获取第一个数据, 从而获得总页数
    get_count_params = REQUEST_PARAMS.copy()
    get_count_params["page_size"] = 1
    first_data = get_data(get_count_params)
    ret_data_list = [first_data["results"][0]]
    # 获得总页数
    count = first_data["count"]
    # 获取线程执行结果
    res_list = []
    for i in range(1, math.ceil(count / REQUEST_PARAMS["page_size"]) + 1):
        res = pool.submit(get_data, REQUEST_PARAMS, i)
        res_list.append(res)
    # 关闭线程池
    pool.shutdown()
    for res in res_list:
        ret_data_list.extend(res.result()["results"])
    # 获取数据
    ret_data = structure_dict(ret_data_list)
    return ret_data


def get_data(params, page=1):
    time.sleep(0.2)
    params = params.copy()
    params["page"] = page
    data = requests.get(PROFILES_LIST_URL, params)
    data = json.loads(data.content)
    if not data["result"]:
        logger.error(f"账户数据获取失败, 请求信息:{params}")
        return False
    return data["data"]


def structure_dict(src_data, store_dict=None):
    if store_dict is None:
        store_dict = {}
    account_username = {account["username"] for account in src_data}
    exist_user = User.objects.filter(
        account_id__username__in=account_username
    ).values_list("account_id__username", flat=True)
    for elem in src_data:
        store_dict[elem["username"]] = {
            "username": elem["username"],
            "name": elem["display_name"],
            "departments": elem["departments"][0]["name"],
            "is_import": True if elem["username"] in exist_user else False,
        }
    return store_dict
