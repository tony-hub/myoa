#!/usr/bin/env python
__author__ = 'tony'

from permission.permission_interface_libs import PermWrapper


def current_user_processor(request):
    return {'current_user': request.current_user, 'user_perms': PermWrapper(request.current_user)}