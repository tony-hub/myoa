# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from string import printable

from django.db import models
from uuid import uuid4
from pbkdf2 import PBKDF2
# Create your models here.


class User(models.Model):
    uuid = models.UUIDField(verbose_name='uuid', unique=True, default=uuid4)
    name = models.CharField(verbose_name=u'名字', max_length=64, unique=True)
    _password = models.CharField(verbose_name=u'密码', max_length=64)
    phone = models.CharField(verbose_name=u'手机号', max_length=20)
    last_login = models.DateTimeField(verbose_name=u'上次登录时间', auto_now=True)
    login_count = models.IntegerField(verbose_name=u'登录次数', default=0)
    register_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    email = models.EmailField(verbose_name='email')
    qq = models.CharField(verbose_name=u'QQ号', max_length=50)
    _locked = models.BooleanField(verbose_name=u'是否被冻结', default=False)
    _deleted = models.BooleanField(verbose_name=u'是否被删除', default=False)
    _avatar = models.CharField(verbose_name=u'头像名', max_length=128)

    @classmethod
    def all(cls):
        return cls.objects.all()

    @classmethod
    def by_id(cls, id):
        return cls.objects.filter(id=id).first()

    @classmethod
    def by_uuid(cls, uuid):
        return cls.objects.filter(uuid=uuid).first()

    @classmethod
    def by_name(cls, name):
        return cls.objects.filter(name=name).first()

    def _hash_password(self, password):
        return PBKDF2.crypt(password, iterations=0x2537)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = self._hash_password(password)

    @property
    def avatar(self):
        return self._avatar if self._avatar else 'default_avatar.jpg'

    @avatar.setter
    def avatar(self, avater):
        class ValidationError(Exception):
            def __init__(self, message):
                super(ValidationError, self).__init__(message)
        if 64 < len(avater) < 1024 * 1024:
            import imghdr
            import os
            ext = imghdr.what('', h=avater)  # 获取后缀名
            uu = str(self.uuid)
            if ext in ['png', 'jpeg', 'jpg', 'gif', 'bmp'] and not self.is_xss_image(avater):
                if self._avatar and os.path.exists('static/images/useravatars/{}'.format(self._avatar)):
                    os.unlink('static/images/useravatars/{}'.format(self._avatar))   #del file
                file_path = 'static/images/useravatars/{}.{}'.format(uu, ext)
                with open(file_path, 'w') as f:
                    f.write(avater)
                self._avatar = '%s.%s' % (uu, ext)
            else:
                raise ValidationError("not in ['png','jpeg','jpg','gif', 'bmp']")
        else:
            raise ValidationError(u'图片大小必须在64到1024*1024 bytes')

    def is_xss_image(self, data):
        return all([i in printable for i in data[:16]])

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, value):
        assert isinstance(value, bool)
        self._locked = value

    def auth_password(self, other_password):
        if self._password is not None:
            return self.password == PBKDF2.crypt(other_password, self.password)

    def __str__(self):
        return "%s : %s" % (self.id, self.name)
