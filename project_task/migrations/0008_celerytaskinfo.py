# Generated by Django 3.2.4 on 2022-05-01 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project_task", "0007_alter_projecttask_questions_info"),
    ]

    operations = [
        migrations.CreateModel(
            name="CeleryTaskInfo",
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
                ("project_task_id", models.BigIntegerField(verbose_name="任务id")),
                (
                    "celery_task_id",
                    models.CharField(max_length=60, verbose_name="celery任务id"),
                ),
            ],
        ),
    ]
