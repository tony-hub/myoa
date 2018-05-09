# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse
from oa.common_func import login_required
from libs import add_tag_category_lib, tag_category, del_category_tag_lib, add_article_lib


@login_required
def article_list(request):
    return render(request, 'article/article_list.html')


@login_required
def add_article(request):
    if request.method == 'GET':
        kw = tag_category()
        return render(request, 'article/add_article.html', kw)
    if request.method == 'POST':
        postdata = request.POST.copy()
        title = postdata.get('title', '')
        article = postdata.get('article', '')
        desc = postdata.get('desc', '')
        category = postdata.get('category', '')
        thumbnail = postdata.get('thumbnail', '')
        tags = postdata.get('tags', '')
        article_id = postdata.get('article_id', '')
        add_article_lib(title, article, desc, category, thumbnail, tags, article_id)


@login_required
def add_category_tag(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name', None)
        tag_name = request.POST.get('tag_name', None)
        result = add_tag_category_lib(category_name, tag_name)
        if result['status']:
            return JsonResponse({'status': 200, 'msg': result['msg']})
        return JsonResponse({'status': 400, 'msg': result['msg']})
    kw = tag_category()
    return render(request, 'article/article_add_category_tag.html', kw)


def del_category_tag(request):
    if request.method == 'GET':
        c_uuid = request.GET.get('c_uuid', None)
        t_uuid = request.GET.get('t_uuid', None)
        del_category_tag_lib(c_uuid, t_uuid)
        return redirect(reverse('article:add_category_tag'))


def article_modify_list(request):
    return render(request, 'article/article.html')

