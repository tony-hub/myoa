#!/usr/bin/env python
# -*- coding: utf-8 -*-
#__author__ = 'tony'
from models import Category, Tag, Article


def add_tag_category_lib(category_name, tag_name):
    if category_name is not None:
        Category.objects.create(name=category_name)
        return {'status': True, 'msg': u'分类添加成功'}
    if tag_name is not None:
        Tag.objects.create(name=tag_name)
        return {'status': True, 'msg': u'标签添加成功'}
    return {'status': False, 'msg': u'参数不能为空'}


def tag_category():
    tags = Tag.by_all()
    categorys = Category.by_all()
    return {'tags': tags, 'categorys': categorys}


def del_category_tag_lib(c_uuid, t_uuid):
    if c_uuid is not None:
        category = Category.by_uuid(c_uuid)
        category.delete()
        return {'status': True, 'msg': u'分类删除成功'}
    if t_uuid is not None:
        tag = Tag.by_uuid(t_uuid)
        tag.delete()
        return {'status': True, 'msg': u'标签删除成功'}
    return {'status': False, 'msg': u'参数不能为空'}


def add_article_lib(title, article, desc, category, thumbnail, tags, article_id):
    article = Article()
    article.title = title
    article.content = article
    article.desc = desc
    article.category = category
    article.thumbnail = thumbnail
    article.tags = tags