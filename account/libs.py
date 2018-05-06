# coding=utf8
# !/usr/bin/env python
__author__ = 'tony'

from datetime import datetime
from random import randint
from models import User
from utils.captcha.captcha import create_captcha
from public_libs.redis_conn.redis_conn import conn
from public_libs.yun_tong_xun.yun_tong_xun import sendTemplateSMS
from public_libs.send_email.send_email_libs import send_qq_html_email
from random import choice
from string import printable
from uuid import uuid4
import json
from task import send_celery_email


def get_captcha_lib(pre_code, code):
    """获取图形验证码"""
    if pre_code is not None:
        conn.delete('captcha:%s' % pre_code)
    text, img = create_captcha()
    conn.setex('captcha:%s' % code, text.lower(), 60)
    return img


def get_mobile_code_lib(mobile, code, captcha):
    """获取短信验证码"""
    captcha_redis = conn.get('captcha:%s' % code)
    if captcha.lower() == captcha_redis:
        code = randint(1000, 9999)
        conn.setex('mobile_code:%s' % mobile, code,  30*60*60*365)
        sendTemplateSMS(mobile, [code, 30], 1)
        return {'status': True, 'msg': mobile}
    else:
        return {'status': False, 'msg': u'图形验证码错误'}


def register_lib(mobile_num, code, mobile_captcha,
                 img_captcha, name, password1, password2):

    """用户注册"""
    mobile_code_redis = conn.get('mobile_code:%s' % mobile_num)
    captcha_redis = conn.get('captcha:%s' % code)
    if mobile_num == '' or name == '' or password1 == '' or password2 == '':
        return {'status': False, 'msg': u'参数不能为空'}
    print 'mobile_captcha', mobile_code_redis, 'img_captcha', captcha_redis
    if mobile_captcha != mobile_code_redis:
        return {'status': False, 'msg': u'手机验证码不正确'}
    if captcha_redis != img_captcha.lower():
        return {'status': False, 'msg': u'图形验证码不正确'}
    if password1 != password2:
        return {'status': False, 'msg': u'两次密码不一致'}
    if User.by_name(name) is not None:
        return {'status': True, 'msg': u'用户名已存在'}
    user = User()
    user.name = name
    user.password = password1
    user.mobile = mobile_num
    user.save()
    return {'status': True, 'msg': u'注册成功'}


def login_lib(request, name, password, code, captcha, remember):
    """用户登录"""
    if code == '' or name == '' or password == '' or captcha == '':
        return {'status': False, 'msg': u'参数不能为空'}
    if conn.get('captcha:%s' % code) != captcha:
        return {'status': False, 'msg': u'图形验证码不正确'}
    user = User.by_name(name)
    if user is None:
        return {'status': False, 'msg': u'用户不存在'}
    if user.auth_password(password) is True:
        user.last_login = datetime.now()
        user.login_count += 1
        user.save()
        request.session['user_id'] = user.id
        if remember == 'remember':
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(1800)
        return {'status': True, 'msg': '登录成功', 'user': user}
    return {'status': False, 'msg': '密码输入错误'}


def bind_user_email_lib(request, email):
    """绑定邮箱"""
    email = email.encode('utf-8')
    if email != '':
        ttl = conn.ttl('email:%s' % email)
        if ttl is not None:
            return {'status': True, 'msg': u'邮件已发送，过%s秒在发送' % ttl}
        email_code = ''.join([choice(printable[:62]) for i in xrange(4)]) # 生成验证码
        u = str(uuid4())
        text_dict = {
            'email_code': email_code,
            u: request.current_user.id
        }
        redis_text = json.dumps(text_dict)  # json封装字典存入redis
        from oa.settings import HOST, Port
        content = """
                 <p>绑定邮箱</p>
        <p><a href="http://{}:{}/account/auth_user_email?email_code={}&u={}&email={}">点击此链接绑定邮箱，有效期为10分钟</a></p>
        """.format(HOST, Port, email_code, u, email)
        # send_fail = send_qq_html_email('1156391589@qq.com', [email], u'绑定邮箱', content)
        # print send_fail
        send_celery_email.delay('1156391589@qq.com', [email], u'绑定邮箱', content)
        conn.setex('email:%s' % email, redis_text, 600)
        return {'status': True, 'msg': u'邮件发送成功，请注意查收'}
    return {'status': False, 'msg': u'请输入邮箱'}


def auth_user_email_lib(request, email_code, email, u):
    if email == '' or email_code == '' or u == '':
        return {'status': False, 'msg': u'参数不能为空'}
    if email:
        text_json = conn.get('email:%s' % email)
        if text_json:
            text_dict = json.loads(text_json)
            if text_dict['email_code'] == email_code:
                user = request.current_user
                if not user:
                    user_id = text_dict.get(u, '')
                    user = User.by_id(user_id)
                user.email = email
                user.register_time = datetime.now()
                user.save()
                return {'status': True, 'msg': u'邮箱绑定成功'}
            return {'status': False, 'msg': u'参数错误'}
        return {'status': False, 'msg': u'邮箱错误或者验证码过期'}
    return {'status': False, 'msg': u'邮箱不能为空'}


def user_edit_lib(request, name, password):
    if name == '':
        return {'status': False, 'msg': u'用户名不能为空'}
    if password == '':
        return {'status': False, 'msg': u'密码不能为空'}
    user = request.current_user
    user.password = password
    user.name = name
    user.save()
    return {'status': True, 'msg': u'用户信息修改成功'}


def upload_avatar_lib(request, avatar):
    if avatar:
        if avatar.multiple_chunks() is True:
            return {'status': False, 'msg': u'头像图片要求小于2M'}
        try:
            user = request.current_user
            user.avatar = avatar.read()
            user.register_time = datetime.now()
            user.save()
            return {'status': True, 'msg': u'头像上次成功'}
        except Exception, e:
            import traceback
            print '----------------'
            print traceback.format_exc()
            send_qq_html_email('1156391589@qq.com', ['542041398@qq.com'], u'异常捕捉', traceback.format_exc().replace('\n', '<br>'))
            return {'status': False, 'msg': e}
    return {'status': False, 'msg': u'头像图片不能为空'}
