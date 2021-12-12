# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = (
    url(r"^$", views.course_find),
    url(r"^$", views.course_alter),
    url(r"^$", views.course_add),
    url(r"^$", views.course_delete),
)
