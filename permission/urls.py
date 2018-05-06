#!/usr/bin/env python
__author__ = 'tony'
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'manage/$', views.manage, name='manage'),
    url(r'role_add_permission/$', views.role_add_permission, name='role_add_permission'),
    url(r'user_add_role/$', views.user_add_role, name='user_add_role'),
    url(r'add_role/$', views.add_role, name='add_role'),
    url(r'add_menu/$', views.add_menu, name='add_menu'),
    url(r'add_permission/$', views.add_permission, name='add_permission'),
    url(r'del_role/$', views.del_role, name='del_role'),
    url(r'del_permission/$', views.del_permission, name='del_permission'),
]
