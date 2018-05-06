# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from account.models import User


class Role(models.Model):
    """角色表"""
    name = models.CharField(u'角色名', max_length=32, unique=True, null=False)
    users = models.ManyToManyField(User, related_name='roles')

    @classmethod
    def by_name(cls, name):
        return cls.objects.filter(name=name).first()

    @classmethod
    def by_id(cls, id):
        return cls.objects.filter(pk=id).first()

    @classmethod
    def all(cls):
        return cls.objects.all()


class Permission(models.Model):
    """权限表"""
    name = models.CharField(u'权限名', max_length=32, unique=True, null=False)
    strcode = models.CharField(u'权限码', max_length=32)
    roles = models.ManyToManyField(Role, related_name='permissions')

    @classmethod
    def by_name(cls, name):
        return cls.objects.filter(name=name).first()

    @classmethod
    def by_id(cls, id):
        return cls.objects.filter(pk=id).first()

    @classmethod
    def all(cls):
        return cls.objects.all()


class Menu(models.Model):
    """菜单表"""
    name = models.CharField(u'菜单名', max_length=32, unique=True, null=False)
    permissions = models.OneToOneField(Permission)

    @classmethod
    def by_name(cls, name):
        return cls.objects.filter(name=name).first()

    @classmethod
    def by_id(cls, id):
        return cls.objects.filter(pk=id).first()

    @classmethod
    def all(cls):
        return cls.objects.all()


class Handler(models.Model):
    """视图函数表"""
    name = models.CharField(u'视图名称', max_length=32, unique=True, null=False)
    permissions = models.OneToOneField(Permission)

    @classmethod
    def by_name(cls, name):
        return cls.objects.filter(name=name).first()

    @classmethod
    def by_id(cls, id):
        return cls.objects.filter(pk=id).first()

    @classmethod
    def all(cls):
        return cls.objects.all()