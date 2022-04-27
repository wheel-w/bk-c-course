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
from django.db import models

# Create your models here.


class Question(models.Model):
    class QuestionTypes:
        SINGLE = "SINGLE"
        MULTIPLE = "MULTIPLE"
        COMPLETION = "COMPLETION"
        JUDGE = "JUDGE"
        SHORT_ANSWER = "SHORT_ANSWER"

    TYPES = [
        (QuestionTypes.SINGLE, "单选题"),
        (QuestionTypes.MULTIPLE, "多选题"),
        (QuestionTypes.COMPLETION, "填空题"),
        (QuestionTypes.JUDGE, "判断题"),
        (QuestionTypes.SHORT_ANSWER, "简答题"),
    ]

    project_id = models.BigIntegerField("题目所属项目id")
    types = models.CharField("题目类型", max_length=20, choices=TYPES)
    title = models.TextField("题目")
    question_url = models.TextField("题目文件url", null=True, blank=True)
    option_A = models.TextField("选项A", blank=True, null=True)
    option_B = models.TextField("选项B", blank=True, null=True)
    option_C = models.TextField("选项C", blank=True, null=True)
    option_D = models.TextField("选项D", blank=True, null=True)
    option_E = models.TextField("选项E", blank=True, null=True)
    answer = models.TextField("问题答案")
    answer_url = models.TextField("问题答案文件url", null=True, blank=True)
    explain = models.TextField("答案解析", blank=True, null=True, default="无")
    explain_url = models.TextField("答案解析文件url", null=True, blank=True)

    def __str__(self):
        return "{}".format(self.title)


class QuestionTag(models.Model):
    value = models.CharField("标签值", max_length=20)
    color = models.CharField("标签颜色", max_length=7)
    text = models.CharField("标签说明", max_length=200)
    time_created = models.DateTimeField("创建时间", auto_now_add=True)
    time_updated = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return "{}".format(self.value)


class QuestionTagContact(models.Model):
    question_id = models.BigIntegerField("用户id")
    tag_id = models.BigIntegerField("标签id")

    def __str__(self):
        return "{}-{}".format(self.question_id, self.tag_id)
