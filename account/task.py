#!/usr/bin/env python
#coding=utf-8
from __future__ import absolute_import, unicode_literals
from celery import task, shared_task
from public_libs.send_email.send_email_libs import send_qq_html_email

@task
def send_celery_email(from_email, to_emails, title, content):
    send_fail = send_qq_html_email(from_email, to_emails, title, content)
    print send_fail


