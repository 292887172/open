# !/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import json
import random
import logging
import base64
import django
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from base.const import ConventionValue
from conf.sessionconf import *
from base.connection import RedisBaseHandler
from conf.redisconf import SMS_CHECK_CODE_PREFIX, EMAIL_CHECK_CODE_PREFIX, EMAIL_ACTIVE_PREFIX
from conf.redisconf import SMS_CHECK_CODE_EXPIRE, EMAIL_CHECK_CODE_EXPIRE, EMAIL_ACTIVE_EXPIRE
from conf.newuserconf import *
from util.auth import get_auth_user
from util.sms.SendTemplateSMS import sendTemplateSMS
from model.center.account import Account
from common.smart_helper import check_user_password, check_factory_uuid, get_factory_info
from util.email.send_email_code import send_mail
from common.validate_code import create_validate_code
from util.email.email_code import create_eamil_code
from common.developer_helper import create_developer
from util.sms.verify_code import verify_sms_code
from conf.commonconf import HOST_DOMAIN
from base.crypto import md5_en
from common.account_helper import change_user_pwd
from model.center.app import App
from common.app_helper import create_app

_convention = ConventionValue()


@csrf_exempt
@login_required
def home(request):
    """
    开发者中心
    :param request:
    :return:
    """
    if request.user.account_type == _convention.USER_IS_ADMIN:
        return HttpResponseRedirect(reverse("admin_center"))
    # 移除第三方登录标志，和注册成功标志，防止用户直接访问这两个页面
    try:
        del request.session[SESSION_LOGIN_THIRD]
        del request.session[SESSION_REGISTER_SUCCESS]
    except Exception as e:
        logging.getLogger("").info(str(e))
        pass
    if request.method == 'POST':
        # 登录账户信息
        user = request.POST.get('user', '')
        user_from = request.POST.get('user_from', '')
        # 公司团队信息
        company = request.POST.get('coName', '')
        company_url = request.POST.get('coNetUrl', '')
        company_address = request.POST.get('coAddress', '')
        company_scale = request.POST.get('coDevScale', '')

        # 联系人信息
        contact_name = request.POST.get('coContactName', '')
        contact_role = request.POST.get('coContactRole', '')
        # 联系人移动手机
        contact_mobile = request.POST.get('coContactMobile', '')
        # 联系人固定电话
        contact_phone = request.POST.get('coContactPhone', '')
        contact_qq = request.POST.get('coContactQq', '')
        contact_email = request.POST.get('devEmail', '')
        email_code = request.POST.get('devCode', '')

        # 合作厂商信息
        factory_name = request.POST.get('factory_name', '')
        factory_uuid = request.POST.get('coFacUid', '')
        r = RedisBaseHandler().client
        try:
            e_code = r.get(EMAIL_CHECK_CODE_PREFIX + contact_email)
            if str(e_code.decode()).lower() == str(email_code).lower():
                re = create_developer(company, company_url, company_address, company_scale, contact_name, contact_role,
                                      contact_mobile, contact_phone, contact_qq, contact_email, factory_name,
                                      factory_uuid, user, user_from)
                if re:
                    # 注册成功后将账号15267183467下的三个产品复制给新用户
                    for i in range(len(APP_NAME)):
                        result = create_app(re, APP_NAME[i], APP_MODEL[i], APP_CATEGORY[i], 1, APP_COMMAND[i], DEVICE_CONF[i], APP_FACTORY_UID[i], DEVICE_TYPE[i])
                        result.app_logo = APP_LOGO[i]
                        result.save()
                    return HttpResponse(json.dumps({'status': 'ok', 'msg': '基本信息已保存', 'url': 'center'}))
                else:
                    return HttpResponse(json.dumps({'status': 'error', 'msg': '登记失败，请确保信息完整'}))
            else:
                return HttpResponse(json.dumps({'status': 'error', 'msg': '验证码错误，请重新输入'}))
        except Exception as e:
            logging.getLogger('').info(str(e))
            return HttpResponse(json.dumps({'status': 'error', 'msg': '验证码失效，请重新获取'}))
    fac_info = get_factory_info(request.user.account_from_id)
    return render(request, "center/home.html", locals())


def login(request):
    if request.method == "POST":
        account = request.POST.get("account", "")
        if not account:
            msg = "<div class='ui-error-box' ><b></b><p>帐号不能为空</P></div>"
            return render(request, "center/login.html", locals())
        password = request.POST.get("password", "")
        # password = security.md5(password)
        # password = hashlib.md5(password.encode("utf-8")).hexdigest()
        # print("==============================", password)
        if not password:
            msg = "<div class='ui-error-box' ><b></b><p>请输入密码</P></div>"
            return render(request, "center/login.html", locals())
        try:
            user_obj = authenticate(username=account, password=password)

            if not user_obj:
                msg = "<div class='ui-error-box' ><b></b><p>用户名或密码错误</P></div>"
                return render(request, "center/login.html", locals())
            # 已禁用的帐号不允许登录
            if user_obj.is_forbid != 0:
                msg = "<div class='ui-error-box' ><b></b><p>该帐号已被禁用，暂时无法登录</P></div>"
                return render(request, "center/login.html", locals())
            # 登录成功后跳转回请求的页面
            uri = request.session[SESSION_REDIRECT_URI]
            uri = "/product/list"
            response = HttpResponseRedirect(uri)
            remember = request.POST.get("remember")
            if not remember:
                request.session.set_expiry(0)
            django.contrib.auth.login(request, user_obj)
            return response
        except Exception as e:
            print(e)
            logging.getLogger('').info(str(e))
            msg = "<div class='ui-error-box' ><b></b><p>不存在此用户</P></div>"
            return render(request, "center/login.html", locals())
    try:
        request.session[SESSION_REDIRECT_URI] = request.GET.get('next', "/center")
        if request.user.account_id:

            return HttpResponseRedirect("/guide")
    except Exception as e:
        logging.getLogger('').info(str(e))
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
    django.contrib.auth.logout(request)
    return HttpResponseRedirect(reverse("home"))


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
        team_persons = request.POST.get('persons', 1)
        expertise = request.POST.get('expertise', "")
        sproducts = request.POST.get('sproducts', "")
        intent = request.POST.get('intent', "")

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
        del request.session[SESSION_REGISTER_SUCCESS]
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
        print(account_id, user_id)
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
