from rest_framework import serializers

from project_task.models import ProjectTask, StudentProjectTaskInfo
from question.models import Question
from question.serializer import QuestionSerializer
from user_manager.models import User

from .constants import STATUS


class ProjectTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        fields = "__all__"


# 为老师提供的任务基本信息的序列化器
class ProjectTaskForTeacherSerializer(serializers.ModelSerializer):
    submitted_count = serializers.SerializerMethodField()  # 已提交的人数
    marked_count = serializers.SerializerMethodField()  # 已批阅的人数
    student_total_count = serializers.SerializerMethodField()  # 学生总数

    class Meta:
        model = ProjectTask
        exclude = ["questions_info", "judge_teachers_info", "project_id"]

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


# 为老师提供的Task的详情序列化器
class ProjectTaskDetailForTeacherSerializer(serializers.ModelSerializer):
    questions_info = serializers.SerializerMethodField()
    submitted_count = serializers.SerializerMethodField()  # 已提交的人数
    marked_count = serializers.SerializerMethodField()  # 已批阅的人数
    student_total_count = serializers.SerializerMethodField()  # 学生总数
    student_info = serializers.SerializerMethodField()  # 学生信息列表
    marked_student_info = serializers.SerializerMethodField()  # # 已批阅的学生信息列表
    submitted_student_info = serializers.SerializerMethodField()  # 已提交的学生信息列表

    class Meta:
        model = ProjectTask
        fields = "__all__"

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


# 为学生提供的任务基本信息的序列化器
class ProjectTaskInfoForStuSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectTask
        exclude = ["questions_info", "judge_teachers_info"]


# 学生任务状态不为已提交时的任务详情序列化器
class ProjectTaskDetailForStuHasNotSubmitSerializer(serializers.ModelSerializer):
    questions_info = serializers.SerializerMethodField()
    judge_teachers_info = serializers.SerializerMethodField()

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

    def get_judge_teachers_info(self, data):
        if data.students_visible:
            return data.judge_teachers_info
        else:
            return "老师评分信息不可见"


# 学生任务状态为已提交时的任务详情序列化器
class ProjectTaskDetailForStuHasSubmitSerializer(serializers.ModelSerializer):
    questions_info = serializers.SerializerMethodField()
    judge_teachers_info = serializers.SerializerMethodField()

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

    def get_judge_teachers_info(self, data):
        if data.students_visible:
            return data.judge_teachers_info
        else:
            return "老师评分信息不可见"


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


# normal的Relation序列化器
class StudentProjectTaskInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProjectTaskInfo
        exclude = ["id"]


# 老师评分开启匿名时的Relation序列化器
class StudentProjectTaskInfoForStuSerializer(serializers.ModelSerializer):
    individual_score = serializers.SerializerMethodField()

    class Meta:
        model = StudentProjectTaskInfo
        exclude = ["id"]

    def get_individual_score(self, relation):
        individual_score = relation.individual_score
        for item in individual_score:
            item.pop("teacher_name")
            item.pop("teacher_id")
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
