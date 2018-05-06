from django.shortcuts import render, HttpResponse, redirect, reverse
from django.http import JsonResponse
from django.views.generic import View
from .libs import (get_captcha_lib, get_mobile_code_lib, register_lib,
                     login_lib, bind_user_email_lib, auth_user_email_lib, user_edit_lib, upload_avatar_lib
                     )
from django.conf import settings
# from django.contrib.auth.decorators import login_required
from oa.common_func import login_required
from account.models import User
from django.contrib import messages


class RegisterView(View):
    """
    register
    """

    def get(self, request):
        login_url = reverse('account:user_login')
        return render(request, 'account/auth_regist.html', {'login_url': login_url})

    def post(self, request):
        postdata = request.POST.copy()
        mobile_captcha = postdata.get('mobile_captcha', '')
        mobile_num = postdata.get('mobile', '')
        img_captcha = postdata.get('captcha', '').lower()
        code = postdata.get('code', '')
        name = postdata.get('name', '')
        password1 = postdata.get('password1', '')
        password2 = postdata.get('password2', '')
        result = register_lib(mobile_num, code, mobile_captcha,
                              img_captcha, name, password1, password2)
        if result['status'] is True:
            return JsonResponse({'status': 200, 'msg': result['msg']})
        return JsonResponse({'status': 400, 'msg': result['msg']})
        # if result['status'] is True:
            # return redirect(reverse('account:user_login'))
        # kw = {'message':result['msg']}
        # return render(request, 'account/auth_regist.html',kw)


class GetCaptchaView(View):
    """
    get captcha code
    """

    def get(self, request):
        getdata = request.GET.copy()
        pre_code = getdata.get('pre_code', '')
        code = getdata.get('code', '')
        print pre_code, code
        captcha_img = get_captcha_lib(pre_code, code)
        return HttpResponse(captcha_img, content_type='image/jpg')


class SendMobileCode(View):
    """
    send mobile code
    """
    def post(self, request):
        postdata = request.POST.copy()
        mobile = postdata.get('mobile', '')
        code = postdata.get('code', '')
        captcha = postdata.get('captcha', '')
        result = get_mobile_code_lib(mobile, code, captcha)
        print mobile, code, captcha
        if result['status'] is True:
            return JsonResponse( {'status': 200, 'msg':result['msg']})
        else:
            return JsonResponse( {'status': 400, 'msg':result['msg']})


class LoginView(View):
    """
    login
    """
    def get(self, request):
        next = request.GET.get('next', '')
        return render(request, 'account/auth_login.html', {'next': next if next else '/account/profile'})

    def post(self,request):
        postdata = request.POST.copy()
        name = postdata.get('name', '')
        password = postdata.get('password', '')
        code = postdata.get('code', '')
        captcha = postdata.get('captcha', '')
        remember = postdata.get('remember', '')
        result = login_lib(request, name, password, code, captcha, remember)
        if result['status'] is True:
            return JsonResponse({'status': 200, 'msg': result['msg']})
        else:
            return JsonResponse({'status': 400, 'msg': result['msg']})


@login_required
def profile(request):
    return render(request, 'account/account_profile.html')


@login_required
def user_logout(request):
    request.session.flush()    # del session
    return redirect(reverse('account:user_login'))


@login_required
def user_edit(request):
    if request.method == 'POST':
        postdata = request.POST.copy()
        name = postdata.get('name', '')
        password = postdata.get('password', '')
        result = user_edit_lib(request, name, password)
        kw = result['msg']
        if result['status']:
            return render(request, 'account/account_edit.html', {'message': kw})
        return render(request, 'account/account_edit.html', {'message': kw})
    return render(request, 'account/account_edit.html')


@login_required
def bind_user_email(request):
    if request.method == 'GET':
        return render(request, 'account/account_bind_email.html')
    if request.method == 'POST':
        postdata = request.POST.copy()
        email = postdata.get('email', '')
        result = bind_user_email_lib(request, email)
        if result['status'] is True:
            messages.success(request, result['msg'])
        else:
            messages.error(request, result['msg'])
        return redirect(reverse('account:bind_user_email'))



@login_required
def auth_user_email(request):
    getdata = request.GET.copy()
    email_code = getdata.get('email_code', '')
    email = getdata.get('email', '')
    u = getdata.get('u', '')
    result = auth_user_email_lib(request, email_code, email, u)
    if result['status'] is True:
        return redirect(reverse('account:user_edit'))
    return HttpResponse(result['msg'])


@login_required
def upload_avatar(request):
    avatar = request.FILES.get('user_avatar', '')
    result = upload_avatar_lib(request, avatar)
    if result['status'] is True:
        return render(request, 'account/account_edit.html', {'message': result['msg']})
    return render(request, 'account/account_edit.html', {'message': result['msg']})

