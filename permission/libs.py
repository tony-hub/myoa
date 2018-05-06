#!/usr/bin/env python
# coding=utf8
__author__ = 'tony'

from .models import Permission, Role, Handler, Menu
from account.models import User


def permission_manage_lib():
    roles = Role.all()
    permissions = Permission.all()
    handlers = Handler.all()
    menus = Menu.all()
    users = User.all()
    return roles, permissions, menus, users, handlers


def role_add_permission_lib(role_id, permission_id):
    permission = Permission.by_id(permission_id)
    role = Role.by_id(role_id)
    if permission and role:
        permission.roles.add(role)


def add_role_lib(name):
    role_name = Role.by_name(name)
    if not role_name:
        role = Role()
        role.name = name
        role.save()
        return {'status': True, 'msg': u'角色:%s创建成功' % name}
    return {'status': False, 'msg': u'角色:%s已存在' % name}


def add_permission_lib(name, strcode):
    perm_name = Permission.by_name(name)
    if not perm_name:
        permission = Permission()
        permission.name = name
        permission.strcode = strcode
        permission.save()
        return {'status': True, 'msg': u'权限创建成功'}
    return {'status': False, 'msg': u'权限已存在'}


def del_role_lib(role_id):
    if role_id:
        role = Role.by_id(role_id)
        role.delete()


def del_permission_lib(permission_id):
    if permission_id:
        permission = Permission.by_id(permission_id)
        permission.delete()


def user_add_role_lib(userid, roleid):
    user = User.by_id(userid)
    role = Role.by_id(roleid)
    if user and role:
        role.users.add(user)


def add_menu_lib(permission_id, name):
    menu = Menu()
    menu.name = name
    menu.permissions_id = permission_id
    menu.save()




