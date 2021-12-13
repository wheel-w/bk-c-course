# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = (
    url(r"^test/search/$", views.course_find),
    url(r"^test/alter/$", views.course_alter),
    url(r"^test/add/$", views.course_add),
    url(r"^test/delete/$", views.course_delete),
)