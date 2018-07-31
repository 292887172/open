# !/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import json
import random
import logging
import base64
import hashlib
import datetime
import re

import django
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from base.const import ConventionValue
from base.wx_login import deal_wxlogin_data
from conf.apiconf import wx_oauth, wx_userinfo
from conf.sessionconf import *
from base.connection import RedisBaseHandler
from conf.redisconf import SMS_CHECK_CODE_PREFIX, EMAIL_CHECK_CODE_PREFIX, EMAIL_ACTIVE_PREFIX
from conf.redisconf import SMS_CHECK_CODE_EXPIRE, EMAIL_CHECK_CODE_EXPIRE, EMAIL_ACTIVE_EXPIRE

from util.auth import get_auth_user
from util.sms.SendTemplateSMS import sendTemplateSMS
from model.center.account import Account
from model.center.auto_login import AutoLogin
from common.smart_helper import check_user_password, check_factory_uuid, get_factory_info
from util.email.send_email_code import send_mail
from common.validate_code import create_validate_code
from util.email.email_code import create_eamil_code
from common.developer_helper import create_developer, update_group_info
from django.db.models import Q
from base.connection import MyAdapter
from util.sms.verify_code import verify_sms_code

from conf.commonconf import HOST_DOMAIN
from base.crypto import md5_en
from common.account_helper import change_user_pwd, update_user_login_data
from conf.wxconf import APPID, APP_SECRET
import requests

_convention = ConventionValue()


@csrf_exempt
@login_required
def home(request):
    """
    开发者中心
    :param request:
    :return:
    """
    if request.method == 'GET':
        if request.user.account_type == _convention.USER_IS_ADMIN:
            return HttpResponseRedirect(reverse("admin_center"))
        # 移除第三方登录标志，和注册成功标志，防止用户直接访问这两个页面
        try:
            del request.session[SESSION_LOGIN_THIRD]
            del request.session[SESSION_REGISTER_SUCCESS]
        except Exception as e:
            logging.getLogger("").info(str(e))
            pass
        fac_info = get_factory_info(request.user.account_from_id)
        t = Account.objects.get(account_id=request.user)
        if t.relate_account:
            team_info = json.loads(t.relate_account)
            print(team_info)
        return render(request, "center/home.html", locals())
    elif request.method == 'POST':
        # 登录账户信息
        user = request.POST.get('user', '')
        action = request.POST.get("action", "")
        user_from = request.POST.get('user_from', '')
        team_info = request.POST.get("team_info")
        # 公司团队信息
        company = request.POST.get('coName', '')
        company_url = request.POST.get('coNetUrl', '')
        company_address = request.POST.get('coAddress', '')
        company_scale = request.POST.get('coDevScale', 0)

        # 联系人信息
        contact_name = request.POST.get('coContactName', '')
        contact_role = request.POST.get('coContactRole', '')
        # 联系人移动手机
        contact_mobile = request.POST.get('coContactMobile', '')
        # 联系人固定电话
        contact_phone = request.POST.get('coContactPhone', '')
        contact_qq = request.POST.get('coContactQq', '')
        contact_email = request.POST.get('devEmail', '')
        # email_code = request.POST.get('devCode', '')

        # 合作厂商信息
        factory_name = request.POST.get('factory_name', '')
        factory_uuid = request.POST.get('coFacUid', '')
        update = request.POST.get('coUpdate', None)
        if action == 'submit_email':
            update_group_info(user, team_info)
            return HttpResponse(json.dumps({"status": "ok"}))
        r = RedisBaseHandler().client
        try:
            # e_code = r.get(EMAIL_CHECK_CODE_PREFIX + contact_email)
            res = create_developer(company, company_url, company_address, company_scale, contact_name, contact_role,
                                   contact_mobile, contact_phone, contact_qq, contact_email, factory_name,
                                   factory_uuid, user, user_from)
            if res:
                return HttpResponse(json.dumps({'status': 'ok', 'msg': '基本信息已保存', 'url': 'product/list'}))
            else:
                return HttpResponse(json.dumps({'status': 'error', 'msg': '登记失败，请确保信息完整'}))

        except Exception as e:
            logging.getLogger('').info(str(e))
            return HttpResponse(json.dumps({'status': 'error', 'msg': '验证码失效，请重新获取'}))


@csrf_exempt
def login(request):
    if request.method == "POST":
        account = request.POST.get("account", "")
        if not account:
            msg = "<div class='ui-error-box' ><b></b><p>帐号不能为空</P></div>"
            return render(request, "center/login.html", locals())
        password = request.POST.get("password", "")
        if not password:
            msg = "<div class='ui-error-box' ><b></b><p>请输入密码</P></div>"
            return render(request, "center/login.html", locals())
        try:
            a = Account.objects.filter(Q(account_id=account)|Q(account_phone=account)|Q(account_email=account))

            for i in a:
                account = i.account_id
            password = base64.b64decode(password)
            user_obj = authenticate(username=account, password=password)

            if not user_obj:
                msg = "<div class='ui-error-box' ><b></b><p>用户名或密码错误</P></div>"
                return render(request, "center/login.html", locals())
            # 已禁用的帐号不允许登录
            if user_obj.is_forbid != 0:
                msg = "<div class='ui-error-box' ><b></b><p>该帐号已被禁用，暂时无法登录</P></div>"
                return render(request, "center/login.html", locals())
            # 登录成功后跳转回请求的页面
            if account == 'admin':
                uri = "/center"
            else:
                uri = request.session[SESSION_REDIRECT_URI]
            response = HttpResponseRedirect(uri)
            remember = request.POST.get("remember")
            # 将用户登录信息保存到cookie
            if remember:
                dt = datetime.datetime.now() + datetime.timedelta(days=30)
                response.set_cookie(COOKIE_USER_ACCOUNT, account, expires=dt)
                m = hashlib.md5()
                m.update(('token_' + account).encode('utf-8'))
                token = m.hexdigest()
                update_user_login_data(account, password, token, request.META.get('REMOTE_ADDR'), 'save')
                response.set_cookie(AUTO_LOGIN, token, expires=dt)
            else:
                response.delete_cookie(COOKIE_USER_ACCOUNT)
            django.contrib.auth.login(request, user_obj)
            return response
        except Exception as e:
            print(e)
            logging.getLogger('').info(str(e))
            msg = "<div class='ui-error-box' ><b></b><p>不存在此用户</P></div>"
            return render(request, "center/login.html", locals())
    try:
        request.session[SESSION_REDIRECT_URI] = request.GET.get('next', "/product/console")
        if request.user.developer.developer_id:
            return HttpResponseRedirect("/product/console")
        elif request.user.account_id:
            return HttpResponseRedirect("/guide")
    except Exception as e:
        logging.getLogger('').info(str(e))
    if COOKIE_USER_ACCOUNT in request.COOKIES:
        username = request.COOKIES[COOKIE_USER_ACCOUNT]
    if AUTO_LOGIN in request.COOKIES:
        token = request.COOKIES[AUTO_LOGIN]
        try:
            al = AutoLogin.objects.get(al_token=token)
            ac_id = al.al_account_id
            ac_pwd = base64.b64decode(al.al_account_pwd)
            user_obj = authenticate(username=ac_id, password=ac_pwd)
            django.contrib.auth.login(request, user_obj)
            return HttpResponseRedirect("/product/console")
        except Exception as e:
            pass
    return render(request, "center/login.html", locals())


def login_sys(request):
    if request.method == "POST":
        account = request.POST.get("account", "")
        if not account:
            msg = "<div class='ui-error-box' ><b></b><p>帐号不能为空</P></div>"
            return render(request, "center/login-sys.html", locals())
        password = request.POST.get("password", "")
        if not password:
            msg = "<div class='ui-error-box' ><b></b><p>请输入密码</P></div>"
            return render(request, "center/login-sys.html", locals())
        try:
            user_obj = check_user_password(account, password)

            if user_obj['status'] == 'error':
                if user_obj['result'] == 'invalid password':
                    msg = "<div class='ui-error-box' ><b></b><p>密码错误，请核对</P></div>"
                else:
                    msg = "<div class='ui-error-box' ><b></b><p>请用厂家帐号登录</P></div>"
                return render(request, "center/login-sys.html", locals())
            elif user_obj['status'] == 'ok':
                # 已禁用的帐号不允许登录
                if user_obj['result']['is_forbid'] != 0:
                    msg = "<div class='ui-error-box' ><b></b><p>该帐号已被禁用，暂时无法登录</P></div>"
                    return render(request, "center/login.html", locals())
                # 登录成功后跳转回请求的页面
                uri = request.session[SESSION_REDIRECT_URI]
                try:
                    # 厂商帐号已经注册过
                    a = Account.objects.get(account_from_id=account)
                    user_name = a.account_id
                    uri = '/center'
                    # Account.objects.create_user(user_id, password, "53iq")
                    user_account = get_auth_user(username=user_name)
                    django.contrib.auth.login(request, user_account)
                except Exception as e:
                    # 厂商注册第三个参数为53iq
                    request.session[SESSION_LOGIN_THIRD] = account
                    logging.getLogger('').info(str(e))
                    pass
                response = HttpResponseRedirect(uri)
                return response
        except Exception as e:
            print(e)
            logging.getLogger('').info(str(e))
            msg = "<div class='ui-error-box' ><b></b><p>登录异常</P></div>"
            return render(request, "center/login-sys.html", locals())

    request.session[SESSION_REDIRECT_URI] = request.GET.get('next', "register_confirm")
    try:
        if request.user.account_id:
            return HttpResponseRedirect("/guide")
    except Exception as e:
        logging.getLogger('').info(str(e))
    return render(request, "center/login-sys.html", locals())


def logout(request):
    """
    登出
    :param request:
    :return:
    """
    account_id = ''
    try:
        if request.user.account_id:
            account_id = request.user.account_id
    except Exception as e:
        print(e)
        logging.getLogger('').info(str(e))
    django.contrib.auth.logout(request)
    response = HttpResponseRedirect(reverse("home"))
    response.delete_cookie(AUTO_LOGIN)
    update_user_login_data(account_id, '', '', '', 'delete')
    return response


@csrf_exempt
def register(request):
    """
    用户注册
    :param request:
    :return:
    """

    def post():
        user_id = request.POST.get('user_id', None)
        password = request.POST.get("password", "")
        code = request.POST.get('code', None)
        rg = request.POST.get('rg', '')
        dproducts = request.POST.get('dproducts', "")
        team_persons = request.POST.get('persons', "")
        expertise = request.POST.get('expertise', "")
        sproducts = request.POST.get('sproducts', "")
        intent = request.POST.get('intent', "")

        # 用这个字段判断是否给用户默认注册
        # 有这个字段的请求，是从外部过来的
        default_register = request.POST.get("default", "")
        if default_register == "1":
            email = request.POST.get("email", '')
            try:
                # 平台注册帐号来源为53iq
                Account.objects.create_user(
                    account=user_id, password=password, stat="open/ex", dproducts=dproducts, email=email)
                ret = {"code": 0, "msg": "success"}
            except Exception as e:
                logging.getLogger('').exception(e)
                ret = {"code": -1, "msg": str(e)}
            return JsonResponse(ret)

        # 人数为空时，默认为None
        if team_persons == '':
            team_persons = None
        else:
            try:
                # 人数转成int类型判断是否为正整数
                team_persons = int(team_persons)
                if type(team_persons) != int or team_persons <= 0:
                    re = {'status': 4, 'error': '人数必须输入正整数'}
                    return HttpResponse(json.dumps(re))
            except Exception as e:
                print(str(e))
                # 人数无法转成int类型，输入了非数字
                re = {'status': 5, 'error': '人数输入的不是数字'}
                return HttpResponse(json.dumps(re))
        if rg == 'email':
            re = {}
            if code.lower() == str(request.session[SESSION_LOGIN_VALIDATE]).lower():
                try:
                    # 将注册信息临时存在redis里面，等待激活，有效时间30分钟
                    r = RedisBaseHandler().client
                    r.set(EMAIL_ACTIVE_PREFIX + user_id, password, EMAIL_ACTIVE_EXPIRE)
                    request.session[SESSION_REGISTER_SUCCESS] = 'success'
                    re = {'status': 1, 'url': 'register_success?rg=email&user=' + user_id}
                except Exception as e:
                    print(e)
                    logging.getLogger('').info(str(e))
            else:
                re = {'status': 2, 'error': '验证码错误'}
            return HttpResponse(json.dumps(re))
        else:
            re = verify_sms_code(user_id, code)
            if re['status'] == 1:
                try:
                    # 平台注册帐号来源为53iq
                    Account.objects.create_user(user_id, password, "53iq", dproducts, team_persons, expertise,
                                                sproducts, intent)
                    user_obj = authenticate(username=user_id, password=password)
                    django.contrib.auth.login(request, user_obj)
                    request.session[SESSION_REGISTER_SUCCESS] = 'success'
                except Exception as e:
                    logging.getLogger('').info(str(e))
            return HttpResponse(json.dumps(re))

    if request.method == "GET":
        # 注册方式，默认是手机，可选邮箱注册
        rg_method = request.REQUEST.get('rg', 'phone')
    elif request.method == "POST":
        return post()

    return render(request, "center/register.html", locals())


@csrf_exempt
def register_confirm(request):
    """
    第三方登录注册确认
    :param request:
    :return:
    """

    def post():
        user_id = request.POST.get('username', None)
        from_user_id = request.POST.get('from_id', None)
        password = request.POST.get("password", "")
        validate = request.POST.get('validate', None)
        res = {'status': '', 'msg': ''}
        try:
            if validate.lower() == str(request.session[SESSION_LOGIN_VALIDATE]).lower():
                # 厂商帐号注册，帐号来源为设备管理系统厂商帐号
                r = get_factory_info(from_user_id)
                phone = ''
                if r:
                    phone = r['phone']
                Account.objects.create_user(user_id, password, from_user_id, phone)
                user_obj = authenticate(username=user_id, password=password)
                django.contrib.auth.login(request, user_obj)
                res['status'] = 'ok'
            else:
                res['status'] = 'error'
                res['msg'] = '验证码错误'
        except Exception as e:
            res['status'] = 'error'
            res['msg'] = '注册失败，确保信息正确'
            logging.getLogger('').info(str(e))
            pass
        return HttpResponse(json.dumps(res))

    if request.method == "GET":
        # 厂商帐号登录确认，若非异常访问返回开发者中心
        t = "center/register-confirm.html"
        if SESSION_LOGIN_THIRD in request.session:
            from_id = request.session[SESSION_LOGIN_THIRD]
            t = "center/register-confirm.html"
        else:
            pass
            # return HttpResponseRedirect('/')
        return render(request, t, locals())
    elif request.method == "POST":
        return post()


@csrf_exempt
def register_success(request):
    """
    注册成功返回界面
    :param request:
    :return:
    """
    rg = request.REQUEST.get('rg', '')
    user = request.REQUEST.get('user', '')
    t = "center/register.html"

    if SESSION_REGISTER_SUCCESS in request.session:
        if rg == 'email':
            # base64加密user_id
            user_b64 = base64.b64encode(user.encode(encoding="utf-8"))
            send_mail(user, '53iq通行证-注册激活', HOST_DOMAIN + '/center/active?user=' + user_b64.decode())
        t = "center/register-success.html"
        # del request.session[SESSION_REGISTER_SUCCESS]
    return render(request, t, locals())


def me(request):
    return HttpResponse("me")


@csrf_exempt
def send_sms(request):
    """
    发送验证码短信
    :param request:
    :return:
    """
    user_id = request.POST.get('user_id', None)
    if user_id:
        try:
            tel = request.POST.get('tel', None)
            if tel:
                code = str(random.randint(100000, 999999))
                # 将短信验证码保存到redis中
                r = RedisBaseHandler().client
                r.set(SMS_CHECK_CODE_PREFIX + user_id, code, SMS_CHECK_CODE_EXPIRE)

                # 发送验证短信
                sendTemplateSMS(tel, [code, str(SMS_CHECK_CODE_EXPIRE // 60)], 34882)
                return HttpResponse(json.dumps({'status': '1'}))
            else:
                return HttpResponse(json.dumps({'status': '-1'}))
        except Exception as e:
            logging.getLogger('').info(str(e))
            return HttpResponse(json.dumps({'status': '-1'}))
    else:
        return HttpResponse(json.dumps({'status': '-1'}))


def validate_code(request):
    """
    生成验证码
    :param request:
    :return:
    """
    vcode = create_validate_code()
    print('vcode[1]=', vcode[1])
    request.session[SESSION_LOGIN_VALIDATE] = vcode[1]
    mstream = io.BytesIO()
    vcode[0].save(mstream, format="GIF")
    return HttpResponse(mstream.getvalue(), "image/gif")


@csrf_exempt
def check_user_name(request):
    """
    验证用户名是否存在返回ok表示已经存在
    :param request:
    :return:
    """
    user_name = request.POST.get('username', '')
    try:
        Account.objects.get(account_id=user_name)
        re = 'ok'
    except Exception as e:
        re = 'error'
        logging.getLogger('').info(str(e))
        pass
    return HttpResponse(json.dumps({'status': re}))


@csrf_exempt
def check_fac_uuid(request):
    """
    验证厂商uuid是否正确
    :param request:
    :return:
    """
    fac_name = request.POST.get('fac_name', '')
    fac_uuid = request.POST.get('fac_uuid', '')
    re = ''
    try:
        re = check_factory_uuid(fac_name, fac_uuid)
    except Exception as e:
        logging.getLogger('').info(str(e))
        pass
    return HttpResponse(json.dumps({'status': re}))


@csrf_exempt
# @login_required
def send_email_code(request):
    """
    发送邮箱验证码
    :param request:
    :return:
    """
    email_address = request.POST.get('email', '')
    result = 'error'
    r = RedisBaseHandler().client
    if email_address:
        # 接收到请求发送验证码，首先检查是否已经发送过且在有效期，若在直接读取redis，否则生成再存到redis
        try:
            e_code = r.get(EMAIL_CHECK_CODE_PREFIX + email_address)
            if e_code:
                res = send_mail(email_address, '53iq智能云开发者申请', e_code.decode())
                if res:
                    result = 'ok'
            else:
                re_code = create_eamil_code(6)
                re = send_mail(email_address, '53iq智能云开发者申请', re_code)
                if re:
                    # 将邮箱验证码保存到redis中
                    r.set(EMAIL_CHECK_CODE_PREFIX + email_address, re_code, EMAIL_CHECK_CODE_EXPIRE)
                    result = 'ok'
        except Exception as e:
            logging.getLogger('').info(str(e))
            pass
    return HttpResponse(json.dumps({'result': result}))


@login_required
def checklist(request):
    """
    审核状态视图
    :param request:
    :return:
    """
    t = 'center/checklist.html'
    return render(request, t, locals())


@login_required
def prolist(request):
    """
    审核状态视图
    :param request:
    :return:
    """
    t = 'center/prolist.html'
    return render(request, t, locals())


def active(request):
    """
    邮箱注册激活
    :param request:
    :return:
    """
    user = request.GET.get('user', '')
    if user:
        r = RedisBaseHandler().client
        try:
            # base64解密user_id
            user_b64 = base64.b64decode(user.encode(encoding='utf-8'))
            pwd = r.get(EMAIL_ACTIVE_PREFIX + user_b64.decode()).decode()
            Account.objects.create_user(user_b64.decode(), pwd, '53iq')
            user_obj = authenticate(username=user_b64.decode(), password=pwd)
            django.contrib.auth.login(request, user_obj)
            r.delete(EMAIL_ACTIVE_PREFIX + user_b64.decode())
            return HttpResponseRedirect('/center')
        except Exception as e:
            logging.getLogger('').info(str(e))
            print('e=', e)
            pass
    return HttpResponseRedirect('register')


@csrf_exempt
def forget_pwd(request):
    """
    忘记密码
    :param request:
    :return:
    """
    uid = request.GET.get('id', '')
    if request.method == 'POST':
        method = request.POST.get('type', '')
        user_id = request.POST.get('user_id', '')
        code = request.POST.get('code', '')
        if method == 'first':
            if user_id:
                res = Account.objects.filter(account_id=user_id)
                if res:
                    if code.lower() == str(request.session[SESSION_LOGIN_VALIDATE]).lower():
                        request.session[SESSION_USER_ID] = user_id
                        request.session['step1'] = 'step1'
                        return HttpResponse(json.dumps(
                            {'status': 1, 'url': '/center/forget_pwd?id=9b782e40768fc9007786b032ba7911aa',
                             'error': ''}))
                    else:
                        return HttpResponse(json.dumps({'status': 0, 'url': '', 'error': '验证码错误'}))

            return HttpResponse(json.dumps({'status': 0, 'url': '', 'error': '该帐号不存在'}))
        elif method == 'second':
            sel = request.POST.get('sel', '')
            if sel == 'phone':
                # try:
                #     user_id = request.session[SESSION_USER_ID]
                # except:
                #     pass
                re = verify_sms_code(user_id, code)
                if re['status'] == 1:
                    del request.session['step1']
                    request.session['step2'] = 'step2'
                    return HttpResponse(json.dumps(
                        {'status': 1, 'url': '/center/forget_pwd?id=36129a68e34a0c182d4e7ad279e7bd86',
                         'error': ''}))
            else:
                r = RedisBaseHandler().client
                e_code = r.get(EMAIL_CHECK_CODE_PREFIX + user_id)
                if str(e_code.decode()).lower() == str(code).lower():
                    r.delete(EMAIL_CHECK_CODE_PREFIX + user_id)
                    del request.session['step1']
                    request.session['step2'] = 'step2'
                    return HttpResponse(json.dumps(
                        {'status': 1, 'url': '/center/forget_pwd?id=36129a68e34a0c182d4e7ad279e7bd86',
                         'error': ''}))
            return HttpResponse(json.dumps({'status': 0, 'url': '', 'error': '验证码错误'}))
        elif method == 'third':
            new_pwd = request.POST.get('pwd')
            try:
                user_name = request.session[SESSION_USER_ID]
                change_user_pwd(user_name, new_pwd)
                del request.session['step2']
                return HttpResponse(json.dumps({'status': 1, 'url': '/center/login', 'error': '密码重置成功'}))
            except Exception as e:
                logging.getLogger('').info(str(e))
                pass
            return HttpResponse(json.dumps({'status': 0, 'url': '', 'error': '密码重置失败'}))
    t = 'center/forget-pwd.html'
    # md5值比较step2
    if uid == md5_en('step2'):
        if 'step1' in request.session:
            user_id = request.session[SESSION_USER_ID]
            try:
                a = Account.objects.get(account_id=user_id)
                email = a.account_email
                phone = a.account_phone
            except Exception as e:
                print(e)
                logging.getLogger('').info(str(e))
            t = 'center/forget-pwd2.html'
        else:
            # 强行访问跳到修改密码首页
            return HttpResponseRedirect('/center/forget_pwd')
    # md5值比较step3
    if uid == md5_en('step3'):
        if 'step2' in request.session:
            t = 'center/forget-pwd3.html'
        else:
            return HttpResponseRedirect('/center/forget_pwd')
    return render(request, t, locals())


@login_required
def view_rule(request):
    """
    开发者协议
    :param request:
    :return:
    """
    return render(request, 'center/rules.html', locals())


@login_required
def modify_pwd(request):
    """
    修改密码
    :param request:
    :return:
    """
    if request.method == 'POST':
        account_id = request.user.account_id
        old_pwd = request.POST.get('old_pwd', '')
        new_pwd = request.POST.get('new_pwd', '')
        new_pwd2 = request.POST.get('new_pwd2', '')
        user_id = request.POST.get('user_id', '')
        code = request.POST.get('code', '')
        if account_id == user_id:
            r = authenticate(username=account_id, password=old_pwd)
            if r:
                if code.lower() == str(request.session[SESSION_LOGIN_VALIDATE]).lower():
                    try:
                        Account.objects.change_password(account_id, new_pwd)
                        msg = '修改成功'
                    except Exception as e:
                        logging.getLogger('').info(str(e))
                        msg = '修改失败'
                    return HttpResponse(json.dumps({'status': 0, 'error': '', 'msg': msg}))
                else:
                    return HttpResponse(json.dumps({'status': 2, 'error': '验证码错误'}))
            else:
                return HttpResponse(json.dumps({'status': 1, 'error': '密码错误'}))
        else:
            return HttpResponse(json.dumps({'status': -1, 'error': '请求异常'}))
    else:
        try:
            account_id = request.user.account_id
            phone = request.user.account_phone
            email = request.user.account_email
        except Exception as e:
            logging.getLogger('').info(str(e))
    return render(request, 'center/modify-pwd.html', locals())


def callback(request):
    if request.method == 'GET':
        code = request.GET.get('code', None)
        state = request.GET.get('state', None)
        if code is None:
            return HttpResponse('微信验证失败')
        else:
            url = wx_oauth.format(APPID, APP_SECRET, code)

            # s = requests.Session()
            # s.mount('https://', MyAdapter())
            try:
                s = requests.get(url)
                ret = s.json()
            except Exception as e:
                s = requests.Session()
                s.mount('https://', MyAdapter())
                s = requests.get(url)
                ret = s.json()
            # ret = {"openid": "", "unionid": "oixkIuJaT3J3AgwVmJx2Y4D81CdM"}
            openid = ret.get('openid')
            unionid = ret.get('unionid')
            if re.match('\d{9}', state):
                # 推送微信登录消息
                try:
                    login_status = deal_wxlogin_data(unionid, state)
                except Exception as e:
                    login_status = False
                    logging.getLogger('').info('推送微信消息出错' + str(e))
                return render(request, 'center/wx-login-wait.html', locals())
            access_token = ret.get('access_token', None)
            if access_token is None:
                return HttpResponse('code值无效')
            url2 = wx_userinfo.format(access_token, openid)
            try:

                ret2 = requests.get(url2)
                ret2.encoding = 'utf8'
                ret2 = ret2.json()
            except Exception as e:
                s = requests.Session()
                s.mount('https://', MyAdapter())
                s = requests.get(url2)
                s.encoding = 'utf8'
                ret2 = s.json()
            nickname = ret2.get('nickname', '')
            co = re.compile(u'[\U00010000-\U0010ffff]')
            nickname = co.sub(r'', nickname)
            dt = datetime.datetime.now() + datetime.timedelta(days=30)
            m = hashlib.md5()
            m.update(('token_' + unionid).encode('utf-8'))
            token = m.hexdigest()
            username = "53iq_" + unionid[-8:]
            update_user_login_data(username, '123'.encode('utf8'), token, request.META.get('REMOTE_ADDR'), 'save')

            try:
                ac = Account.objects.get(account_id=username)
                ac.account_nickname = nickname
                ac.save()
                user_obj = authenticate(username=username, password='123')
                django.contrib.auth.login(request, user_obj)
                if ac.is_developer:
                    response = HttpResponseRedirect('/product/console')
                else:
                    create_developer('', '', '', 0, '', '', '', '', '', '', '', '', username, username, 2)
                    response = HttpResponseRedirect('/product/console')
                response.set_cookie(COOKIE_USER_ACCOUNT, username, expires=dt)
                response.set_cookie(AUTO_LOGIN, token, expires=dt)
                return response
            except Exception as e:
                logging.getLogger('').info("微信登录设置登录cookie出错" + str(e))
            try:
                Account.objects.create_wx_user(username, '123', openid, nickname)
                create_developer('', '', '', 0, '', '', '', '', '', '', '', '', username, username, 2)
            except Exception as e:
                logging.getLogger('').info('创建微信账号出错' + str(e), "  nickname:", nickname)
                return HttpResponse('登录失败，请尝试其他方式登录')
            user_obj = authenticate(username=username, password='123')
            django.contrib.auth.login(request, user_obj)
            response = HttpResponseRedirect('/product/controldown')
            response.set_cookie(COOKIE_USER_ACCOUNT, username, expires=dt)
            response.set_cookie(AUTO_LOGIN, token, expires=dt)
            return response
