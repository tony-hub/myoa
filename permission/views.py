# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse
from oa.common_func import login_required
from .libs import (role_add_permission_lib, add_role_lib, add_permission_lib, permission_manage_lib,
                     del_role_lib, del_permission_lib, user_add_role_lib, add_menu_lib)


@login_required
def manage(request):
    roles, permissions, menus, users, handlers =permission_manage_lib()
    kw = {
        'roles': roles,
        'permissions': permissions,
        'menus': menus,
        'users': users,
        'handles': handlers,
        'dev_users': [],
        'dev_role_id': [],
    }
    return render(request, 'permission/permission_list.html',kw)


@login_required
def role_add_permission(request):
    if request.method == 'POST':
        permission_id = request.POST.get('permissionid', '')
        role_id = request.POST.get('roleid', '')
        result = role_add_permission_lib(role_id, permission_id)
        # if result['status'] is True:
        #     return render(request, 'permission/permission_list.html', {'message': result['msg']})
        # return render(request, 'permission/permission_list.html', {'message': result['msg']})
    return redirect(reverse('permission:manage'))

@login_required
def add_role(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        result = add_role_lib(name)
        # if result['status'] is True:
        #     return render(request, 'permission/permission_list.html', {'message': result['msg']})
        # return render(request, 'permission/permission_list.html', {'message': result['msg']})
    return redirect(reverse('permission:manage'))


@login_required
def add_permission(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        strcode = request.POST.get('strcode', '')
        add_permission_lib(name, strcode)
    return redirect(reverse('permission:manage'))



@login_required
def del_role(request):
    role_id = request.GET.get('id', '')
    del_role_lib(role_id)
    return redirect(reverse('permission:manage'))


@login_required
def del_permission(request):
    permission_id = request.GET.get('id', '')
    del_permission_lib(permission_id)
    return redirect(reverse('permission:manage'))



def user_add_role(request):
    if request.method == 'POST':
        userid = request.POST.get('userid', '')
        roleid = request.POST.get('roleid', '')
        user_add_role_lib(userid, roleid)
        return redirect(reverse('permission:manage'))



def add_menu(request):
    if request.method == 'POST':
        permission_id = request.POST.get('permissionid', '')
        name = request.POST.get('name', '')
        add_menu_lib(permission_id, name)
    return redirect(reverse('permission:manage'))