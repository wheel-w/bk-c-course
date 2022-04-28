from rest_framework import serializers

from project_task.models import ProjectTask, StudentProjectTaskInfo
from question.models import Question
from question.serializer import QuestionSerializer


class ProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = "__all__"


class ProjectTaskDetailSerializer(serializers.ModelSerializer):
    questions_info = serializers.SerializerMethodField()

    class Meta:
        model = ProjectTask
        fields = "__all__"

    def get_questions_info(self, data):
        raw_questions_info = data.questions_info

        question_score_list = []
        for item in raw_questions_info.values():
            for score in item.values():
                question_score_list.append(score)

        question_id_list = list(raw_questions_info.keys())
        questions = Question.objects.filter(id__in=question_id_list)
        questions_info = QuestionSerializer(questions, many=True)

        question_index = 0
        for item in questions_info.data:
            item["question_score"] = question_score_list[question_index]
            question_index += 1

        return questions_info.data


class ProjectTaskDetailForStuSerializer(serializers.ModelSerializer):
    questions_info = serializers.SerializerMethodField()

    class Meta:
        model = ProjectTask
        fields = "__all__"

    def get_questions_info(self, data):
        raw_questions_info = data.questions_info

        question_score_list = []
        for item in raw_questions_info.values():
            for score in item.values():
                question_score_list.append(score)

        question_id_list = list(raw_questions_info.keys())
        questions = Question.objects.filter(id__in=question_id_list)
        questions_info = QuestionSerializer(questions, many=True)

        question_index = 0
        for item in questions_info.data:
            item["question_score"] = question_score_list[question_index]
            item.pop("answer")
            item.pop("answer_url")
            item.pop("explain")
            item.pop("explain_url")
            question_index += 1

        return questions_info.data


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


class StudentProjectTaskInfoForStuSerializer(serializers.ModelSerializer):
    individual_score = serializers.SerializerMethodField()

    class Meta:
        model = StudentProjectTaskInfo
        exclude = ["id"]

    def get_individual_score(self, relation):
        print(relation.individual_score)
        individual_score = relation.individual_score
        for item in individual_score:
            item.pop("teacher_name")
        return individual_score


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
    score_list = serializers.ListField(child=serializers.IntegerField())
