from django.conf.urls import url
from weixin import views


urlpatterns = [
    url(r'login', views.is_bind_wxuser),
    url(r'authenticate', views.verify_schooluser),
]