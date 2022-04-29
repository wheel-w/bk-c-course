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


class SCORE:
    WRONG = 0  # 错误时的得分
    NOT_JUDGE = -1  # 未批改时的得分


class TYPES:
    SINGLE = "SINGLE"
    MULTIPLE = "MULTIPLE"
    COMPLETION = "COMPLETION"
    JUDGE = "JUDGE"
    SHORT_ANSWER = "SHORT_ANSWER"


class STATUS:
    NOT_ANSWER = "NOT_ANSWER"
    SAVED = "SAVED"
    SUBMITTED = "SUBMITTED"
    MARKED = "MARKED"
    CANCEL = "CANCEL"
