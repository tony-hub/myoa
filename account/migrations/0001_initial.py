# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-26 15:47
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True, verbose_name='uuid')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='\u540d\u5b57')),
                ('_password', models.CharField(max_length=64, verbose_name='\u5bc6\u7801')),
                ('phone', models.CharField(max_length=20, verbose_name='\u624b\u673a\u53f7')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='\u4e0a\u6b21\u767b\u5f55\u65f6\u95f4')),
                ('login_count', models.IntegerField(default=0, verbose_name='\u767b\u5f55\u6b21\u6570')),
                ('register_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('email', models.EmailField(max_length=254, verbose_name='email')),
                ('qq', models.CharField(max_length=50, verbose_name='QQ\u53f7')),
                ('_locked', models.BooleanField(default=False, verbose_name='\u662f\u5426\u88ab\u51bb\u7ed3')),
                ('_deleted', models.BooleanField(default=False, verbose_name='\u662f\u5426\u88ab\u5220\u9664')),
                ('_avatar', models.CharField(max_length=128, verbose_name='\u5934\u50cf\u540d')),
            ],
        ),
    ]
