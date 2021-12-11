from django.db import models


# Create your models here.
class Course(models.Model):
    course_name = models.CharField("课程名称", max_length=90)
    course_introduction = models.TextField("课程简介", blank=True, null=True)
    teacher = models.CharField("教师姓名", max_length=90)
    create_people = models.CharField("创建人", max_length=90)
    manage_student = models.TextField("学生管理员", null=True, blank=True)


class UserCourseContact(models.Model):
    user_id = models.IntegerField("用户id")
    course_id = models.IntegerField("课程id")


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

    username = models.CharField("saas用户名", max_length=50)
    openid = models.CharField("wechat唯一标识", max_length=50, blank=True, null=True)
    class_number = models.CharField("学号/工号", max_length=30, blank=True, null=True)
    name = models.CharField("姓名", max_length=30)

    professional_class = models.CharField("专业班级", max_length=30, blank=True, null=True)

    gender = models.CharField(max_length=20, choices=GENDER,)
    identity = models.CharField(max_length=20, choices=IDENTITY, default=Identity.NOT_CERTIFIED)

    phone_number = models.CharField("手机号", max_length=30, blank=True, null=True)
    email_number = models.EmailField("邮箱", max_length=50, blank=True, null=True)
    qq_number = models.CharField("QQ号", max_length=30, blank=True, null=True)
    wechat_number = models.CharField("微信号", max_length=50, blank=True, null=True)
