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

USER_PAGE_SIZE = 20
REQUEST_PARAMS = {
    "bk_app_code": "bk-course-manage",
    "bk_app_secret": "svgZF9p20lKI86YtMrAcI4WwDGyet3KcgVH8",
    "access_token": "bkcrypt%24gAAAAABiWMn-NXrNu4z_RfBhpM1H5Lx5_NNX5uhFbEOfOEcrKm1bZniwEACUpT"
    "-gslOQccXL8V58-W56aJrF3kQrPdboobCIU_-4RUN4hBSuMzh8FNrspCjQ2frvGNgmsHPNDggJBrf8",
    "fields": ["username", "departments", "display_name", "leader"],
    "wildcard_search_fields": ["departments__name", "display_name", "username"],
    "page_size": USER_PAGE_SIZE,
}

PROFILES_LIST_URL = (
    "https://bkapi.paas-edu.bktencent.com/api/bk-user/prod/api/v2/profiles/"
)
