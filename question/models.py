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

from django.core.validators import validate_comma_separated_integer_list
from django.db import models

# Create your models here.
from django.utils import timezone


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

    course_id = models.IntegerField("题目所属课程id")
    types = models.CharField("题目类型", max_length=20, choices=TYPES)
    question = models.TextField("题目")
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
        return "{}".format(self.question)


class QuestionTag(models.Model):
    tag_value = models.CharField("标签值", max_length=20)
    tag_color = models.CharField("标签颜色", max_length=7)
    tag_text = models.CharField("标签说明", max_length=200)
    time_created = models.DateTimeField("创建时间", default=timezone.now)
    time_updated = models.DateTimeField("修改时间", auto_now=True)

    def __str__(self):
        return "{}".format(self.tag_value)


class QuestionTagContact(models.Model):
    user_id = models.BigIntegerField("用户id")
    tag_id = models.BigIntegerField("标签id")

    def __str__(self):
        return "{}-{}".format(self.user_id, self.tag_id)


class Paper(models.Model):
    status_list = ["DRAFT", "RELEASE", "MARKED"]

    class Types:
        EXERCISE = "EXERCISE"
        EXAM = "EXAM"

    class Status:
        DRAFT = "DRAFT"
        RELEASE = "RELEASE"
        MARKED = "MARKED"

    TYPES = [(Types.EXERCISE, "练习卷"), (Types.EXAM, "测试卷")]

    STATUS = [(Status.DRAFT, "草稿"), (Status.RELEASE, "已发布"), (Status.MARKED, "已批阅")]

    types = models.CharField("试卷类型", max_length=10, choices=TYPES)
    course_id = models.IntegerField("卷子所属课程id")
    paper_name = models.CharField("卷子名称", max_length=255)
    teacher = models.CharField("教师姓名", max_length=90)
    question_order = models.CharField(
        "存储题目顺序",
        validators=[validate_comma_separated_integer_list],
        max_length=200,
        blank=True,
        null=True,
        default="",
    )

    def __str__(self):
        return self.paper_name


class Exam(models.Model):
    class Status:
        DRAFT = "DRAFT"
        RELEASE = "RELEASE"
        MARKED = "MARKED"

    STATUS = [(Status.DRAFT, "草稿"), (Status.RELEASE, "已发布"), (Status.MARKED, "已批阅")]

    paper_id = models.IntegerField("试卷id")
    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    start_time = models.DateTimeField("开始时间", blank=True, null=True)
    end_time = models.DateTimeField("截止时间", blank=True, null=True)
    status = models.CharField("卷子状态", max_length=10, choices=STATUS)

    def __str__(self):
        return self.id


class StudentExamAnswer(models.Model):
    student_id = models.BigIntegerField("用户id")
    exam_id = models.IntegerField("考试id")
    stu_answers = models.JSONField("学生提交答案")
    individual_score = models.JSONField("学生题目单项得分")
    total_score = models.FloatField("学生总体得分", blank=True, null=True, default=0)

    def __str__(self):
        return "{}-{}".format(self.student_id, self.exam_id)


class StudentExamContact(models.Model):
    class Status:
        NOT_ANSWER = "NOT_ANSWER"
        SAVED = "SAVED"
        SUBMITTED = "SUBMITTED"
        MARKED = "MARKED"

    STATUS = [
        (Status.NOT_ANSWER, "未答题"),
        (Status.SAVED, "已保存"),
        (Status.SUBMITTED, "已提交"),
        (Status.MARKED, "已批改"),
    ]

    course_id = models.IntegerField("课程id")
    paper_id = models.IntegerField("卷子id")
    student_id = models.TextField("学生id")
    status = models.CharField("状态", max_length=10, choices=STATUS)
    score = models.FloatField("总分", blank=True, null=True, default=0)
    cumulative_time = models.DurationField("答题累计时间", default=timedelta(seconds=0))

    def __str__(self):
        return "{}-{}-{}".format(self.course_id, self.paper_id, self.student_id)
