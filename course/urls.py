# -*- coding: utf-8 -*-

from django.conf.urls import url

from . import views

urlpatterns = (url(r"^manage_course/$", views.manage_course),)
