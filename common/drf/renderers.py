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
import json

from rest_framework.compat import INDENT_SEPARATORS, LONG_SEPARATORS, SHORT_SEPARATORS
from rest_framework.renderers import JSONRenderer


class StandardResponseRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        renderer_context = renderer_context or {}
        renderer_context["response"].status_code = 200
        indent = self.get_indent(accepted_media_type, renderer_context)

        if indent is None:
            separators = SHORT_SEPARATORS if self.compact else LONG_SEPARATORS
        else:
            separators = INDENT_SEPARATORS

        # 如果请求失败,填充message信息
        if renderer_context["response"].exception:
            if isinstance(data, str):
                message = data
            elif isinstance(data, dict):
                message = ""
                for key, value in data.items():
                    message = f"{message}[{key}]{''.join(value)}\n"
            render_data = {
                "result": False,
                "message": message,
                "code": -1,
                "data": None,
            }

        else:
            render_data = {
                "result": True,
                "message": "success",
                "code": 0,
                "data": data,
            }

        ret = json.dumps(
            render_data,
            cls=self.encoder_class,
            indent=indent,
            ensure_ascii=self.ensure_ascii,
            allow_nan=not self.strict,
            separators=separators,
        )

        ret = ret.replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
        return ret.encode()
