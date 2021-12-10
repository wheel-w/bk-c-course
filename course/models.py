from django.db import models


# Create your models here.
class Course(models.Model):
    course_name = models.CharField("课程名称", max_length=90, blank=True)
    course_introduction = models.TextField("课程简介", blank=True)
    teacher = models.CharField("教师姓名", max_length=90)
    create_people = models.CharField("创建人", max_length=90)
    manage_student = models.TextField("学生管理员", null=True, blank=True)


class UserCourseContact(models.Model):
    user_id = models.IntegerField("用户id")
    course_id = models.IntegerField("课程id")
