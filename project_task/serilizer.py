from django.db import transaction
from rest_framework import serializers
from rest_framework.response import Response

from project_task.models import ProjectTask, StudentProjectTaskInfo
from question.serializer import QuestionSerializer


class ProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = "__all__"


class TaskCreateSerializer(serializers.Serializer):
    questions = QuestionSerializer(many=True)
    students = serializers.ListField(child=serializers.IntegerField())
    questions_id_order_scores = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField())
    )

    project_id = serializers.IntegerField()
    types = serializers.CharField(max_length=10)
    title = serializers.CharField(max_length=255)
    describe = serializers.CharField(max_length=255)
    start_time = serializers.DateTimeField(required=False)
    end_time = serializers.DateTimeField(required=False)
    status = serializers.CharField(max_length=10)
    judge_teachers_weight = serializers.JSONField()
    students_visible = serializers.BooleanField(required=False)
    creator = serializers.CharField(required=False)
    creator_id = serializers.IntegerField(required=False)

    def create(self, validated_data):
        questions_id_order_scores = validated_data.pop("questions_id_order_scores")
        questions_temp = validated_data.pop("questions")

        project_id = validated_data["project_id"]
        id = validated_data.pop("creator_id")

        validated_data["updater"] = validated_data["creator"]
        with transaction.atomic():
            save = transaction.savepoint()

            # 确保问题的项目id何project的项目id一致
            for i in range(len(questions_temp)):
                questions_temp[i]["project_id"] = project_id
            questions = QuestionSerializer(data=questions_temp, many=True)
            questions.is_valid(raise_exception=True)
            questions_id_list = questions.save()

            questions_info = {}
            try:
                for i in range(len(questions_id_list)):
                    questions_temp = {
                        questions_id_list[i].id: questions_id_order_scores[i]
                    }
                    questions_info.update(questions_temp)
            except IndexError:
                return Response("答案与答案分数个数不匹配", exception=True)

            validated_data["questions_info"] = questions_info
            task = ProjectTaskSerializer(data=validated_data)
            task.is_valid(raise_exception=True)
            task_temp = task.save()

            relation = []
            for i in validated_data["students"]:
                temp = {
                    "student_id": i,
                    "project_id": validated_data.get("project_id"),
                    "project_task_id": task_temp.id,
                    "creator_id": id,
                    "updator_id": id,
                }
                relation.append(temp)
            taskinfo = StudentProjectTaskInfoSerializer(data=relation, many=True)
            taskinfo.is_valid(raise_exception=True)
            taskinfo.save()

        transaction.savepoint_commit(save)
        return task_temp


class StudentProjectTaskInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProjectTaskInfo
        exclude = ["id"]


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
