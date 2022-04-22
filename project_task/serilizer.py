from rest_framework import serializers

from project_task.models import ProjectTask, StudentProjectTaskInfo
from question.serializer import QuestionSerializer


class ProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = "__all__"

    def validate_questions_id_order_scores(self, data):
        flag = 1
        for i in data:
            d = list(i.values())[0]
            try:
                int(dict(d)[str(flag)])
            except ValueError:
                raise serializers.ValidationError("问题分数-参数校验错误")
            except KeyError:
                raise serializers.ValidationError("问题顺序-参数校验错误")
            flag += 1
        return data


class TaskCreateSerializer(ProjectTaskSerializer):
    """
    供创建让任务时候的Swagger使用
    """

    questions = QuestionSerializer(many=True)
    questions_order_scores = serializers.ListField()
    students = serializers.ListField()


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
