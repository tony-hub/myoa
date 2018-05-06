#!/usr/bin/env python
__author__ = 'tony'
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'article_list/$', views.article_list, name='article_list'),
    url(r'add_article/$', views.add_article, name='add_article'),
    url(r'add_category_tag/$', views.add_category_tag, name='add_category_tag'),
    url(r'del_category_tag/$', views.del_category_tag, name='del_category_tag'),
    url(r'article_modify_list/$', views.article_modify_list, name='article_modify_list'),
]
