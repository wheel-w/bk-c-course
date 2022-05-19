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

import xlwt
from django.http import FileResponse
from django.utils.encoding import escape_uri_path
from xlwt import Pattern, Style, Workbook, XFStyle


def export_excel(head_data, records, title):
    w = Workbook(encoding="utf-8")
    sheet1 = w.add_sheet("sheet1")
    for filed in range(0, len(head_data)):
        sheet1.write(0, filed, head_data[filed], excel_head_style())
    for row in range(1, len(records) + 1):
        for col in range(0, len(head_data)):
            sheet1.write(row, col, records[row - 1][col], excel_record_style())
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


# 定义导出文件表头格式
def excel_head_style():
    # 创建一个样式
    style = XFStyle()
    # 设置背景色
    pattern = Pattern()
    pattern.pattern = Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = Style.colour_map["light_green"]  # 设置单元格背景色
    style.pattern = pattern
    # 设置字体
    font0 = xlwt.Font()
    font0.name = "微软雅黑"
    font0.bold = True
    font0.colour_index = 0
    font0.height = 240
    style.font = font0
    # 设置文字位置
    alignment = xlwt.Alignment()  # 设置字体在单元格的位置
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
    alignment.vert = xlwt.Alignment.VERT_CENTER  # 竖直方向
    style.alignment = alignment
    # 设置边框
    borders = xlwt.Borders()  # Create borders
    borders.left = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.right = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.top = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.bottom = xlwt.Borders.THIN  # 添加边框-虚线边框
    style.borders = borders

    return style


# 定义导出文件记录格式
def excel_record_style():
    # 创建一个样式
    style = XFStyle()
    # 设置字体
    font0 = xlwt.Font()
    font0.name = "微软雅黑"
    font0.bold = False
    font0.colour_index = 0
    font0.height = 200
    style.font = font0
    # 设置文字位置
    alignment = xlwt.Alignment()  # 设置字体在单元格的位置
    alignment.horz = xlwt.Alignment.HORZ_CENTER  # 水平方向
    alignment.vert = xlwt.Alignment.VERT_CENTER  # 竖直方向
    style.alignment = alignment
    # 设置边框
    borders = xlwt.Borders()  # Create borders
    borders.left = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.right = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.top = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.bottom = xlwt.Borders.THIN  # 添加边框-虚线边框
    style.borders = borders

    return style
