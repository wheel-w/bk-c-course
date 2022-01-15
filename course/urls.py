# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = (
    url(r"^update_user_info/$", views.update_user_info, name="update_user_info"),
    url(r"^manage_course/$", views.manage_course),  # 课程的增删改
    url(r"^find_courses/$", views.search_courses_by_userid),  # 查询课程所有信息
    url(r"^show_course_names/$", views.show_course_names),  # 返回课程名称的下拉列表
)
