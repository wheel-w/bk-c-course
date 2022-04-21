# Generated by Django 3.2.4 on 2022-04-21 07:50

import re

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project_task", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="projecttask",
            old_name="judge_teachers",
            new_name="judge_teachers_weight",
        ),
        migrations.RemoveField(
            model_name="projecttask",
            name="create_time",
        ),
        migrations.RemoveField(
            model_name="projecttask",
            name="question_order",
        ),
        migrations.AddField(
            model_name="projecttask",
            name="questions_order",
            field=models.CharField(
                blank=True,
                default="",
                max_length=200,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^\\d+(?:\\,\\d+)*\\Z"),
                        code="invalid",
                        message="Enter only digits separated by commas.",
                    )
                ],
                verbose_name="存储题目id及其顺序",
            ),
        ),
        migrations.AddField(
            model_name="projecttask",
            name="questions_score",
            field=models.CharField(
                blank=True,
                default="",
                max_length=200,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        re.compile("^\\d+(?:\\,\\d+)*\\Z"),
                        code="invalid",
                        message="Enter only digits separated by commas.",
                    )
                ],
                verbose_name="每个题目的单独分数",
            ),
        ),
        migrations.AlterField(
            model_name="projecttask",
            name="end_time",
            field=models.DateTimeField(blank=True, null=True, verbose_name="任务截止时间"),
        ),
        migrations.AlterField(
            model_name="projecttask",
            name="start_time",
            field=models.DateTimeField(blank=True, null=True, verbose_name="任务开始时间"),
        ),
        migrations.AlterField(
            model_name="projecttask",
            name="time_created",
            field=models.DateTimeField(auto_now_add=True, verbose_name="任务创建时间"),
        ),
        migrations.AlterField(
            model_name="projecttask",
            name="time_updated",
            field=models.DateTimeField(auto_now=True, verbose_name="任务更新时间"),
        ),
        migrations.AlterField(
            model_name="studentprojecttaskinfo",
            name="individual_score",
            field=models.JSONField(blank=True, null=True, verbose_name="学生题目单项得分"),
        ),
        migrations.AlterField(
            model_name="studentprojecttaskinfo",
            name="status",
            field=models.CharField(
                choices=[
                    ("NOT_ANSWER", "未答题"),
                    ("SAVED", "已保存"),
                    ("SUBMITTED", "已提交"),
                    ("MARKED", "已批改"),
                    ("CANCEL", "已撤销"),
                ],
                default="NOT_ANSWER",
                max_length=10,
                verbose_name="学生完成任务状态",
            ),
        ),
        migrations.AlterField(
            model_name="studentprojecttaskinfo",
            name="stu_answers",
            field=models.JSONField(blank=True, null=True, verbose_name="学生提交答案列表"),
        ),
    ]
