# Generated by Django 3.2.4 on 2022-04-08 02:59

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0004_create_cache_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('u', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='account.user')),
                ('name', models.CharField(blank=True, max_length=20, null=True, verbose_name='姓名')),
                ('gender', models.CharField(blank=True, choices=[('MALE', '男'), ('FEMALE', '女')], max_length=20, null=True, verbose_name='性别')),
                ('phone_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='手机号')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='邮箱地址')),
                ('qq_number', models.CharField(blank=True, max_length=15, null=True, verbose_name='qq号')),
                ('vx_number', models.CharField(blank=True, max_length=15, null=True, verbose_name='vx号')),
                ('vx_open_id', models.CharField(blank=True, max_length=20, null=True, verbose_name='微信Open_id')),
                ('time_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('time_updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'db_table': 'u_user',
            },
        ),
        migrations.CreateModel(
            name='UserTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_value', models.CharField(max_length=20, verbose_name='标签值')),
                ('tag_color', models.CharField(max_length=7, verbose_name='标签颜色')),
                ('is_built_in', models.BooleanField(default=False, verbose_name='是否内置')),
                ('sub_project', models.CharField(max_length=30, verbose_name='所属项目')),
                ('time_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('time_updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'db_table': 'u_tag',
            },
        ),
        migrations.CreateModel(
            name='UserTagContact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(verbose_name='用户id')),
                ('tag_id', models.BigIntegerField(verbose_name='标签id')),
            ],
            options={
                'db_table': 'u_tag_user',
            },
        ),
    ]
