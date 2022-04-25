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
from datetime import timedelta

from django.db import models

# Create your models here.


class ProjectTask(models.Model):
    class Status:
        DRAFT = "DRAFT"
        RELEASE = "RELEASE"
        MARKED = "MARKED"

    STATUS = [(Status.DRAFT, "草稿"), (Status.RELEASE, "已发布"), (Status.MARKED, "已批阅")]

    class Types:
        DAILY = "DAILY"
        ASSESSMENT = "ASSESSMENT"

    TYPES = [(Types.DAILY, "日常任务"), (Types.ASSESSMENT, "考核任务")]

    project_id = models.BigIntegerField("任务所属项目id")
    types = models.CharField("任务类型", max_length=10, choices=TYPES)
    title = models.CharField("任务名称", max_length=255)
    describe = models.CharField("任务描述", max_length=255)
    questions_info = models.JSONField("题目id及其顺序与分值", blank=True, null=True)

    start_time = models.DateTimeField("任务开始时间", blank=True, null=True)
    end_time = models.DateTimeField("任务截止时间", blank=True, null=True)
    status = models.CharField("任务状态", max_length=10, choices=STATUS)
    judge_teachers_weight = models.JSONField("评委老师id及其权重")

    creator = models.TextField("创建者姓名")
    updater = models.TextField("更新者姓名")
    time_created = models.DateTimeField("任务创建时间", auto_now_add=True)
    time_updated = models.DateTimeField("任务更新时间", auto_now=True)

    students_visible = models.BooleanField("导师评分是否开启匿名", default=False)

    def __str__(self):
        return self.title


class StudentProjectTaskInfo(models.Model):
    student_id = models.BigIntegerField("学生id")
    project_id = models.BigIntegerField("项目id")
    project_task_id = models.BigIntegerField("任务id")
    stu_answers = models.JSONField("学生提交答案列表", blank=True, null=True)
    individual_score = models.JSONField("学生题目单项得分", blank=True, null=True)
    total_score = models.FloatField("学生总体得分", blank=True, null=True, default=0)

    class Status:
        NOT_ANSWER = "NOT_ANSWER"
        SAVED = "SAVED"
        SUBMITTED = "SUBMITTED"
        MARKED = "MARKED"
        CANCEL = "CANCEL"

    STATUS = [
        (Status.NOT_ANSWER, "未答题"),
        (Status.SAVED, "已保存"),
        (Status.SUBMITTED, "已提交"),
        (Status.MARKED, "已批改"),
        (Status.CANCEL, "已撤销"),
    ]

    status = models.CharField(
        "学生完成任务状态", max_length=10, choices=STATUS, default=Status.NOT_ANSWER
    )
    cumulative_time = models.DurationField("任务累计时间", default=timedelta(seconds=0))

    creator_id = models.BigIntegerField("创建者id")
    updator_id = models.BigIntegerField("更新者id")
    time_created = models.DateTimeField("创建时间", auto_now_add=True)
    time_updated = models.DateTimeField("更新时间", auto_now=True)

    def __str__(self):
        return "{}-{}-{}".format(self.project_id, self.project_task_id, self.student_id)
