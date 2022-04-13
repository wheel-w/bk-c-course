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


class Exam(models.Model):
    class Status:
        DRAFT = "DRAFT"
        RELEASE = "RELEASE"
        MARKED = "MARKED"

    STATUS = [(Status.DRAFT, "草稿"), (Status.RELEASE, "已发布"), (Status.MARKED, "已批阅")]

    class Types:
        EXERCISE = "EXERCISE"
        EXAM = "EXAM"

    TYPES = [(Types.EXERCISE, "练习卷"), (Types.EXAM, "测试卷")]

    types = models.CharField("试卷类型", max_length=10, choices=TYPES)
    course_id = models.IntegerField("卷子所属课程id")
    title = models.CharField("卷子名称", max_length=255)
    master_teacher = models.CharField("出卷教师姓名", max_length=90)
    master_teacher_id = models.IntegerField("出卷教师id")
    question_order = models.CharField(
        "存储题目顺序",
        validators=[validate_comma_separated_integer_list],
        max_length=200,
        blank=True,
        null=True,
        default="",
    )

    create_time = models.DateTimeField("创建时间", auto_now_add=True)
    start_time = models.DateTimeField("开始时间", blank=True, null=True)
    end_time = models.DateTimeField("截止时间", blank=True, null=True)
    status = models.CharField("卷子状态", max_length=10, choices=STATUS)
    judge_teachers_id = models.CharField(
        "判卷老师id",
        validators=[validate_comma_separated_integer_list],
        max_length=200,
        blank=True,
        null=True,
        default="",
    )
    judge_teachers_weight = models.CharField(
        "判卷老师权重",
        validators=[validate_comma_separated_integer_list],
        max_length=200,
        blank=True,
        null=True,
        default="",
    )
    exam_students_id = models.CharField(
        "考生id",
        validators=[validate_comma_separated_integer_list],
        max_length=200,
        blank=True,
        null=True,
        default="",
    )

    def __str__(self):
        return self.title


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
    exam_id = models.IntegerField("卷子id")
    student_id = models.TextField("学生id")
    status = models.CharField("状态", max_length=10, choices=STATUS)
    score = models.FloatField("总分", blank=True, null=True, default=0)
    cumulative_time = models.DurationField("答题累计时间", default=timedelta(seconds=0))

    def __str__(self):
        return "{}-{}-{}".format(self.course_id, self.exam_id, self.student_id)
