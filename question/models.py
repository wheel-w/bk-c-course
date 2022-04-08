from django.db import models

# Create your models here.
from django.utils import timezone


class Question(models.Model):
    class QuestionTypes:
        SINGLE = 'SINGLE'
        MULTIPLE = 'MULTIPLE'
        COMPLETION = 'COMPLETION'
        JUDGE = 'JUDGE'
        SHORT_ANSWER = 'SHORT_ANSWER'

    TYPES = [
        (QuestionTypes.SINGLE, '单选题'),
        (QuestionTypes.MULTIPLE, '多选题'),
        (QuestionTypes.COMPLETION, '填空题'),
        (QuestionTypes.JUDGE, '判断题'),
        (QuestionTypes.SHORT_ANSWER, '简答题'),
    ]

    course_id = models.IntegerField('题目所属课程id')
    chapter_id = models.IntegerField('题目所属章节id')
    types = models.CharField('题目类型', max_length=20, choices=TYPES)
    question = models.TextField('题目')
    question_url = models.TextField('题目文件url', null=True, blank=True)
    option_A = models.TextField('选项A', blank=True, null=True)
    option_B = models.TextField('选项B', blank=True, null=True)
    option_C = models.TextField('选项C', blank=True, null=True)
    option_D = models.TextField('选项D', blank=True, null=True)
    option_E = models.TextField('选项E', blank=True, null=True)
    answer = models.TextField('问题答案')
    answer_url = models.TextField('问题答案文件url', null=True, blank=True)
    explain = models.TextField('答案解析', blank=True, null=True, default='无')
    explain_url = models.TextField('答案解析文件url', null=True, blank=True)


class QuestionTag(models.Model):
    tag_value = models.CharField("标签值", max_length=20)
    tag_color = models.CharField("标签颜色", max_length=7)
    tag_text = models.CharField("标签说明", max_length=200)
    is_built_in = models.BooleanField("是否内置", default=False)
    sub_project = models.CharField("所属项目", max_length=30)
    time_created = models.DateTimeField("创建时间", default=timezone.now)
    time_updated = models.DateTimeField("修改时间", auto_now=True)

    class Meta:
        db_table = "question_tag_user"

    def __str__(self):
        return "{}".format(self.tag_value)


class QuestionTagContact(models.Model):
    user_id = models.BigIntegerField("用户id")
    tag_id = models.BigIntegerField("标签id")

    class Meta:
        db_table = "question_tag"

    def __str__(self):
        return "{}-{}".format(self.user_id, self.tag_id)
