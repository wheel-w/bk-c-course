from django.db import models


class Project(models.Model):
    name = models.CharField("项目名称", max_length=90)
    introduction = models.TextField("项目简介", blank=True, null=True)
    property = models.CharField("项目性质", max_length=90)
    category = models.CharField("项目归属", max_length=90)
    organization = models.CharField("组织名称", max_length=90)
    creator = models.CharField("创建人", max_length=90)
    create_time = models.DateTimeField("项目创建时间", auto_now_add=True)
    update_time = models.DateTimeField("项目更新时间", auto_now=True)

    class Meta:
        db_table = "project"
        ordering = ["-update_time"]

    def __str__(self):
        return self.name
