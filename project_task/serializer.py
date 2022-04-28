from rest_framework import serializers

from project_task.models import ProjectTask, StudentProjectTaskInfo
from question.serializer import QuestionSerializer


class ProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = "__all__"


# 创建课程的序列化器
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


class StudentPerformTaskSerializer(serializers.ModelSerializer):
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
    student_id = serializers.IntegerField()
    score_list = serializers.ListField(child=serializers.IntegerField())
