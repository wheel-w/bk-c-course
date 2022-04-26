from rest_framework import serializers

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
    judge_teachers_info = serializers.JSONField()
    students_visible = serializers.BooleanField(required=False)
    creator = serializers.CharField(required=False)
    creator_id = serializers.IntegerField(required=False)


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
