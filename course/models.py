from django.db import models

# member属性列表
MEMBER_ATTR_LIST = ["username", "class_number", "name", "professional_class", "gender", "identity", "phone_number",
                    "email_number", "qq_number", "wechat_number"]


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

    username = models.CharField("saas用户名", max_length=50, unique=True)
    openid = models.CharField("wechat唯一标识", max_length=50, blank=True, null=True)
    class_number = models.CharField("学号/工号", max_length=30, unique=True, blank=True, null=True, )
    name = models.CharField("姓名", max_length=30, blank=True, null=True)
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
