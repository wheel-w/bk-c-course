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

from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.response import Response

from question.models import Question

from .models import ProjectTask, StudentProjectTaskInfo
from .serializer import (
    StudentPerformTaskSerializer,
    StudentProjectTaskInfoSerializer,
    TeacherJudgeSerializer,
)


# 答题和判卷的视图集
class PerformAndJudgeViewSet(viewsets.ViewSet):
    queryset = StudentProjectTaskInfo.objects.all()
    serializer_class = StudentPerformTaskSerializer

    @swagger_auto_schema(
        operation_summary="获取所有关系表",
    )
    def get_all_info(self, request, *args, **kwargs):
        task_id = kwargs["project_task_id"]
        data = StudentProjectTaskInfo.objects.filter(
            Q(project_task_id=task_id), Q(status="SUBMITTED") | Q(status="MARKED")
        )
        serializer = StudentProjectTaskInfoSerializer(data, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="获取学生关系表",
    )
    def get_stu_info(self, request, *args, **kwargs):
        task_id = kwargs["project_task_id"]
        stu_id = kwargs["student_id"]
        try:
            data = StudentProjectTaskInfo.objects.get(
                Q(project_task_id=task_id),
                Q(student_id=stu_id),
                Q(status="SUBMITTED") | Q(status="MARKED"),
            )
        except StudentProjectTaskInfo.DoesNotExist:
            return Response("ERROR", exception=True)

        serializer = StudentProjectTaskInfoSerializer(data)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="获取学生个人关系表（不传id）",
    )
    def get_individual_info(self, request, *args, **kwargs):
        task_id = kwargs["project_task_id"]
        data = StudentProjectTaskInfo.objects.get(
            project_task_id=task_id, student_id=request.user.id
        )
        serializer = StudentProjectTaskInfoSerializer(data)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=StudentPerformTaskSerializer,
        operation_summary="学生答题, 提交",
    )
    def perform_task(self, request, *args, **kwargs):
        task_id = kwargs["project_task_id"]

        request.data["updater_id"] = request.user.id
        student_id = request.user.id

        data = request.data
        relation_info = StudentProjectTaskInfo.objects.get(
            student_id=student_id, project_task_id=task_id
        )

        # 更改状态 已保存 ----> 已提交
        if data["status"] == "SUBMITTED":
            if relation_info.status == "SAVED":
                temp = StudentPerformTaskSerializer(relation_info, data)
                temp.is_valid(raise_exception=True)
                temp.save()
                return Response()
            else:
                return Response("ERROR", exception=True)

        task_info = ProjectTask.objects.get(id=relation_info.project_task_id)
        questions_info = task_info.questions_info
        question_id_list = list(questions_info.keys())
        # 问题的分值
        questions_score = []

        # 批阅老师信息
        judge_teachers_info = task_info.judge_teachers_info

        # 整理 question_info
        for question_info in questions_info.values():
            for score in question_info.values():
                questions_score.append(score)

        # question's type and answer
        question_type_ans_list = list(
            Question.objects.filter(id__in=question_id_list).values_list(
                "types", "answer"
            )
        )

        stu_answers = data["stu_answers"]
        individual_score = []

        for teacher_id, teacher_weight in judge_teachers_info.items():
            score = []
            question_index = 0
            for answer, question in zip(stu_answers, question_type_ans_list):
                if question[0] == "SINGLE" or "JUDGE" or "MULTIPLE":
                    if answer == question[1]:
                        score.append(questions_score[question_index])
                    else:
                        score.append(0)
                else:
                    # -1 代表未批改
                    score.append(-1)
                question_index += 1
            score_info = {
                "teacher_id": int(teacher_id),
                "teacher_weight": float(teacher_weight),
                "is_judge": False,
                "score": score,
            }
            individual_score.append(score_info)

        data["individual_score"] = individual_score

        perform_info = StudentPerformTaskSerializer(relation_info, data)
        perform_info.is_valid(raise_exception=True)
        perform_info.save()

        return Response()

    @swagger_auto_schema(
        request_body=TeacherJudgeSerializer,
        operation_summary="老师判卷",
    )
    def judge_task(self, request, *args, **kwargs):
        task_id = kwargs["project_task_id"]
        request.data["updater_id"] = request.user.id
        data = request.data

        relation_info = StudentProjectTaskInfo.objects.get(
            student_id=data["student_id"], project_task_id=task_id
        )

        individual_score = relation_info.individual_score

        for item in individual_score:
            if item["teacher_id"] == request.user.id:
                item["score"] = data["score_list"]
                item["is_judge"] = True
                break

        if all(item["is_judge"] for item in individual_score):
            total_score = 0.0
            for item in individual_score:
                total_score += sum(item["score"]) * item["teacher_weight"]

            judge_info = {
                "status": "MARKED",
                "total_score": total_score,
                "individual_score": individual_score,
                "updater_id": request.user.id,
            }
        else:
            judge_info = {
                "individual_score": individual_score,
                "updater_id": request.user.id,
            }

        ret = StudentPerformTaskSerializer(relation_info, judge_info)
        ret.is_valid(raise_exception=True)
        ret.save()

        return Response()
