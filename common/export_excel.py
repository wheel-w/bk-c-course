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

import tempfile

from django.http import FileResponse
from django.utils.encoding import escape_uri_path
from xlwt import Workbook


def export_excel(head_data, records, title):
    w = Workbook(encoding="utf-8")
    sheet1 = w.add_sheet("sheet1")
    for filed in range(0, len(head_data)):
        sheet1.write(0, filed, head_data[filed])
    for row in range(1, len(records) + 1):
        for col in range(0, len(head_data)):
            sheet1.write(row, col, records[row - 1][col])
            sheet1.col(col).width = 256 * 15

    tmpfile = tempfile.NamedTemporaryFile(
        mode="w+b", suffix=".xls", dir="static/files", delete=True
    )
    w.save(tmpfile)
    tmpfile.flush()
    tmpfile.seek(0)
    response = FileResponse(tmpfile, as_attachment=True)
    response["Content-Type"] = "application/octet-stream"
    response["Content-Disposition"] = "attachment;filename={}".format(
        escape_uri_path(f"{title}.xls")
    )
    return response
