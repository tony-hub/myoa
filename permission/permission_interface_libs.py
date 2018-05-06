#!/usr/bin/env python
__author__ = 'tony'
from permission.models import Menu, Permission

class PermWrapper(object):
    def __init__(self, current_user):
        self.current_user = current_user

    def __getitem__(self, menu_name):
        # perm_name = Menu.by_name(menu_name).permissions.strcode
        # print '-------------', perm_name
        return Permission.objects.filter(roles__users__id=self.current_user.id).filter(strcode=menu_name).exists()
