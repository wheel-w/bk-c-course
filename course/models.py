# Create your models here.
from django.db import models
from jsonfield import JSONField

# from picklefield.fields import PickledObjectField


# Create your models here.
class CourseTable(models.Model):
    course_id = models.AutoField("课程id", primary_key=True)  # 课程id
    course_name = models.CharField(
        "课程名称", max_length=90, null=True, blank=True, unique=True
    )  # 课程名称
    course_introduction = models.TextField("课程简介", blank=True)  # 课程简介
    teacher = JSONField("教师姓名", blank=False)
    create_people = JSONField("创建人", blank=False)
    manage_student = JSONField("学生管理员", null=True)


class CourseConnect(models.Model):
    connect_id = (models.AutoField("关系id", primary_key=True),)  # 关系id
    # user_id = models.ForeignKey(PersonInformation "用户id"),#这是用户表的唯一标识，跟用户表同步
    course_id = models.ForeignKey(CourseTable, "课程id")  # 这是课程表的唯一标识，跟课程表同步
