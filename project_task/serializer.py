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

import datetime

from django.utils.timezone import utc
from rest_framework import serializers

from project_task.models import CeleryTaskInfo, ProjectTask, StudentProjectTaskInfo
from question.models import Question
from question.serializer import QuestionSerializer, QuestionShowSerializer
from user_manager.models import User

from .constants import STATUS, TASK_STATUS


class ProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = "__all__"


class ProjectTaskUpdateSerializer(serializers.ModelSerializer):
    questions_detail = serializers.ListField(
        child=serializers.DictField(), required=False
    )
    questions = QuestionSerializer(many=True, required=False)
    # 定时发布
    scheduled_publish_time = serializers.DateTimeField(required=False)

    class Meta:
        model = ProjectTask
        fields = [
            "title",
            "types",
            "describe",
            "end_time",
            "status",
            "judge_teachers_info",
            "students_visible",
            "questions_detail",
            "questions",
            "scheduled_publish_time",
        ]

        extra_kwargs = {
            "title": {"required": False},
            "types": {"required": False},
            "describe": {"required": False},
            "status": {"required": False},
            "judge_teachers_info": {"required": False},
        }

        def validate_end_time(self, end_time):
            if end_time.replace(tzinfo=utc) < datetime.datetime.now().replace(
                tzinfo=utc
            ):
                raise serializers.ValidationError("任务截止时间不能早于当前!!!")
            return end_time


class ProjectTaskForTeacherSerializer(serializers.ModelSerializer):
    """为老师提供的任务基本信息的序列化器"""

    submitted_count = serializers.SerializerMethodField()  # 已提交的人数
    marked_count = serializers.SerializerMethodField()  # 已批阅的人数
    student_total_count = serializers.SerializerMethodField()  # 学生总数
    types = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = ProjectTask
        exclude = ["questions_info", "judge_teachers_info", "project_id"]

    def get_types(self, data):
        return data.get_types_display()

    def get_status(self, data):
        return data.get_status_display()

    def get_submitted_count(self, data):
        return StudentProjectTaskInfo.objects.filter(
            project_task_id=data.id, status=STATUS.SUBMITTED
        ).count()

    def get_marked_count(self, data):
        return StudentProjectTaskInfo.objects.filter(
            project_task_id=data.id, status=STATUS.MARKED
        ).count()

    def get_student_total_count(self, data):
        return StudentProjectTaskInfo.objects.filter(project_task_id=data.id).count()


class ProjectTaskDetailForTeacherSerializer(serializers.ModelSerializer):
    """为老师提供的Task的详情序列化器"""

    questions_info = serializers.SerializerMethodField()
    submitted_count = serializers.SerializerMethodField()  # 已提交的人数
    marked_count = serializers.SerializerMethodField()  # 已批阅的人数
    student_total_count = serializers.SerializerMethodField()  # 学生总数
    student_info = serializers.SerializerMethodField()  # 学生信息列表
    marked_student_info = serializers.SerializerMethodField()  # # 已批阅的学生信息列表
    submitted_student_info = serializers.SerializerMethodField()  # 已提交的学生信息列表
    types = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = ProjectTask
        fields = "__all__"

    def get_types(self, data):
        return data.get_types_display()

    def get_status(self, data):
        return data.get_status_display()

    def get_submitted_count(self, data):
        return StudentProjectTaskInfo.objects.filter(
            project_task_id=data.id, status=STATUS.SUBMITTED
        ).count()

    def get_marked_count(self, data):
        return StudentProjectTaskInfo.objects.filter(
            project_task_id=data.id, status=STATUS.MARKED
        ).count()

    def get_student_total_count(self, data):
        return StudentProjectTaskInfo.objects.filter(project_task_id=data.id).count()

    def get_student_info(self, data):
        student_id_list = list(
            StudentProjectTaskInfo.objects.filter(project_task_id=data.id).values_list(
                "student_id", flat=True
            )
        )
        student_name_list = list(
            User.objects.filter(id__in=student_id_list).values_list("name", flat=True)
        )

        student_info = []

        for student_id, student_name in zip(student_id_list, student_name_list):
            single_info = {
                "student_id": student_id,
                "student_name": student_name,
            }
            student_info.append(single_info)

        return student_info

    def get_submitted_student_info(self, data):
        student_id_list = list(
            StudentProjectTaskInfo.objects.filter(
                project_task_id=data.id,
                status=STATUS.SUBMITTED,
            ).values_list("student_id", flat=True)
        )

        student_name_list = list(
            User.objects.filter(id__in=student_id_list).values_list("name", flat=True)
        )

        student_info = []

        for student_id, student_name in zip(student_id_list, student_name_list):
            single_info = {
                "student_id": student_id,
                "student_name": student_name,
            }
            student_info.append(single_info)

        return student_info

    def get_marked_student_info(self, data):
        student_id_list = list(
            StudentProjectTaskInfo.objects.filter(
                project_task_id=data.id,
                status=STATUS.MARKED,
            ).values_list("student_id", flat=True)
        )

        student_name_list = list(
            User.objects.filter(id__in=student_id_list).values_list("name", flat=True)
        )

        student_info = []

        for student_id, student_name in zip(student_id_list, student_name_list):
            single_info = {
                "student_id": student_id,
                "student_name": student_name,
            }
            student_info.append(single_info)

        return student_info

    def get_questions_info(self, data):
        raw_questions_info = data.questions_info

        question_id_list = []
        for item in raw_questions_info:
            question_id_list.append(item["id"])

        questions = Question.objects.filter(id__in=question_id_list)
        questions_info = QuestionShowSerializer(questions, many=True)

        question_index = 0
        for item in questions_info.data:
            item.update(raw_questions_info[question_index])
            question_index += 1

        return questions_info.data


class ProjectTaskInfoForStuSerializer(serializers.ModelSerializer):
    """为学生提供的任务基本信息的序列化器"""

    types = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = ProjectTask
        exclude = ["questions_info", "judge_teachers_info"]

    def get_types(self, data):
        return data.get_types_display()

    def get_status(self, data):
        return data.get_status_display()


class ProjectTaskDetailForStuHasNotSubmitSerializer(serializers.ModelSerializer):
    """学生任务状态不为已提交时的任务详情序列化器"""

    questions_info = serializers.SerializerMethodField()
    judge_teachers_info = serializers.SerializerMethodField()
    types = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = ProjectTask
        fields = "__all__"

    def get_types(self, data):
        return data.get_types_display()

    def get_status(self, data):
        return data.get_status_display()

    def get_questions_info(self, data):
        raw_questions_info = data.questions_info

        question_id_list = []
        for item in raw_questions_info:
            question_id_list.append(item["id"])

        questions = Question.objects.filter(id__in=question_id_list)
        questions_info = QuestionShowSerializer(questions, many=True)

        question_index = 0
        for item in questions_info.data:
            item.update(raw_questions_info[question_index])
            item.pop("answer")
            item.pop("answer_file")
            item.pop("explain")
            item.pop("explain_file")
            question_index += 1

        return questions_info.data

    def get_judge_teachers_info(self, data):
        if data.students_visible:
            return data.judge_teachers_info
        else:
            return "老师评分信息不可见"


class ProjectTaskDetailForStuHasSubmitSerializer(serializers.ModelSerializer):
    """学生任务状态为已提交时的任务详情序列化器"""

    questions_info = serializers.SerializerMethodField()
    judge_teachers_info = serializers.SerializerMethodField()
    types = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = ProjectTask
        fields = "__all__"

    def get_types(self, data):
        return data.get_types_display()

    def get_status(self, data):
        return data.get_status_display()

    def get_questions_info(self, data):
        raw_questions_info = data.questions_info

        question_id_list = []
        for item in raw_questions_info:
            question_id_list.append(item["id"])

        questions = Question.objects.filter(id__in=question_id_list)
        questions_info = QuestionShowSerializer(questions, many=True)

        question_index = 0
        for item in questions_info.data:
            item.update(raw_questions_info[question_index])
            question_index += 1

        return questions_info.data

    def get_judge_teachers_info(self, data):
        if data.students_visible:
            return data.judge_teachers_info
        else:
            return "老师评分信息不可见"


class TaskCreateSerializer(serializers.Serializer):
    """
    创建课程的序列化器
    """

    class TASK_TYPES:
        DAILY = "DAILY"
        ASSESSMENT = "ASSESSMENT"

    questions = QuestionSerializer(many=True)
    students = serializers.ListField(child=serializers.IntegerField())
    questions_detail = serializers.ListField(child=serializers.DictField())

    project_id = serializers.IntegerField()
    types = serializers.ChoiceField(
        choices=((TASK_TYPES.DAILY, "日常任务"), (TASK_TYPES.ASSESSMENT, "考核任务"))
    )
    title = serializers.CharField(max_length=255)
    describe = serializers.CharField(max_length=255)
    start_time = serializers.DateTimeField(required=False)
    end_time = serializers.DateTimeField(required=False)
    status = serializers.ChoiceField(
        choices=((TASK_STATUS.DRAFT, "草稿"), (TASK_STATUS.RELEASE, "已发布")),
        default=TASK_STATUS.DRAFT,
    )
    judge_teachers_info = serializers.JSONField()
    students_visible = serializers.BooleanField(required=False)
    creator = serializers.CharField(required=False)
    creator_id = serializers.IntegerField(required=False)

    def validate_end_time(self, end_time):
        if end_time.replace(tzinfo=utc) < datetime.datetime.now().replace(tzinfo=utc):
            raise serializers.ValidationError("任务截止时间不能早于当前!!!")
        return end_time


class StudentProjectTaskInfoSerializer(serializers.ModelSerializer):
    """normal的Relation序列化器"""

    class Meta:
        model = StudentProjectTaskInfo
        exclude = ["id"]


class StudentProjectTaskInfoShowSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    cumulative_time_seconds = serializers.SerializerMethodField()

    class Meta:
        model = StudentProjectTaskInfo
        exclude = ["id"]

    def get_status(self, relation):
        return relation.get_status_display()

    def get_cumulative_time_seconds(self, relation):
        return int(relation.cumulative_time.total_seconds())


class StudentProjectTaskInfoForStuSerializer(serializers.ModelSerializer):
    """老师评分开启匿名时的Relation序列化器"""

    individual_score = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    cumulative_time_seconds = serializers.SerializerMethodField()

    class Meta:
        model = StudentProjectTaskInfo
        exclude = ["id"]

    def get_status(self, relation):
        return relation.get_status_display()

    def get_individual_score(self, relation):
        individual_score = relation.individual_score
        for item in individual_score:
            item.pop("teacher_name")
            item.pop("teacher_id")
        return individual_score

    def get_cumulative_time_seconds(self, relation):
        return int(relation.cumulative_time.total_seconds())


class ProjectSearchInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProjectTaskInfo
        fields = [
            "project_id",
            "project_task_id",
            "student_id",
            "individual_score",
            "total_score",
        ]
        extra_kwargs = {
            "creator": {"required": False},
            "updater": {"required": False},
            "individual_score": {"required": False},
            "total_score": {"required": False},
        }


class StudentPerformTaskSerializer(serializers.ModelSerializer):
    """学生答题使用的序列化器"""

    stu_answers = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = StudentProjectTaskInfo
        fields = [
            "stu_answers",
            "cumulative_time",
            "individual_score",
            "updater_id",
            "status",
            "student_id",
            "total_score",
        ]

        extra_kwargs = {
            "cumulative_time": {"required": False},
            "individual_score": {"required": False},
            "student_id": {"required": False},
            "updater_id": {"required": False},
            "total_score": {"required": False},
        }


class TeacherJudgeSerializer(serializers.Serializer):
    score_list = serializers.ListField(child=serializers.IntegerField())


class TaskDeleteSerializer(serializers.Serializer):
    task_id_list = serializers.ListField(child=serializers.IntegerField())


class CeleryTaskInfoCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CeleryTaskInfo
        fields = "__all__"


class TimeTransferSerializer(serializers.Serializer):
    scheduled_publish_time = serializers.DateTimeField()
