# Generated by Django 3.2.4 on 2022-05-02 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project_task", "0008_celerytaskinfo"),
    ]

    operations = [
        migrations.AddField(
            model_name="celerytaskinfo",
            name="celery_task_type",
            field=models.CharField(
                choices=[("AUTO_SUBMIT", "自动提交任务"), ("SCHEDULED_PUBLISH", "定时发布任务")],
                default="AUTO_SUBMIT",
                max_length=30,
                verbose_name="celery任务类型",
            ),
            preserve_default=False,
        ),
    ]
