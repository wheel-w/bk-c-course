from datetime import timedelta

from django.db import models
from django_mysql.models import JSONField

# member属性列表
MEMBER_ATTR_LIST = ["id", "username", "class_number", "name", "college", "professional_class", "gender", "identity",
                    "phone_number", "email_number", "qq_number", "wechat_number"]


# Create your models here.
class Course(models.Model):
    course_name = models.CharField("课程名称", max_length=90)
    course_introduction = models.TextField("课程简介", blank=True, null=True)
    teacher = models.CharField("教师姓名", max_length=90)
    create_people = models.CharField("创建人", max_length=90)
    manage_student = models.TextField("学生管理员", null=True, blank=True)

    create_time = models.DateTimeField("课程创建时间", auto_now_add=True)
    update_time = models.DateTimeField("课程更新时间", auto_now=True)

    class Meta:
        db_table = "course"
        ordering = ["-update_time"]

    def __str__(self):
        return self.course_name


class UserCourseContact(models.Model):
    user_id = models.IntegerField("用户id")
    course_id = models.IntegerField("课程id")

    create_time = models.DateTimeField("成员加入课程时间", auto_now_add=True)

    class Meta:
        db_table = "user_course_contact"
        ordering = ["-create_time"]

    def __str__(self):
        return "{}-{}".format(self.user_id, self.course_id)


class Member(models.Model):
    class Gender:
        MAN = "MAN"
        WOMAN = "WOMAN"

    class Identity:
        TEACHER = "TEACHER"
        STUDENT = "STUDENT"
        NOT_CERTIFIED = "NOT_CERTIFIED"

    GENDER = [
        (Gender.MAN, "男"),
        (Gender.WOMAN, "女")
    ]
    IDENTITY = [
        (Identity.TEACHER, "老师"),
        (Identity.STUDENT, "学生"),
        (Identity.NOT_CERTIFIED, "未认证")
    ]

    username = models.CharField("saas用户名", max_length=50, unique=True, blank=True, null=True)
    openid = models.CharField("wechat唯一标识", max_length=50, blank=True, null=True, unique=True)
    class_number = models.CharField("学号/工号", max_length=30, unique=True, blank=True, null=True)
    name = models.CharField("姓名", max_length=30, blank=True, null=True)
    college = models.CharField("学院", max_length=40, blank=True, null=True)
    professional_class = models.CharField("专业班级", max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER, blank=True, null=True)
    identity = models.CharField(max_length=20, choices=IDENTITY, default=Identity.NOT_CERTIFIED)
    phone_number = models.CharField("手机号", max_length=30, blank=True, null=True)
    email_number = models.EmailField("邮箱", max_length=50, blank=True, null=True)
    qq_number = models.CharField("QQ号", max_length=30, blank=True, null=True)
    wechat_number = models.CharField("微信号", max_length=50, blank=True, null=True)

    create_time = models.DateTimeField("课程创建时间", auto_now_add=True)
    update_time = models.DateTimeField("课程更新时间", auto_now=True)

    class Meta:
        db_table = "member"
        ordering = ["class_number"]

    def __str__(self):
        return "{}({})".format(self.class_number, self.name)


class Chapter(models.Model):
    course_id = models.IntegerField('课程id')
    chapter_name = models.TextField('章节名称')


class Question(models.Model):
    class Types:
        SINGLE = 'SINGLE'
        MULTIPLE = 'MULTIPLE'
        COMPLETION = 'COMPLETION'
        JUDGE = 'JUDGE'
        SHORT_ANSWER = 'SHORT_ANSWER'

    TYPES = [
        (Types.SINGLE, '单选题'),
        (Types.MULTIPLE, '多选题'),
        (Types.COMPLETION, '填空题'),
        (Types.JUDGE, '判断题'),
        (Types.SHORT_ANSWER, '简答题'),
    ]

    course_id = models.IntegerField('题目所属课程id')
    chapter_id = models.IntegerField('题目所属章节id')
    types = models.CharField('题目类型', max_length=20, choices=TYPES)
    question = models.TextField('题目')
    option_A = models.TextField('选项A', blank=True, null=True)
    option_B = models.TextField('选项B', blank=True, null=True)
    option_C = models.TextField('选项C', blank=True, null=True)
    option_D = models.TextField('选项D', blank=True, null=True)
    option_E = models.TextField('选项E', blank=True, null=True)
    answer = models.TextField('问题答案')
    explain = models.TextField('答案解析', blank=True, null=True, default='无')


class Paper(models.Model):
    status_list = ['DRAFT', 'RELEASE', 'MARKED']

    class Types:
        EXERCISE = 'EXERCISE'
        EXAM = 'EXAM'

    class Status:
        DRAFT = 'DRAFT'
        RELEASE = 'RELEASE'
        MARKED = 'MARKED'

    TYPES = [
        (Types.EXERCISE, '练习卷'),
        (Types.EXAM, '测试卷')
    ]

    STATUS = [
        (Status.DRAFT, '草稿'),
        (Status.RELEASE, '已发布'),
        (Status.MARKED, '已批阅')
    ]

    types = models.CharField('试卷类型', max_length=10, choices=TYPES)
    course_id = models.IntegerField('卷子所属课程id')
    chapter_id = models.IntegerField('卷子所属章节id', blank=True, null=True)
    paper_name = models.CharField('卷子名字', max_length=255)
    teacher = models.CharField('教师姓名', max_length=90)
    question_order = JSONField('存储题目顺序的Json', default=None, blank=True, null=True)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    start_time = models.DateTimeField('开始时间', blank=True, null=True)
    end_time = models.DateTimeField('截至时间', blank=True, null=True)
    status = models.CharField('卷子状态', max_length=10, choices=STATUS)


class CustomType(models.Model):
    course_id = models.IntegerField('课程id')
    custom_type_name = models.TextField('题目类型名称')


class PaperQuestionContact(models.Model):
    paper_id = models.IntegerField('卷子id')
    types = models.CharField('题目类型', max_length=20, choices=Question.TYPES)
    score = models.FloatField('题目分数', default=1)
    question_id = models.IntegerField('题目id')
    question = models.TextField('题目')
    option_A = models.TextField('选项A', blank=True, null=True)
    option_B = models.TextField('选项B', blank=True, null=True)
    option_C = models.TextField('选项C', blank=True, null=True)
    option_D = models.TextField('选项D', blank=True, null=True)
    option_E = models.TextField('选项E', blank=True, null=True)
    answer = models.TextField('问题答案')
    explain = models.TextField('答案解析', blank=True, null=True, default='无')


class StudentAnswer(models.Model):
    student_id = models.IntegerField('学生id')
    PQContact_id = models.IntegerField('卷子与题目关联表单的id')
    answer = models.TextField('学生的作答', blank=True, null=True)
    score = models.FloatField('学生这道题的得分', blank=True, null=True, default=0)


class StudentPaperContact(models.Model):
    class Status:
        NOT_ANSWER = 'NOT_ANSWER'
        SAVED = 'SAVED'
        SUBMITTED = 'SUBMITTED'

    STATUS = [
        (Status.NOT_ANSWER, '未答题'),
        (Status.SAVED, '已保存'),
        (Status.SUBMITTED, '已提交')
    ]

    course_id = models.IntegerField('课程id')
    paper_id = models.IntegerField('卷子id')
    student_id = models.TextField('学生id')
    status = models.CharField('状态', max_length=10, choices=STATUS)
    score = models.FloatField('总分', blank=True, null=True, default=0)
    cumulative_time = models.DurationField('答题累计时间', default=timedelta(seconds=0))
