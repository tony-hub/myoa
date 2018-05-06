#!/usr/bin/env python
__author__ = 'tony'

from functools import wraps
from django.shortcuts import redirect, reverse
import urllib

def login_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id', ''):
            url = reverse('account:user_login')
            url_full = '%s?next=%s' % (url, urllib.quote(request.get_full_path()))
            return redirect(url_full)
        return func(request, *args, **kwargs)
    return wrapper



