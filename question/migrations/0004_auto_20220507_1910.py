# Generated by Django 3.2.4 on 2022-05-07 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("question", "0003_alter_questiontagcontact_question_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="question",
            name="answer_url",
        ),
        migrations.RemoveField(
            model_name="question",
            name="explain_url",
        ),
        migrations.RemoveField(
            model_name="question",
            name="question_url",
        ),
        migrations.AddField(
            model_name="question",
            name="answer_file",
            field=models.FileField(
                blank=True, null=True, upload_to="", verbose_name="问题答案文件"
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="explain_file",
            field=models.FileField(
                blank=True, null=True, upload_to="", verbose_name="答案解析文件"
            ),
        ),
        migrations.AddField(
            model_name="question",
            name="question_file",
            field=models.FileField(
                blank=True, null=True, upload_to="", verbose_name="题目文件"
            ),
        ),
    ]
