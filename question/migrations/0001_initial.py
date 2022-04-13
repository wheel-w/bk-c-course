# Generated by Django 3.2.4 on 2022-04-13 09:41

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("course_id", models.IntegerField(verbose_name="题目所属课程id")),
                (
                    "types",
                    models.CharField(
                        choices=[
                            ("SINGLE", "单选题"),
                            ("MULTIPLE", "多选题"),
                            ("COMPLETION", "填空题"),
                            ("JUDGE", "判断题"),
                            ("SHORT_ANSWER", "简答题"),
                        ],
                        max_length=20,
                        verbose_name="题目类型",
                    ),
                ),
                ("question", models.TextField(verbose_name="题目")),
                (
                    "question_url",
                    models.TextField(blank=True, null=True, verbose_name="题目文件url"),
                ),
                (
                    "option_A",
                    models.TextField(blank=True, null=True, verbose_name="选项A"),
                ),
                (
                    "option_B",
                    models.TextField(blank=True, null=True, verbose_name="选项B"),
                ),
                (
                    "option_C",
                    models.TextField(blank=True, null=True, verbose_name="选项C"),
                ),
                (
                    "option_D",
                    models.TextField(blank=True, null=True, verbose_name="选项D"),
                ),
                (
                    "option_E",
                    models.TextField(blank=True, null=True, verbose_name="选项E"),
                ),
                ("answer", models.TextField(verbose_name="问题答案")),
                (
                    "answer_url",
                    models.TextField(blank=True, null=True, verbose_name="问题答案文件url"),
                ),
                (
                    "explain",
                    models.TextField(
                        blank=True, default="无", null=True, verbose_name="答案解析"
                    ),
                ),
                (
                    "explain_url",
                    models.TextField(blank=True, null=True, verbose_name="答案解析文件url"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuestionTag",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.CharField(max_length=20, verbose_name="标签值")),
                ("color", models.CharField(max_length=7, verbose_name="标签颜色")),
                ("text", models.CharField(max_length=200, verbose_name="标签说明")),
                (
                    "time_created",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="创建时间"
                    ),
                ),
                (
                    "time_updated",
                    models.DateTimeField(auto_now=True, verbose_name="修改时间"),
                ),
            ],
        ),
        migrations.CreateModel(
            name="QuestionTagContact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.BigIntegerField(verbose_name="用户id")),
                ("tag_id", models.BigIntegerField(verbose_name="标签id")),
            ],
        ),
    ]
