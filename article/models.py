# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from uuid import uuid4
from account.models import User


class Article(models.Model):
    """文章表"""
    uuid = models.UUIDField('uuid', unique=True, default=uuid4)
    title = models.CharField(u'标题', max_length=64, unique=True)
    content = models.TextField()
    createtime = models.DateTimeField(u'创建时间', auto_now_add=True)
    thumbnail = models.CharField(u'缩略图', max_length=64, unique=True)
    desc = models.CharField(u'简述', max_length=64)
    categorys = models.ForeignKey('Category', related_name='articles')
    comments = models.ForeignKey('Comment', related_name='articles')
    tags = models.ManyToManyField('Tag', related_name='articles')
    users = models.ForeignKey(User, related_name='articles')
    readnum = models.IntegerField(u'阅读次数', default=0)

    @classmethod
    def by_uuid(cls, uuid):
        return cls.objects.filter(uuid=uuid).first()

    @classmethod
    def by_id(cls, id):
        return cls.objects.filter(id=id).first()

    @classmethod
    def by_title(cls, title):
        return cls.objects.filter(title=title).first()

    @classmethod
    def by_all(cls):
        return cls.objects.all()

    def __str__(self):
        return 'title:%s' % self.title


class Category(models.Model):
    """
    分类表
    """
    uuid = models.UUIDField('uuid', unique=True, default=uuid4)
    name = models.CharField('分类名', max_length=64, null=False)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)

    @classmethod
    def by_all(cls):
        return cls.objects.all()

    @classmethod
    def by_uuid(cls, uuid):
        return cls.objects.filter(uuid=uuid).first()

    @classmethod
    def by_createtime(cls, createtime):
        return cls.objects.filter(createtime=createtime).first()


class Comment(models.Model):
    """
    评论表
    """
    uuid = models.UUIDField('uuid', unique=True, default=uuid4)
    content = models.TextField()
    articles = models.ForeignKey(Article)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)
    users = models.ForeignKey(User, related_name='comments')

    @classmethod
    def by_all(cls):
        return cls.objects.all()

    @classmethod
    def by_uuid(cls, uuid):
        return cls.objects.filter(uuid=uuid).first()

    @classmethod
    def by_createtime(cls, createtime):
        return cls.objects.filter(createtime=createtime).first()


class SecondComment(models.Model):
    """
    二级评论表
    """
    uuid = models.UUIDField('uuid', unique=True, default=uuid4)
    content = models.TextField()
    createtime = models.DateTimeField('创建时间', auto_now_add=True)
    second_comments = models.ForeignKey(Comment, related_name='second_comments')
    users = models.ForeignKey(User, related_name='second_comments')

    @classmethod
    def by_all(cls):
        return cls.objects.all()

    @classmethod
    def by_uuid(cls, uuid):
        return cls.objects.filter(uuid=uuid).first()

    @classmethod
    def by_createtime(cls, createtime):
        return cls.objects.filter(createtime=createtime).first()


class Tag(models.Model):
    """
    标签表
    """
    uuid = models.UUIDField('uuid', unique=True, default=uuid4)
    name = models.CharField('标签名', max_length=64)
    createtime = models.DateTimeField('创建时间', auto_now_add=True)

    @classmethod
    def by_uuid(cls, uuid):
        return cls.objects.filter(uuid=uuid).first()

    @classmethod
    def by_id(cls, id):
        return cls.objects.filter(id=id).first()

    @classmethod
    def by_name(cls, name):
        return cls.objects.filter(name=name).first()

    @classmethod
    def by_all(cls):
        return cls.objects.all()

    def __str__(self):
        return 'name:%s' % self.name

