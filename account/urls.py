#!/usr/bin/env python
__author__ = 'tony'
from django.conf.urls import url
from . import views

urlpatterns = [

    url(r'user_regist/$', views.RegisterView.as_view(), name='user_regist'),
    url(r'user_login/$', views.LoginView.as_view(), name='user_login'),
    url(r'captcha/$', views.GetCaptchaView.as_view(), name='captcha'),
    url(r'send_mobile_code/$', views.SendMobileCode.as_view(), name='send_mobile_code'),
    url(r'profile/$', views.profile, name='profile'),
    url(r'user_logout/$', views.user_logout, name='user_logout'),
    url(r'user_edit/$', views.user_edit, name='user_edit'),
    url(r'bind_user_email/$', views.bind_user_email, name='bind_user_email'),
    url(r'auth_user_email/$', views.auth_user_email, name='auth_user_email'),
    url(r'upload_avatar/$', views.upload_avatar, name='upload_avatar'),
]
