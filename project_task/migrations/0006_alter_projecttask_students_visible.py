# Generated by Django 3.2.4 on 2022-04-29 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("project_task", "0005_auto_20220429_1027"),
    ]

    operations = [
        migrations.AlterField(
            model_name="projecttask",
            name="students_visible",
            field=models.BooleanField(default=False, verbose_name="导师评分学生是否可见"),
        ),
    ]
