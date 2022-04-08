import django
from django.utils import timezone
from blueapps import account
from django.db import models


# Create your models here.


class User(models.Model):
    class Gender:
        MALE = "MALE"
        FEMALE = "FEMALE"

    GENDER = [
        (Gender.MALE, "男"),
        (Gender.FEMALE, "女")
    ]
    u = models.OneToOneField(auto_created=True, parent_link=True,
                             primary_key=True, serialize=False, on_delete=models.CASCADE, to='account.user')
    name = models.CharField('姓名', max_length=20, blank=True, null=True)
    gender = models.CharField('性别', max_length=20, choices=GENDER, blank=True, null=True)
    phone_number = models.CharField("手机号", max_length=30, blank=True, null=True)
    email = models.EmailField('邮箱地址', blank=True, null=True)
    qq_number = models.CharField("qq号", max_length=15, blank=True, null=True)
    vx_number = models.CharField('vx号', max_length=15, blank=True, null=True)
    vx_open_id = models.CharField('微信Open_id', max_length=20, blank=True, null=True)
    time_created = models.DateTimeField('创建时间', default=timezone.now)
    time_updated = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'u_user'


class UserTag(models.Model):
    tag_value = models.CharField("标签值", max_length=20)
    tag_color = models.CharField("标签颜色", max_length=7)
    is_built_in = models.BooleanField('是否内置', default=False)
    sub_project = models.CharField('所属项目', max_length=30)
    time_created = models.DateTimeField('创建时间', default=timezone.now)
    time_updated = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        db_table = 'u_tag'


class UserTagContact(models.Model):
    user_id = models.BigIntegerField("用户id")
    tag_id = models.BigIntegerField("标签id")

    class Meta:
        db_table = 'u_tag_user'

    def __str__(self):
        return "{}-{}".format(self.user_id, self.tag_id)
