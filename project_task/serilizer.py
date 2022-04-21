from rest_framework import serializers

from project_task.models import ProjectTask, StudentProjectTaskInfo
from question.serializer import QuestionSerializer


class ProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = "__all__"


class TaskCreateSerializer(ProjectTaskSerializer):
    """
    供创建让任务时候的Swagger使用
    """

    questions = QuestionSerializer(many=True)
    students = serializers.ListField()


class StudentProjectTaskInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProjectTaskInfo
        exclude = ["id"]
        # extra_kwargs = {
        #     "creator": {"required": False},
        #     "updater": {"required": False},
        #     "time_created": {"required": False},
        #     "time_updated": {"required": False},
        #     "individual_score": {"required": False},
        #     "total_score": {"required": False},
        #     "cumulative_time": {"required": False},
        # }


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


# class TaskCreateSerializer(serializers.ModelSerializer):
#     questions = serializers.ListField()
#     class Meta:
#         model = ProjectTask
#         fields = "__all__"
#         extra_kwargs = {
#             "creator": {"required": False},
#             "updater": {"required": False},
#             "time_created": {"required": False},
#             "time_updated": {"required": False},
#         }
