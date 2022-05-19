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

import logging

from celery.task import task

from project_task.constants import SCORE, TYPES
from project_task.models import ProjectTask, StudentProjectTaskInfo
from project_task.serializer import StudentPerformTaskSerializer
from question.models import Question

logger = logging.getLogger("root")


# 客观题评分
@task()
def judge_objective(relation_id):
    logger.info("客观题评分任务开始执行")
    relation_info = StudentProjectTaskInfo.objects.get(id=relation_id)
    task_info = ProjectTask.objects.get(id=relation_info.project_task_id)

    # 批阅老师信息
    judge_teachers_info = task_info.judge_teachers_info

    questions_info = task_info.questions_info
    question_id_list = [item["id"] for item in questions_info]

    # question's type and answer
    question_type_ans_list = list(
        Question.objects.filter(id__in=question_id_list).values_list("types", "answer")
    )

    stu_answers = relation_info.stu_answers
    individual_score = []

    for teacher_info in judge_teachers_info:
        score = []
        question_index = 0
        # question[0]为题型,question[1]为答案
        for answer, question in zip(stu_answers, question_type_ans_list):
            if (
                question[0] == TYPES.SINGLE
                or question[0] == TYPES.JUDGE
                or question[0] == TYPES.MULTIPLE
            ):
                if answer == question[1]:
                    score.append(questions_info[question_index]["score"])
                else:
                    score.append(SCORE.WRONG)
            else:
                score.append(SCORE.NOT_JUDGE)
            question_index += 1

        score_info = {
            "teacher_id": teacher_info["id"],
            "teacher_weight": teacher_info["weight"],
            "teacher_name": "",
            "is_judge": False,
            "score": score,
        }
        individual_score.append(score_info)

    data = {
        "individual_score": individual_score,
    }

    perform_info = StudentPerformTaskSerializer(relation_info, data)
    perform_info.is_valid(raise_exception=True)
    perform_info.save()
    logger.info("客观题评分任务执行完毕")
