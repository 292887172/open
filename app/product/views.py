# !/usr/bin/env python
# -*- coding: utf-8 -*-
import hashlib
import math
import os
import random
import string
import time
from functools import cmp_to_key

import requests
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, JsonResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.utils.http import urlquote
from django.views.decorators.csrf import csrf_exempt
from ebcloudstore.client import EbStore

from base.connection import Redis3_ClientDB6, Redis3_ClientDB5
from base.const import ConventionValue
from base.const import StatusCode, DefaultProtocol, DefaultSchedule
from base.util import gen_app_default_conf, get_app_default_logo
from common.account_helper import add_team_email, del_team_email
from common.app_helper import cancel_release_app
from common.app_helper import create_app, update_app_fun_widget, add_fun_id, add_mod_funs, \
    get_mod_funs, get_config_funs
from common.app_helper import del_app, save_app, check_cloud, new_mxs_data, save_control, fk_opera_data, save_version
from common.app_helper import off_app
from common.app_helper import release_app
from common.app_helper import reset_app_secret
from common.app_helper import update_app_config
from common.app_helper import update_app_info
from common.config_helper import get_device_protocol_config, get_device_function
from common.device_fun_helper import add_device_fun
from common.device_online import device_online
from common.message_helper import save_user_message
from common.mysql_helper import get_ui_static_conf, remove_up_url
from common.project_helper import get_personal_project, get_personal_project_by_key
from common.smart_helper import *
from common.util import parse_response, send_test_device_status, reverse_numeric
from conf.apiconf import *
from conf.commonconf import CLOUD_TOKEN
from conf.message import *
from conf.newuserconf import *
from conf.wxconf import *
from model.center.account import Account
from model.center.app import App
from model.center.app_info import AppInfo
from model.center.app_version import AppVersion
from model.center.doc_ui import DocUi
from model.center.firmware import Firmware
from model.center.protocol import Protocol
from model.center.user_group import UserGroup
from open.settings import BASE_DIR
from util.email.send_email_code import send_product_process_email
from util.export_excel import date_deal
from util.netutil import verify_push_url

_code = StatusCode()
_convention = ConventionValue()


@login_required
@csrf_exempt
def product_kitchen(request):
    default_apps = App.objects.filter(developer=DEFAULT_USER).filter(check_status=_convention.APP_DEFAULT)
    return render(request, "product/kitchen.html", locals())


def product_community(request):
    return render(request, "product/community.html", locals())


@login_required
@csrf_exempt
def product_list(request):
    """
    应用列表
    :param request:
    :return:
    """

    def get():
        # 在一个固定账号下查看是否有三个默认的产品，缺少任何一个则创建该产品，有则跳过
        tmp_apps = App.objects.filter(developer=DEFAULT_USER).filter(check_status=_convention.APP_DEFAULT)
        app_names = []
        for tmp_app in tmp_apps:
            app_names.append(tmp_app.app_name)
        try:
            if request.user.developer:  # 获取验证信息
                developer = request.user.developer
            else:
                developer = ''
            keyword = request.GET.get("search", "")  # 后续搜索操作
            if keyword:
                user_apps = developer.developer_related_app.all().filter(app_name__contains=keyword).order_by(
                    "-app_update_date")

            else:
                user_apps = developer.developer_related_app.all().order_by("-app_update_date")
                # user_apps1 = developer.developer_related_app.all().order_by("-app_update_date")[3:]
        except Exception as e:
            user_apps = []
            developer = ''
            keyword = ''
            print(e, '问题')
        # 共享的产品,通过email关联， 账号本身就是邮箱的直接用邮箱查找，否则用绑定的邮箱查找
        try:
            if "@" in request.user.account_id:
                u = UserGroup.objects.filter(user_account=request.user)
            else:
                u = UserGroup.objects.filter(user_account=request.user.account_email)
        except Exception as e:
            u = UserGroup.objects.filter(user_account=request.user)
        # 已经发布, 未发布, 正在请求发布，未通过审核,默认状态
        tmp_apps = []
        #  默认三款产品类型 unpublished_apps
        default_apps = App.objects.filter(developer=DEFAULT_USER).filter(check_status=_convention.APP_DEFAULT)
        for app in user_apps:

            av = AppVersion.objects.filter(app_id=app.app_id)
            if av.count() > 0:
                has_version = 1
            else:
                has_version = 0
            tmp = {
                "app_id": app.app_id,
                "app_logo": app.app_logo,
                "app_name": app.app_name,
                "app_model": app.app_model,
                "app_device_type": app.app_device_type,
                "app_create_source": app.app_create_source,
                "app_group": app.app_group,
                "check_status": app.check_status,
                "app_update_date": app.app_update_date,
                "is_share": 0,
                "has_version": has_version,
                "app_screen_size": app.app_screen_size

            }
            tmp_apps.append(tmp)

        for i in u:
            relate_app = App.objects.filter(group_id=i.group.group_id)
            for j in relate_app:
                av = AppVersion.objects.filter(app_id=j.app_id)
                if av.count() > 0:
                    has_version = 1
                else:
                    has_version = 0
                tmp = {
                    "app_id": j.app_id,
                    "app_logo": j.app_logo,
                    "app_name": j.app_name,
                    "app_model": j.app_model,
                    "app_device_type": j.app_device_type,
                    "app_create_source": j.app_create_source,
                    "app_group": j.app_group,
                    "check_status": j.check_status,
                    "app_update_date": j.app_update_date,
                    "is_share": 1,
                    "has_version": has_version,
                    "app_screen_size": j.app_screen_size

                }
                tmp_apps.append(tmp)
        tmp_apps = sorted(tmp_apps, key=lambda a: a['app_update_date'], reverse=True)
        unpublished_apps = tmp_apps[:3]
        published_apps = tmp_apps[3:]
        template = "product/list.html"
        content = dict(
            keyword=keyword,
            developer=developer,
            unpublished_apps=unpublished_apps,
            published_apps=published_apps,
            default_apps=default_apps,
        )
        return render(request, template, content)

    def post():
        res = dict(
            code=10000
        )
        app_id = request.POST.get("app_id", "")
        action = request.POST.get("action", "")
        export = request.POST.get("name", "")
        # ui = request.POST.get("ui", "")
        if export == "export":
            ret = date_deal(app_id)
            return ret
        if app_id and action in ("del", "del"):

            if action == "del":
                app = App.objects.get(app_id=int(app_id))
                key = app.app_appid[-8:]
                del_protocol_conf(key)
                ret = del_app(app_id)
                res["data"] = ret
                r = Redis3_ClientDB6
                r.delete("product_funs" + app_id)
                return HttpResponse(json.dumps(res, separators=(",", ":")))
        else:
            res["code"] = 10002
        return HttpResponse(json.dumps(res, separators=(",", ":")))

    if request.method == "GET":
        return get()
    elif request.method == "POST":
        return post()


@login_required
@csrf_exempt
def product_controldown(request):
    """
    产品控制台
    :param request:
    :return:
    """

    def get():
        # 在一个固定账号下查看是否有三个默认的产品，缺少任何一个则创建该产品，有则跳过
        tmp_apps = App.objects.filter(developer=DEFAULT_USER).filter(check_status=_convention.APP_DEFAULT)
        app_names = []
        for tmp_app in tmp_apps:
            app_names.append(tmp_app.app_name)
        try:
            if request.user.developer:  # 获取验证信息

                developer = request.user.developer
            else:
                developer = ''
            keyword = request.GET.get("search", "")  # 后续搜索操作
            if keyword:
                user_apps = developer.developer_related_app.all().filter(app_name__contains=keyword).order_by(
                    "-app_update_date")[0:5]
            else:
                user_apps = developer.developer_related_app.all().order_by("-app_update_date")[0:5]
        except Exception as e:
            user_apps = []
            developer = ''
            keyword = ''
            print(e)
        # 已经发布, 未发布, 正在请求发布，未通过审核,默认状态
        # published_apps = []
        unpublished_apps = []
        tmp_apps = []
        #  默认三款产品类型 unpublished_apps
        default_apps = App.objects.filter(developer=DEFAULT_USER).filter(check_status=_convention.APP_DEFAULT)
        for app in user_apps:
            tmp = {
                "app_id": app.app_id,
                "app_name": app.app_name,
                "app_device_type": app.app_device_type,
                "app_create_source": app.app_create_source,
                "check_status": app.check_status,
                "app_update_date": app.app_update_date,
                "is_share": 0,
                "app_screen_size": app.app_screen_size

            }
            tmp_apps.append(tmp)
        # 分享产品
        try:
            if "@" in request.user.account_id:
                u = UserGroup.objects.filter(user_account=request.user)
            else:
                u = UserGroup.objects.filter(user_account=request.user.account_email)
        except Exception as e:
            u = UserGroup.objects.filter(user_account=request.user)
        for i in u:
            relate_app = App.objects.filter(group_id=i.group.group_id)
            for j in relate_app:
                tmp = {
                    "app_id": j.app_id,
                    "app_name": j.app_name,
                    "app_device_type": j.app_device_type,
                    "app_create_source": j.app_create_source,
                    "check_status": j.check_status,
                    "app_update_date": j.app_update_date,
                    "is_share": 1,
                    "app_screen_size": j.app_screen_size
                }
                tmp_apps.append(tmp)
        tmp_apps = sorted(tmp_apps, key=lambda a: a['app_update_date'], reverse=True)
        unpublished_apps = tmp_apps[:5]
        template = "product/controldown.html"
        print(request.COOKIES['COOKIE_USER_ACCOUNT'])
        users = request.COOKIES['COOKIE_USER_ACCOUNT']
        Uobj = Account.objects.filter(account_id=users)
        if Uobj:
            try:
                for i in Uobj:
                    if i.account_email in ['gaowei@53iq.com', 'guoyh@53iq.com', 'rendy@53iq.com', 'zhangjian@53iq.com',
                                           'guodl@53iq.com',
                                           'taosheng@53iq.com', 'dev@53iq.com', 'yangxy@53iq.com', '292887172@qq.com',
                                           'likuo@53iq.com']:
                        if not unpublished_apps:
                            fireware = ''
                        else:
                            fireware = Firmware.objects.all()
                    else:
                        fireware = ''
            except Exception as e:
                print(e)
                fireware = ''
        else:
            fireware = ''
        content = dict(
            keyword=keyword,
            developer=developer,
            unpublished_apps=unpublished_apps,
            default_apps=default_apps,
            fireware=fireware

        )

        return render(request, template, content)

    def post():
        res = dict(
            code=10000
        )
        app_id = request.POST.get("app_id", "")
        action = request.POST.get("action", "")
        export = request.POST.get("name", "")
        # ui = request.POST.get("ui", "")
        if export == "export":
            ret = date_deal(app_id)
            return ret
        if app_id and action in ("del", "del"):

            if action == "del":
                app = App.objects.get(app_id=int(app_id))
                key = app.app_appid[-8:]
                del_protocol_conf(key)
                ret = del_app(app_id)
                res["data"] = ret
                r = Redis3_ClientDB6
                r.delete("product_funs" + app_id)
                return HttpResponse(json.dumps(res, separators=(",", ":")))
        else:
            res["code"] = 10002
        return HttpResponse(json.dumps(res, separators=(",", ":")))

    if request.method == "GET":
        return get()
    elif request.method == "POST":
        return post()


@csrf_exempt
@login_required
def product_add(request):
    """
    添加应用
    :param request:
    :return:
    """
    ret = dict(
        code=0
    )

    def get():
        if not request.user.developer:
            return HttpResponseRedirect(reverse("center"))
        else:
            developer = request.user.developer
        factory_list = get_factory_list()  # 厂家列表
        template = "product/add.html"
        default_apps = App.objects.filter(developer=DEFAULT_USER).filter(check_status=_convention.APP_DEFAULT)
        content = dict(
            developer=developer,
            factory_list=factory_list,
            default_apps=default_apps
        )
        return render(request, template, content)

    def post():

        developer_id = request.POST.get("developer_id", "")
        app_name = request.POST.get("product_name", "")
        app_category = request.POST.get("product_category", "厨房类")
        app_category_detail = request.POST.get("product_category_detail", 0)  # 产品类型
        app_category_detail2 = request.POST.get("product_category_detail2", 0)
        app_product_fast = request.POST.get("product_fast", 0)

        if app_category_detail and app_category_detail2:
            try:
                app_category_detail = int(app_category_detail)
                app_category_detail2 = int(app_category_detail2)
            except Exception as e:
                app_category_detail = 0
                app_category_detail2 = 0
                print(e)
        if app_product_fast:
            try:
                app_product_fast = int(app_product_fast)
            except Exception as e:
                app_product_fast = 0
                print(e)
        factory_name = request.POST.get("brandName", "")
        app_factory_id = get_factory_id(factory_name)
        app_model = request.POST.get("product_model", "")
        app_command = request.POST.get("product_command", "")
        app_group = request.POST.get("product_group", "")
        device_conf = get_config_funs(developer_id, app_category_detail)
        app_logo = get_app_default_logo(app_category_detail)
        if not developer_id:
            ret["code"] = 100001
            ret["msg"] = "missing developer_id"
            ret["message"] = "缺少开发者账号ID"
            url = '/center'
            return HttpResponseRedirect(url)
        # 创建一个app
        try:
            if not developer_id or not app_name or not app_category_detail or not app_command \
                    or not app_group:
                ret["code"] = 100002
                ret["msg"] = "invalid app_id"
                ret["message"] = "无效的APP_ID"
                return HttpResponse(json.dumps(ret, separators=(",", ':')))
            #  根据创建者和产品类型判断用户是否创建过此类型产品

            app_id = create_app(developer_id, app_name, app_model, app_category, app_category_detail, app_command,
                                device_conf, app_factory_id, app_group, app_logo, app_product_fast, 0,
                                app_category_detail2)
            from common.celerytask import add
            add.delay(app_id)
            # 创建app版本号

            #app = App.objects.get(app_id=app_id)
            # try:
            #     if app.device_conf:
            #         opera_data = json.loads(app.device_conf)
            #         # save_version(app, opera_data)
            # except Exception as e:
            #     print(e)

            if app_product_fast:
                return HttpResponse(json.dumps({"code": 0, "appid": app_id}, separators=(",", ':')))
            url = '/product/main/?ID=' + str(app_id) + '#/portal'
            return HttpResponseRedirect(url)
        except Exception as e:
            print(e)
            logging.getLogger("root").error(e)
            logging.getLogger("root").error("创建应用失败")
            ret["code"] = 100004
            ret["msg"] = "created app error"
            ret["message"] = "创建应用失败"
            return HttpResponse(json.dumps(ret, separators=(",", ':')))

    if request.method == "GET":
        return get()
    elif request.method == "POST":
        return post()


# ----------------------------------- angular.js -----------------------------------

@login_required
@csrf_exempt
def product_main(request):
    """
    应用详情
    :param request:
    :return:
    """

    def get():
        # 上传图片回调
        res = request.GET.get("res", "")
        data = request.GET.get("data", '')
        if data:
            return JsonResponse({"xx": "xxx"})
        if res:
            return HttpResponse(res)
        if not request.user.developer:
            developer = ''
        else:
            developer = request.user.developer
        # 判断该产品ID是否是此用户所有或者是协同开发
        # 只判断了该产品是否存在！

        try:
            user_related_app = App.objects.filter(developer=developer)
            app_id = request.GET.get("ID", "")
            user_apps = App.objects.filter(app_id=int(app_id))

            if not user_apps:
                user_apps = App.objects.filter(developer=DEFAULT_USER, app_id=int(app_id))
        except Exception as e:
            print(e, '有问题')
            logging.getLogger('').info("应用出错", str(e))
            return HttpResponseRedirect(reverse("product/list"))
        if not user_apps:
            return HttpResponseRedirect(reverse("product/list"))
        # 判断该产品是否属于这个用户,该产品是否是分享过来的
        try:
            user_login = request.COOKIES['COOKIE_USER_ACCOUNT']
            app_ids = request.GET.get("ID", "")
            user_appsd = App.objects.filter(developer__developer_account=user_login,app_id=app_ids)
            if '@' in user_login:
                user_appss = UserGroup.objects.filter(group_id=[i.group_id for i in App.objects.filter(app_id=app_ids)][0],user_account=user_login)
            else:
                user_appss = UserGroup.objects.filter(group_id=[i.group_id for i in App.objects.filter(app_id=app_ids)][0],user_account=[j.account_email for j in Account.objects.filter(account_id=user_login)][0])
            if not user_appsd:
                if not user_appss:
                    return HttpResponseRedirect(reverse("product/list"))
                else:
                    pass
            else:
                pass
        except Exception as e:
            print(e, '有问题')
            logging.getLogger('').info("应用出错", str(e))
            return HttpResponseRedirect(reverse("product/list"))

        app = user_apps[0]
        all_app = []

        for a in user_related_app:
            tmp = {
                "app_id": a.app_id,
                "app_name": a.app_name,
                "check_status": a.check_status,
                "app_update_date": a.app_update_date,
                "is_share": 0

            }
            all_app.append(tmp)
        # 分享产品
        try:
            if "@" in request.user.account_id:
                u = UserGroup.objects.filter(user_account=request.user)
            else:
                u = UserGroup.objects.filter(user_account=request.user.account_email)
        except Exception as e:
            u = UserGroup.objects.filter(user_account=request.user)
        for i in u:
            relate_app = App.objects.filter(group_id=i.group.group_id)
            for j in relate_app:
                tmp = {
                    "app_id": j.app_id,
                    "app_name": j.app_name,
                    "check_status": j.check_status,
                    "app_update_date": j.app_update_date,
                    "is_share": 1
                }
                all_app.append(tmp)
        all_app = sorted(all_app, key=lambda a: a['app_update_date'], reverse=True)

        device_name = get_device_type(app.app_device_type)

        # g = Group.objects.get(group_id=app.group_id)
        teams = []
        ug = UserGroup.objects.filter(group=app.group_id)
        for j in ug:
            teams.append(j.user_account)
        # 获取这个app的API接口列表
        # api_handler = ApiHandler(app.app_level, app.app_group)
        # api_list = api_handler.api_list
        band_name = get_factory_name(app.app_factory_uid)
        app_key = app.app_appid
        key = app_key[-8:]
        template = "product/main.html"
        default_apps = App.objects.filter(developer=DEFAULT_USER).filter(check_status=_convention.APP_DEFAULT)
        content = dict(
            all_app=all_app,
            app=app,
            teams=teams,
            default_apps=default_apps,
            key=key,
            device_name=device_name,
            band_name=band_name,
        )

        return render(request, template, locals())
    def find(id, opera_data):
        for i in range(len(opera_data)):
            if str(opera_data[i]['id']) == id:
                return [i, opera_data[i]]
        return []

    def findd(opera_data):

        return opera_data

    def findname(names, opera_data):
        names_list = eval(names)
        names = []
        for i in range(len(opera_data)):
            for j in names_list:
                if str(opera_data[i]['Stream_ID']) == j:
                    names.append(opera_data[i]['name'])
        return names

    def post():
        # data_protocol = json.loads(request.body.decode('utf-8')).get('key','')
        # data_protocol_list = json.loads(request.body.decode('utf-8'))
        app_id = request.GET.get("ID", "")
        cook_ies = request.COOKIES['COOKIE_USER_ACCOUNT']
        post_data = request.POST.get("name")

        id = request.POST.get("id")
        r = Redis3_ClientDB6
        standa = request.POST.get("is_standa", None)  # 标准、自定义
        # 根据ID获取到数据库中的设备配置信息
        app = App.objects.get(app_id=app_id)
        device_conf = gen_app_default_conf(app.app_device_type)
        opera_data = []
        opera_data_new = []
        try:
            if app.device_conf:
                opera_data = json.loads(app.device_conf)
                opera_data_new = opera_data

                opera_data = opera_data

                if len(opera_data) <2:
                    pass
                else:
                    opera_data.sort(key=lambda x: int(x.get("id")))
        except Exception as e:
            logging.info("读取数据库中设备配置信息失败", e)
            print(e)
        # 接收页面请求信
        if post_data == 'list':
            # 显示所有列表信息
            page = int(request.POST.get("page", 1))
            rows = int(request.POST.get("rows", 10))
            temp = []
            for line in opera_data:
                # if str(line.get("standa_or_define")) == str(standa):
                temp.append(line)
            data = {'rows': opera_data, 'check_state': app.check_status}
            data["rows"] = temp[(page - 1) * rows:page * rows]
            data["total"] = len(temp) // rows + 1
            data["records"] = len(temp)
            return JsonResponse(data)
        elif post_data in ['show_mod', "add_mod"]:
            # 显示默认模板的功能  添加模板功能
            if post_data == "show_mod":
                app_device_type = app.app_device_type
                mod = get_mod_funs(opera_data, device_conf, app_device_type)
                return JsonResponse({"data": mod})
            elif post_data == "add_mod":
                funs = request.POST.get("funs")
                app_device_type = app.app_device_type
                add_mod_funs(opera_data, device_conf, funs, app_device_type)
                save_app(app, opera_data, cook_ies)
                update_app_protocol(app)
                # 新增功能message
                namess = findname(funs, opera_data)
                print('xx', namess)
                for i in namess:
                    message_content = '"' + app.app_name + '"' + i + CREATE_FUN
                    save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id, app.app_appid)
                return HttpResponse('add_mod_success')
        elif post_data == 'edit':
            # 返回编辑页面信息

            if len(id) > 3:
                id = id.split("#")[0]


            edit_data = find(id, opera_data)
            mods_name = list(map(lambda x: x["Stream_ID"], device_conf))
            mods_name1 = list(map(lambda x: x["Stream_ID"], opera_data))
            mods_name.extend(mods_name1)
            mods_name = list(set(mods_name))
            if edit_data:
                edit_data = edit_data[1]
                mods_name.remove(edit_data["Stream_ID"])
                message_content = '"' + app.app_name + '"' + UPDATE_FUN
                save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id, app.app_appid)
            else:
                edit_data = ''
            return JsonResponse({'data': edit_data, 'funs': opera_data, 'mods': mods_name})

        elif post_data == 'del':
            # 删除信息
            data = find(id, opera_data)
            if data:
                i = data[0]
                fun_name = data[1].get("name")
                is_standa = data[1].get("standa_or_define", None)
                opera_data.pop(i)
                for j in range(len(opera_data)):
                    opera_data[j]['id'] = str(int(j) + int(1))
                c_data = opera_data[:len(opera_data)]
                c_data.sort(key=lambda x: int(x.get("id")))
                c_data.extend(opera_data[len(opera_data):])
                opera_data = c_data
                # 排序？？？？？？
                # replace_fun_id(opera_data, id, is_standa)
                save_app(app, opera_data, cook_ies)
                update_app_protocol(app)
                message_content = '"' + app.app_name + '"' + fun_name + DEL_FUN
                save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id, app.app_appid)
                return HttpResponse('del_success')
        elif post_data == 'del_all':
            # 这里对后台发送来对数据进行筛选,重新排序 从大到小 避免勿删除操作
            id = eval(id)
            # 删除一个与多个判断
            if isinstance(id, int):
                data = find(str(id), opera_data)
                if data:
                    i = data[0]
                    fun_name = data[1].get("name")
                    is_standa = data[1].get("standa_or_define", None)
                    opera_data.pop(i)
                    for j in range(len(opera_data)):
                        opera_data[j]['id'] = str(int(j) + int(1))
                    c_data = opera_data[:len(opera_data)]
                    c_data.sort(key=lambda x: int(x.get("id")))
                    c_data.extend(opera_data[len(opera_data):])
                    opera_data = c_data
                    # 排序？？？？？？
                    # replace_fun_id(opera_data, id, is_standa)
                    save_app(app, opera_data, cook_ies)
                    update_app_protocol(app)
                    message_content = '"' + app.app_name + '"' + fun_name + DEL_FUN
                    save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id, app.app_appid)
            else:
                ids_list = list(id)
                ids_list = sorted(ids_list, key=cmp_to_key(reverse_numeric))
                for id_i in ids_list:
                    data = find(str(id_i), opera_data)
                    if data:
                        i = data[0]
                        fun_name = data[1].get("name")
                        is_standa = data[1].get("standa_or_define", None)
                        opera_data.pop(i)
                        for j in range(len(opera_data)):
                            opera_data[j]['id'] = str(int(j) + int(1))
                        c_data = opera_data[:len(opera_data)]
                        c_data.sort(key=lambda x: int(x.get("id")))
                        c_data.extend(opera_data[len(opera_data):])
                        opera_data = c_data
                        # 排序？？？？？？
                        # replace_fun_id(opera_data, id, is_standa)
                        save_app(app, opera_data, cook_ies)
                        update_app_protocol(app)
                        message_content = '"' + app.app_name + '"' + fun_name + DEL_FUN
                        save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id, app.app_appid)

            return HttpResponse('del_success')



        elif post_data == 'update':
            funs = request.POST.get("funs")
            funs = json.loads(funs)
            try:
                for j in range(len(funs)):
                    for i in funs:
                        if opera_data[j]['Stream_ID'] == i or opera_data[j]['Stream_ID'] == i.split("自定义")[0]:
                            opera_data[j]['id'] = str(int(funs.index(i)) + int(1))
                c_data = opera_data[:len(funs)]
                c_data.sort(key=lambda x: int(x.get("id")))
                c_data.extend(opera_data[len(funs):])
                save_app(app, c_data, cook_ies)
            except Exception as e:
                print(e)
            update_app_protocol(app)

            message_content = '"' + app.app_name + '"' + "功能" + UPDATE_APP_CONFIG
            save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id, app.app_appid)
            return HttpResponse('update_success')
        elif post_data == 'toSwitch':
            for switch in opera_data:
                if int(switch["id"]) == int(id):
                    switch["toSwitch"] = 1
                else:
                    switch["toSwitch"] = 0
            save_app(app, opera_data, cook_ies)
            update_app_protocol(app)

            return HttpResponse('select_success')
        elif post_data in ['isShow', 'isControl', 'isDisplay', "isCloudMenu"]:
            val = request.POST.get("dd")
            data = find(id, opera_data)
            if data:
                data[1][post_data] = val
                fun_name = data[1].get("name")
                if post_data == "isCloudMenu":
                    app.app_is_cloudmenu_device = check_cloud(opera_data)
                save_app(app, opera_data, cook_ies)
                update_app_protocol(app)
                if val == str(1):
                    message_content = '"' + app.app_name + '"' + fun_name + UPDATE_FUN_OPEN
                else:
                    message_content = '"' + app.app_name + '"' + fun_name + UPDATE_FUN_CLOSE
                save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id, app.app_appid)
                return HttpResponse('change_success')
        elif post_data == "export":
            res = date_deal(app_id)
            # print(type(res),res)
            return res
        elif post_data == "save_conf":
            if str(app.app_group) == '2':
                res = update_app_protocol(app)
                if res:
                    data = {'code': 0, 'msg': 'ok'}
                else:
                    data = {'code': -1, 'msg': '请先完善产品功能配置信息'}
                return JsonResponse(data)
            else:
                data = {'code': -1, 'msg': '该产品暂不支持调试'}
                return JsonResponse(data)
        elif post_data == 'save':
            # 接收要编辑或者添加的数据
            indata = request.POST.get('d')
            indata = json.loads(indata)
            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            indata["time"] = dt
            indata["widget"] = update_app_fun_widget(indata)
            indata["isDisplay"] = 1
            try:
                indata['control'] = new_mxs_data(indata['control'])
            except Exception as e:
                print(e)
            fun_name = indata['name']
            if indata["id"]:
                # 编辑参数信息
                data = find(indata['id'], opera_data)
                data[1].update(indata)
                message_content = '"' + app.app_name + '"' + fun_name + UPDATE_FUN
                tt = "modify_success"
                save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id, app.app_appid)
            else:
                # 添加一条参数信息需要申请审核
                indata = add_fun_id(opera_data, indata)
                add_device_fun(app.app_appid, indata)
                opera_data.append(indata)
                opera_data.sort(key=lambda x: int(x.get("id")))
                # message_content = '"' + app.app_name + '"' + fun_name + CREATE_FUN
                tt = "modify_success"
            # 版本区别,在新版本加{"version":"1"} # 区分方法control
            #opera_data = save_control(opera_data)
            save_app(app, opera_data, cook_ies)
            update_app_protocol(app)
            return HttpResponse(tt)

        # 获取设备列表
        elif post_data == 'device_table':
            r5 = Redis3_ClientDB5
            key = app.app_appid
            key = key[-8:]
            device_content = DEVICE + "_" + key
            if r5.exists(device_content):
                device_list = r5.get(device_content)
                device_list = json.loads(device_list.decode())
            else:
                device_list = get_device_list(app.app_appid)
                r5.set(device_content, json.dumps(device_list), 1 * 60)
            for k in device_list:
                is_online = device_online(k['ebf_device_id'])
                k["is_online"] = is_online
            return JsonResponse({'data': device_list, 'key': key, 'check_state': app.check_status})
        # 获取工厂列表
        data = request.POST.get("data", "")
        if data == "factory_list":
            factory_list = get_factory_list()
            return JsonResponse({'data': factory_list})
        #  app操作
        res = dict(
            code=10000
        )
        action = request.POST.get("action", "")
        app_id = request.POST.get("app_id", "")
        app_name = request.POST.get("app_name", "")
        app_model = request.POST.get("app_model", "")
        app_describe = request.POST.get("app_describe", "")
        app_site = request.POST.get("app_site", "")
        app_logo = request.POST.get("app_logo", "")
        app_push_url = request.POST.get("app_config_push_url", "")
        app_push_token = request.POST.get("app_config_push_token", "")
        app_command = request.POST.get("app_command", "")
        app_group = request.POST.get("app_group", "")
        app_factory_uid = request.POST.get("app_factory_uid", "")
        if action in ("cancel_release_product", "off_product", "release_product",
                      "update_info", "update_config", "reset_app_secret"):
            if action == "release_product":
                # 发布应用
                ret = release_app(app_id)
                res["data"] = ret
                return HttpResponse(json.dumps(res, separators=(",", ":")))
            elif action == "cancel_release_product":
                # 取消发布
                ret = cancel_release_app(app_id)
                res["data"] = ret
                return HttpResponse(json.dumps(res, separators=(",", ":")))
            elif action == "off_product":
                # 下架
                ret = off_app(app_id)
                res["data"] = ret
                return HttpResponse(json.dumps(res, separators=(",", ":")))
            elif action == "update_info":
                # 更新基本信息
                ret = update_app_info(app_id, app_name, app_model, app_describe, app_site, app_logo,
                                      app_command, app_group, app_factory_uid)
                logging.getLogger('').info("ss_ret" + str(ret))
                if ret:
                    update_app_protocol(app)
                res["data"] = ret
                logging.getLogger('').info("data" + str(res))
                return HttpResponse(json.dumps(res, separators=(",", ":")))
            elif action == "update_config":
                # 更新配置信息
                # 先验证填写的url地址是否正确
                result = verify_push_url(app_push_url, app_push_token)
                if result:
                    ret = update_app_config(app_id, app_push_url, app_push_token)
                    res["data"] = ret
                    return HttpResponse(json.dumps(res, separators=(",", ":")))
                else:
                    return HttpResponse(json.dumps({'code': -2}))
            elif action == "reset_app_secret":
                # 重置密钥
                ret = reset_app_secret(app_id)
                res["data"] = ret
                return HttpResponse(json.dumps(res, separators=(",", ":")))
        return HttpResponse(json.dumps(res, separators=(",", ":")))

    if request.method == "GET":
        return get()

    elif request.method == "POST":
        return post()


@csrf_exempt
def protocol(request):
    # code说明 1 非表 2 标准 3 错误
    if request.method == 'GET':
        # 协议类型 1为下行 0为上行
        device_key = request.GET.get('key', '')
        zdy = request.GET.get('zdy', '')
        action = request.GET.get('action', '')
        protocol_type = request.GET.get('protocol_type', '0')
        pt = ''
        screen = request.GET.get('screen', '')
        device_types = request.GET.get('device_types', '')
        if action == "get_project":

            print(screen, 'screen')
            if device_types == '油烟机' or device_types == '集成灶':
                if screen == '6.8寸长条屏':
                    print('-------')
                    project_path = BASE_DIR + '/static/sdk/wifi_68.zip'
                    pth = get_personal_project_by_key(project_path, device_key, 'zip')
                    logging.getLogger('').info(pth)
                    pt = 'http://' + request.META['HTTP_HOST'] + '/static/sdk/' + os.path.basename(pth)
                    logging.getLogger('').info(pt)
                else:
                    print('========')
                    p = get_device_protocol_config(device_key)
                    if p:
                        p0 = p[0]
                        p1 = p[1]
                    else:
                        p0, p1 = False, False
                    d = get_device_function(device_key)
                    project_path = BASE_DIR + '/static/sdk/WiFiIot.zip'
                    pth = get_personal_project(project_path, device_key, d, p0, p1)
                    logging.getLogger('').info(pth)
                    pt = 'http://' + request.META['HTTP_HOST'] + '/static/sdk/WiFiIot_' + device_key + '.zip'
                    logging.getLogger('').info(pt)

            return JsonResponse({"code": 0, "url": pt})
        if action == "get_projects":

            if device_types == '油烟机' or device_types == '集成灶':
                if screen == '6.8寸长条屏':
                    project_path = BASE_DIR + '/static/sdk/wifi_68.zip'
                    pth = get_personal_project_by_key(project_path, device_key, 'lua')
                    logging.getLogger('').info(pth)
                    pt = 'http://' + request.META['HTTP_HOST'] + '/static/sdk/' + os.path.basename(pth)
                    logging.getLogger('').info(pt)
                else:
                    p = get_device_protocol_config(device_key)
                    if p:
                        p0 = p[0]  # 上行
                        p1 = p[1]  # 下行
                    else:
                        p0, p1 = False, False
                    d = get_device_function(device_key)
                    project_path = BASE_DIR + '/static/sdk/WiFiIot.zip'
                    # pth = get_personal_project(project_path, device_key, d, p0, p1)
                    pth = get_personal_project(project_path, device_key, d, p0, p1, 'lua')
                    logging.getLogger('').info(pth)
                    pt = 'http://' + request.META['HTTP_HOST'] + '/static/sdk/main_' + device_key + '.lua'
                    logging.getLogger('').info(pt)


            return JsonResponse({"code": 0, "url": pt})

        if action == 'get_data_content':
            app = App.objects.get(app_appid__endswith=device_key)
            dc = json.loads(app.device_conf)
            data = []
            for i in dc:
                tmp = {'id': i['id'], 'title': i['name'], 'length': i['mxsLength'], 'mxs': i['mxs']}
                data.append(tmp)
            return HttpResponse(json.dumps(data))
        elif action == 'get_frame_data':
            # 帧结构数据
            try:
                mlist = Protocol.objects.all().filter(protocol_device_key=device_key)
                if len(mlist) == 0:
                    # 没有定义过，返回标准协议，若请求自定义协议，则返回默认标准自定义协议
                    if zdy == '1':
                        p = DefaultProtocol().DEFAULT_DATA_ZDY
                        data = {"code": 2, "data": p, "protocol_type": protocol_type}
                    else:
                        # p = DefaultProtocol().DEFAULT_DATA
                        p = DefaultProtocol().DEFAULT_DATA_ZDY
                        data = {"code": 2, "data": p, "protocol_type": protocol_type}
                    return HttpResponse(json.dumps(data))
                else:
                    # 根据请求，返回定义的上下行数据
                    for iii in mlist:
                        res_list_data = iii.protocol_factory_content
                        protocol_type1 = iii.protocol_factory_type
                        res_list_data1 = json.loads(res_list_data)

                        res_list_data1['protocol_type'] = protocol_type1

                        if str(protocol_type1) == str(protocol_type):
                            data = {"code": 2, "data": res_list_data1, "protocol_type": protocol_type}
                            return HttpResponse(json.dumps(data))
                    # 请求的数据暂时未定义，比如自定义了上行数据，请求下行数据，或者自定义了下行数据，请求上行数据
                    # 返回空， 前端不处理
                    data = {"code": 1, "data": "", "protocol_type": protocol_type}
                    return HttpResponse(json.dumps(data))
            except Exception as e:
                print(e)
                logging.getLogger('').info("传入的参数zdy出错", str(e))
                data = {"code": 3, "data": DefaultProtocol().DEFAULT_DATA_ZDY, "protocol_type": 0}
                return HttpResponse(json.dumps(data))

    if request.method == "POST":
        r = DefaultProtocol().DEFAULT_DATA_ZDY

        data_protocol_list = json.loads(request.body.decode('utf-8'))
        cook_ies = request.COOKIES['COOKIE_USER_ACCOUNT']

        try:
            if data_protocol_list.get('action', '') == 'update_protocol':
                data_sql = {}
                protocol_type = data_protocol_list.get('protocol_type', 0)
                protocol_endian = data_protocol_list.get("protocol_endian", 1)
                list_t = data_protocol_list.get('frame_content', '')
                list_key = data_protocol_list.get('key', '')
                data_sql['is_single_instruction'] = True
                data_sql['support_response_frame'] = True
                data_sql['support_serial'] = True
                data_sql['active_heartbeat'] = True
                data_sql['support_repeat'] = True
                data_sql['heart_rate'] = "500"
                data_sql['repeat_rate'] = "500"
                data_sql['repeat_count'] = "3"
                data_sql['endian_type'] = protocol_endian  # 1:大端编码， 0：小端编码， 默认大端编码

                tmp_list_t = []
                for i in list_t:
                    if i.get("is_enable", None):
                        tmp_f = {
                            "id": i.get("id"),
                            "length": i.get("length"),
                            "name": i.get("name"),
                            "title": i.get("title"),
                            "value": i.get("value"),
                            "is_enable": i.get("is_enable")
                        }
                    else:
                        tmp_f = {
                            "id": i.get("id"),
                            "length": i.get("length"),
                            "name": i.get("name"),
                            "title": i.get("title"),
                            "value": i.get("value")
                        }
                    if i.get("name") == "data":
                        # 处理数据域
                        l = 0
                        tmp_d = []
                        for j in i.get("value"):
                            if j.get('content'):
                                l += int(j.get('length'))
                                tmp_d.append(j)
                        tmp_f['length'] = math.ceil(l / 8)
                        tmp_f['value'] = tmp_d
                    elif i.get("name") == "check":
                        # 处理校验
                        tmp_f['value'] = {"check_algorithm": i.get('value').get("check_algorithm"),
                                          "check_start": i.get('value').get("check_start"),
                                          "check_end": i.get('value').get("check_end")}
                        data_sql['checkout_algorithm'] = i.get('value').get("check_algorithm")
                        data_sql['start_check_number'] = i.get('value').get("check_start")
                        data_sql['end_check_number'] = i.get('value').get("check_end")
                    tmp_list_t.append(tmp_f)
                data_sql['frame_content'] = tmp_list_t

                data_sql_update = json.dumps(data_sql, ensure_ascii=False)

                types = data_protocol_list.get('typesss', '')

                if types == "change":
                    # 上下行  切换
                    if protocol_type == "0":
                        update_protocol(list_key, data_sql_update, 1, cook_ies)
                        mlist = Protocol.objects.all().filter(protocol_device_key=list_key,
                                                              protocol_factory_type=0)
                    else:
                        update_protocol(list_key, data_sql_update, 0, cook_ies)
                        mlist = Protocol.objects.all().filter(protocol_device_key=list_key,
                                                              protocol_factory_type=1)
                else:
                    update_protocol(list_key, data_sql_update, protocol_type, cook_ies)
                    mlist = Protocol.objects.all().filter(protocol_device_key=list_key,
                                                          protocol_factory_type=protocol_type)
                for ii in mlist:
                    res_list_data = ii.protocol_factory_content
                    protocol_type1 = ii.protocol_factory_type

                    res_list_data1 = json.loads(res_list_data)
                    res_list_data1['protocol_type'] = protocol_type1
                    print(res_list_data1)
                    return HttpResponse(json.dumps(res_list_data1))
        except Exception as e:
            print(e)
            logging.getLogger('').info("非保存操作", str(e))
            data = {"code": 3, "data": DefaultProtocol().DEFAULT_DATA_ZDY, "protocol_type": 0}
            return HttpResponse(json.dumps(data))
        return HttpResponse(json.dumps(r))


@csrf_exempt
def key_verify(request):
    # 验证key
    if request.method == 'POST':
        key = request.POST.get("key", "")
        if not key:
            return JsonResponse(parse_response(code=_code.MISSING_APP_KEY_CODE, msg=_code.MISSING_APP_KEY_MSG))
        app = App.objects.filter(app_appid__endswith=key)
        flag = os.path.exists('static/file/' + key + '.zip')
        if app and flag:
            http_host = request.META.get('HTTP_HOST')

            url_add = 'http://' + http_host + '/static/file/' + key + '.zip'
            return JsonResponse(parse_response(code=_code.SUCCESS_CODE, msg=_code.SUCCESS_MSG, data=url_add))
        return JsonResponse(parse_response(code=_code.INVALID_APP_KEY_CODE, msg=_code.INVALID_APP_KEY_MSG))
    elif request.method == 'GET':
        return HttpResponse("hi!")


@csrf_exempt
def control(request):
    if request.method == 'POST':
        data = request.body
        data = json.loads(data.decode('utf-8'))
        send_test_device_status(data['did'], data)
        return HttpResponse(json.dumps({'code': 0}))


@csrf_exempt
def portal(request):
    if request.method == 'GET':
        date1 = request.GET.get('num', '')

        data1 = int(date1)
        # 根据id获取各个时间message_content

        t = App.objects.filter(app_id=data1)
        times = []
        for i in t:
            zy = i.app_appid[-8:]
            timess = Message.objects.filter(device_key=zy, is_read=0).order_by("-update_date")[0:3]
            for i in timess:
                i.update_date = i.update_date + datetime.timedelta(hours=8)
                tis = i.update_date.strftime("%Y-%m-%d")
                times.append({"time": tis, "message": i.message_content})

        return HttpResponse(json.dumps(times))
    elif request.method == 'POST':
        action = request.POST.get("action", "")
        app_id = request.POST.get("app_id", "")
        email = request.POST.get("email", "")
        user_account = request.user.account_id

        if action == 'submitEmail':
            # 先判断这个用户对这个产品有没有创建过分组，如果没有则创建分组，自动继承默认分组的成员,更新产品所属组信息，添加新成员
            # 若有分组，则直接在分组中添加成员
            team_info = add_team_email(user_account, app_id, email)
            return HttpResponse(json.dumps({"code": 0, "team_info": team_info}))
        elif action == 'delEmail':
            # 删除成员邮箱，先检查是否有自定义分组如果没有，则自动继承默认分组，删除相关成员，更新产品所属组信息
            # 已有自定义分组，直接删除相关成员信息
            del_team_email(user_account, app_id, email)
            return HttpResponse(json.dumps({"code": 0}))


@csrf_exempt
def app(request):
    if request.method == 'GET':
        ids = request.GET.get('id', '')
        num = request.GET.get('num', '')
        m = AppVersion.objects.filter(app_id=ids).order_by("-create_date")
        if m and num == '1':
            app_list = []
            mm = m.filter(upload_type=int(1))
            for i in mm:
                app_dict = {}
                app_dict['url'] = i.download_url
                app_dict['version'] = i.version_name
                date = i.create_date
                tis = date.strftime("%Y-%m-%d %H:%M:%S")
                app_dict['time'] = tis
                app_dict['remarks'] = i.remarks
                app_list.append(app_dict)
            return HttpResponse(json.dumps(app_list))
        elif m and num == '2':
            app_list = []
            mm = m.filter(upload_type=int(2))
            for i in mm:
                app_dict = {}
                app_dict['url'] = i.download_url
                app_dict['version'] = i.version_name
                date = i.create_date
                tis = date.strftime("%Y-%m-%d %H:%M:%S")
                app_dict['time'] = tis
                app_dict['remarks'] = i.remarks
                app_list.append(app_dict)
            return HttpResponse(json.dumps(app_list))
        else:
            return HttpResponse("")
    if request.method == "POST":
        ids = request.GET.get('id', '')
        num = request.GET.get('num', '')
        action = request.GET.get("action", '')
        version = request.GET.get('version', '')
        if action == 'del':
            AppVersion.objects.filter(app_id=ids, upload_type=int(num), version_code=version).delete()
            return HttpResponse(json.dumps({"code": 0}))
        return HttpResponse(json.dumps({"code": 1}))


@csrf_exempt
def del_upload(request):
    if request.method == "POST":
        data = request.POST.get('data','')
        print(data)
        ids = request.POST.get('id', '')
        num = request.POST.get('num', '')
        action = request.POST.get("action", '')
        version = request.POST.get('version', '')
        if action == 'del':
            AppVersion.objects.filter(app_id=ids, upload_type=int(num), version_code=version).delete()
            return HttpResponse(json.dumps({"code": 0}))
        return HttpResponse(json.dumps({"code": 1}))


@csrf_exempt
def schedule(request):
    if request.method == "GET":

        key = request.GET.get('key', '')
        sapp_id = ''
        appobj = App.objects.filter(app_appid__endswith=key)
        for i in appobj:
            sapp_id = i.app_id
        update_list = []
        bb = AppInfo.objects.filter(app_id=sapp_id)
        try:
            li_ui = DocUi.objects.filter(ui_key=key).order_by("-create_date")
            if li_ui:
                id_list = []

                for i in li_ui:
                    update_dict = {}
                    update_dict['id'] = i.ui_upload_id
                    update_dict['remark'] = i.ui_remark
                    update_dict['party'] = i.ui_party
                    update_dict['plan'] = i.ui_plan
                    id_list.append(i.ui_upload_id)
                    try:
                        if i.ui_content:
                            url = eval(i.ui_content)
                            url = sorted(url, key=lambda a: a['date'], reverse=True)
                        else:
                            url = ''
                    except Exception as e:
                        url = ''
                    if not isinstance(url, list):
                        url = [url]
                    update_dict['url'] = url

                    if len(str(url)) > int(10):
                        update_dict['show_url'] = 1
                    else:
                        update_dict['show_url'] = 0
                    update_dict['ack'] = i.ui_ack
                    update_dict['time_stemp'] = i.ui_time_stemp

                    # 负责方
                    if bb:
                        party_list = ''
                        for i in bb:
                            if i.responsible_party:
                                party_list = json.loads(i.responsible_party)
                            update_dict['partys'] = party_list
                    update_list.append(update_dict)
                    c_data = update_list[:len(update_list)]
                    c_data.sort(key=lambda x: int(x.get("id")))
                    c_data.extend(update_list[len(update_list):])
                    update_list = c_data

                return HttpResponse(json.dumps(update_list))
            else:
                r6 = Redis3_ClientDB5
                schedule_key = DefaultSchedule().DEFAULT_SCHEDULE_CHOOSE + key
                if r6.exists(schedule_key):
                    update_list = DocUi.objects.filter(ui_key=key).order_by("-create_date")
                    print('---', update_list)
                else:
                    update_list = DefaultSchedule().DEFAULT_SCHEDULE
                    r6.set(schedule_key, json.dumps(update_list))
                for i in update_list:
                    DocUi.objects.create(ui_key=key, ui_ack=0, ui_upload_id=i['id'], ui_plan=i['plan'], ui_party='',
                                         ui_remark='', ui_time_stemp='',
                                         ui_content='', ui_type='')
                return HttpResponse(json.dumps(update_list))
        except Exception as e:
            print(e)
            return HttpResponse(json.dumps(update_list))

    if request.method == "POST":
        user1 = request.COOKIES['COOKIE_USER_ACCOUNT']
        key = request.POST.get('key', '')
        num = request.POST.get('num', '')
        location = request.POST.get('location', '')
        action = request.POST.get('action', '')
        data = request.POST.get('data', '')
        if data:
            key = request.GET.get('key', '')
            data1 = json.loads(data)
            for i in range(len(data1)):
                ids = int(i) + 1
                Dobj = DocUi.objects.filter(ui_key=key, ui_upload_id=int(data1[i]))

                try:
                    Dobj.update(ui_upload_id=int(ids * 100))
                except Exception as e:
                    print(e)
            Orders = DocUi.objects.filter(ui_key=key)
            list_up_id = []
            for i in Orders:
                list_up_id.append(i.ui_upload_id)
            for isd in list_up_id:
                DocUi.objects.filter(ui_key=key, ui_upload_id=int(isd)).update(ui_upload_id=int(isd / 100))
            return HttpResponse(json.dumps({"code": 0}))

        if action == 'del':
            # 删除下载链接
            del_id = request.POST.get('del_id', '')
            del_filename = request.POST.get('del_filename', '')
            try:
                if del_id:
                    del_id = int(del_id)
                remove_up_url(key, del_id, del_filename)
                Message.objects.create(message_content='产品计划书上传文件删除', message_type=int(5),
                                       message_handler_type=int(5), is_read=1,
                                       device_key=key, message_sender=user1, message_target=user1,
                                       create_date=datetime.datetime.utcnow(),
                                       update_date=datetime.datetime.utcnow())
                return HttpResponse(json.dumps({"code": 0}))
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({"code": 1}))
        elif action == 'delxu':
            # data: {"key": keysss, "action": "delxu", "del_id": id}
            del_xu_id = request.POST.get('del_id', '')
            # 删除原有的id对应的数据 大于id的数据id自减1更新
            try:
                DocUi.objects.filter(ui_key=key, ui_upload_id=int(del_xu_id)).delete()
                del_data = DocUi.objects.filter(ui_key=key, ui_upload_id__gt=int(del_xu_id))
                for id_i in del_data:
                    DocUi.objects.filter(ui_key=key, ui_upload_id=int(id_i.ui_upload_id)).update(
                        ui_upload_id=int(id_i.ui_upload_id) * 100)
                Orders = DocUi.objects.filter(ui_key=key, ui_upload_id__gt=int(del_xu_id))
                for i in Orders:
                    is_gt = i.ui_upload_id
                    DocUi.objects.filter(ui_key=key, ui_upload_id=int(is_gt)).update(ui_upload_id=int(is_gt / 100) - 1)
                Message.objects.create(message_content='产品计划删除', message_type=int(5),
                                       message_handler_type=int(5), is_read=1,
                                       device_key=key, message_sender=user1, message_target=user1,
                                       create_date=datetime.datetime.utcnow(),
                                       update_date=datetime.datetime.utcnow())
                return HttpResponse(json.dumps({"code": 0}))
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({"code": 1}))
        elif action == 'get_detail_plan':
            detail_id = request.POST.get('id', '')
            detail_obj = DocUi.objects.filter(ui_key=key, ui_upload_id=detail_id).order_by("-create_date")
            detail_obj_dict = {}
            if detail_obj:
                for i in detail_obj:
                    detail_obj_dict['remark'] = i.ui_remark  # 备注
                    detail_obj_dict['plan'] = i.ui_plan  # 计划
                    detail_obj_dict['id'] = i.ui_upload_id  # id
                    detail_obj_dict['ack'] = i.ui_ack  # ack
                    detail_obj_dict['time_stemp'] = i.ui_time_stemp  # 时间戳
                    try:
                        if i.ui_content:
                            url = eval(i.ui_content)
                            url = sorted(url, key=lambda a: a['date'], reverse=True)
                        else:
                            url = ''
                    except Exception as e:
                        url = ''
                    if not isinstance(url, list):
                        url = [url]
                    url = json.dumps(url)
                    detail_obj_dict['content'] = url  # url
                    detail_obj_dict['party'] = i.ui_party  # 责任
                print('x', detail_obj_dict)
                return HttpResponse(json.dumps(detail_obj_dict))
            else:
                return HttpResponse(json.dumps(
                    {'remark': '', 'party': '', 'plan': '提交详细技术功能规划书', 'id': 1, 'time_stemp': '', 'ack': 0,
                     'content': '[""]'}))
        elif action == 'save_plan':
            # data: {'key': keysss, "action": "save_plan", "num": that},
            location = request.POST.get('location', '')
            m = DocUi.objects.filter(ui_key=key, ui_upload_id=num).update(ui_ack=int(1))
            modele = DocUi.objects.filter(ui_key=key, ui_upload_id=num)
            a = App.objects.filter(app_appid__endswith=key)  # 获取产品信息
            t = int(num) + int(1)
            app_name = ''  # 1
            user1 = request.COOKIES['COOKIE_USER_ACCOUNT']
            email_list = []
            group_id = ''
            for i in a:
                app_name = i.app_name
                group_id = i.group_id
            ack_name = app_name + '第' + num + '步操作确认通知'
            try:
                b = UserGroup.objects.filter(group__group_id=group_id)
                for i in b:
                    email_list.append(i.user_account)
            except Exception as e:
                print(e)
                print('没有成员')
            if DocUi.objects.filter(ui_key=key, ui_upload_id=t):
                next_stemp = [str(i.ui_plan) for i in
                              DocUi.objects.filter(ui_key=key, ui_upload_id=t)][0]
            else:
                next_stemp = '该产品即将量化'
            try:
                send_product_process_email(ack_name, app_name, BOOK[num], next_stemp, user1, email_list, location,
                                           'confirm')
                Message.objects.create(message_content=BOOK[num] + '已完成', message_type=int(5),
                                       message_handler_type=int(5),
                                       device_key=key, message_sender=user1, message_target=user1,
                                       create_date=datetime.datetime.utcnow(),
                                       update_date=datetime.datetime.utcnow())
            except Exception as e:
                print(e)
            if m:
                Message.objects.create(message_content='产品计划书更新', message_type=int(5),
                                       message_handler_type=int(5), is_read=1,
                                       device_key=key, message_sender=user1, message_target=user1,
                                       create_date=datetime.datetime.utcnow(),
                                       update_date=datetime.datetime.utcnow())
                return HttpResponse(json.dumps({"code": 0}))
            else:
                return HttpResponse(json.dumps({"code": 1}))
        elif action == 'save':
            pass
            # data: {"key": keysss, "num": idd, "plans_name": plans_name, "plans_time": plans_time,
            #      "plans_user": plans_user, "plans_remarks": plans_remarks},
            plans_name = request.POST.get('plans_name', '')
            plans_time = request.POST.get('plans_time', '')
            plans_user = request.POST.get('plans_user', '')
            plans_remarks = request.POST.get('plans_remarks', '')
            Dobj = DocUi.objects.filter(ui_key=key, ui_upload_id=num)
            try:
                if Dobj:
                    # 存在，更新

                    url_list = ''
                    for i in Dobj:
                        url_list = i.ui_content
                    Dobj.update(ui_content=url_list, ui_remark=plans_remarks, ui_party=plans_user,
                                ui_time_stemp=plans_time, ui_plan=plans_name, update_date=datetime.datetime.utcnow())
                else:
                    # 新增
                    DocUi.objects.create(ui_content='', create_date=datetime.datetime.utcnow(),
                                         update_date=datetime.datetime.utcnow(), ui_key=key, ui_upload_id=num,
                                         ui_remark=plans_remarks, ui_party=plans_user, ui_time_stemp=plans_time,
                                         ui_plan=plans_name)
                return HttpResponse(json.dumps({"code": 0}))
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({"code": 1}))
        elif action == 'plan':
            # 时间搓
            time_value = request.POST.get('value', '')
            time_id = request.POST.get('id', '')
            ddd = DocUi.objects.filter(ui_key=key, ui_upload_id=time_id)
            try:
                if ddd:
                    ddd.update(ui_plan=time_value)
                else:
                    uw = ['']
                    DocUi.objects.create(ui_plan=time_value, ui_party='', ui_time_stemp='', ui_remark='',
                                         ui_upload_id=time_id,
                                         ui_key=key, ui_content=uw, ui_type='UI', ui_title='1.0',
                                         create_date=datetime.datetime.utcnow(), update_date=datetime.datetime.utcnow())
                return HttpResponse(json.dumps({"code": 0}))
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({"code": 1}))
        else:
            modele = DocUi.objects.filter(ui_key=key, ui_upload_id=num)
            a = App.objects.filter(app_appid__endswith=key)  # 获取产品信息
            t = int(num) + int(1)
            app_name = ''  # 1
            user1 = request.COOKIES['COOKIE_USER_ACCOUNT']

            email_list = []

            group_id = ''
            for i in a:
                app_name = i.app_name
                group_id = i.group_id
            ack_name = app_name + '第' + num + '步操作确认通知'
            try:
                b = UserGroup.objects.filter(group__group_id=group_id)
                for i in b:
                    email_list.append(i.user_account)
            except Exception as e:
                print(e)
                print('没有成员')
            if t >= 9:
                next_stemp = "量产阶段"
            else:
                next_stemp = BOOK[str(t)]

            try:
                send_product_process_email(ack_name, app_name, BOOK[num], next_stemp, user1, email_list, location,
                                           'confirm')
                Message.objects.create(message_content=BOOK[num] + '已完成', message_type=int(5),
                                       message_handler_type=int(5),
                                       device_key=key, message_sender=user1, message_target=user1,
                                       create_date=datetime.datetime.utcnow(),
                                       update_date=datetime.datetime.utcnow())
            except Exception as e:
                print(e)

            if modele:
                # 确认操作
                modele.update(ui_ack=int(1))
                # 根据产品key，到docui表中去读取所有ack的id，和该key下有多少条id 根据id总数去range循环
                m = DocUi.objects.filter(ui_key=key).count()
                # 产品进度
                pp = int(modele.filter(ui_ack=int(1)).values("ui_upload_id")[0]['ui_upload_id']) + int(1)
                App.objects.filter(app_appid__endswith=key).update(app_currversion=pp)
            else:

                DocUi.objects.create(ui_ack=int(1), ui_upload_id=num, ui_time_stemp='', ui_party='', ui_remark='',

                                     ui_key=key, ui_content='', ui_type='UI', ui_title='1.0',
                                     create_date=datetime.datetime.utcnow(), update_date=datetime.datetime.utcnow())

            return HttpResponse('ok')


@csrf_exempt
def get_version(request):
    pass
    if request.method == "GET":
        key = request.GET.get('key', '')
        app = App.objects.get(app_appid__endswith=key)
        try:
            if app.device_conf:
                opera_data = json.loads(app.device_conf)
                old_or_new = fk_opera_data(opera_data)
                return HttpResponse(old_or_new)
        except Exception as e:
            print(e)
            return HttpResponse(0)


@csrf_exempt
def party(request):
    if request.method == "POST":
        user1 = request.COOKIES['COOKIE_USER_ACCOUNT']
        ap_id = request.POST.get('app_id', '')
        info_list = request.POST.get('listed', '')
        key = request.POST.get('keysss', '')
        obj = AppInfo.objects.filter(app_id=int(ap_id))
        action = request.POST.get('action', '')
        # data: {"key": keysss, "app_id": app_id1, "datas": rr},
        data_list = request.POST.get('datas', '')
        if action == 'del':
            title_list = ''
            if obj:
                try:
                    for i in obj:
                        title_list = json.loads(i.responsible_party)
                    for j in title_list:
                        if data_list in j.values():
                            title_list.remove(j)
                        else:
                            return HttpResponse(json.dumps({"code": 1}))
                    if title_list:
                        AppInfo.objects.filter(app_id=int(ap_id)).update(responsible_party=json.dumps(title_list))
                    else:
                        AppInfo.objects.filter(app_id=int(ap_id)).update(responsible_party='')
                    Message.objects.create(message_content='产品负责方更新', message_type=int(5),
                                           message_handler_type=int(5), is_read=1,
                                           device_key=key, message_sender=user1, message_target=user1,
                                           create_date=datetime.datetime.utcnow(),
                                           update_date=datetime.datetime.utcnow())
                except Exception as e:
                    print(e)
                    return HttpResponse(json.dumps({"code": 1}))
            else:
                return HttpResponse(json.dumps({"code": 1}))
            return HttpResponse(json.dumps({"code": 0}))
        else:
            list = json.loads(info_list)
            try:
                if obj:
                    obj.update(responsible_party=json.dumps(list))

                else:
                    AppInfo.objects.create(app_id=int(ap_id), responsible_party=json.dumps(list))
                Message.objects.create(message_content='产品负责方更新', message_type=int(5),
                                       message_handler_type=int(5), is_read=1,
                                       device_key=key, message_sender=user1, message_target=user1,
                                       create_date=datetime.datetime.utcnow(),
                                       update_date=datetime.datetime.utcnow())
            except Exception as e:
                print(e)
            return HttpResponse(json.dumps({"code": 0}))
        # data: {"key": keysss, "app_id": app_id1, "list": aa},


@csrf_exempt
def upload_file(request):
    try:
        if len(request.FILES.dict()) >= 1:
            f = request.FILES["productImgFile"]
            store = EbStore(CLOUD_TOKEN)
            r = store.upload(f.read(), f.name, f.content_type)
            ret = json.loads(r)
            if ret["code"] == 0:
                print("上传成功")
            else:
                print(ret["msg"])
                logging.getLogger("").info(r["msg"])
            data = ret["data"]
            return HttpResponse(data)
    except Exception as e:
        print(e)
    if request.method == 'POST':
        cook_ies = request.COOKIES['COOKIE_USER_ACCOUNT']
        file = request.FILES.get("file", '')
        post_data = request.POST.get('name', '')
        key = request.POST.get('key', '')
        id = request.POST.get('id', '')
        location = request.POST.get('location', '')
        # action 判断
        action = request.POST.get('action', '')
        app_ids = request.POST.get('app_id', '')
        app_version = request.POST.get('app_version', '')
        appversion_remark = request.POST.get('app_remark', '')
        if action == 'ui_upload':
            try:
                store = EbStore(CLOUD_TOKEN)
                rr = store.upload(file.read(), file.name, file.content_type)
                rr = json.loads(rr)
                r = rr['code']
                print(rr)
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({"code": 1}))
            mobj = App.objects.filter(app_id=int(app_ids))
            print(mobj)
            t = AppVersion.objects.filter(app_id_id=int(app_ids), version_code=app_version, version_name=app_version,
                                          upload_type=int(1))

            if t:
                return HttpResponse(json.dumps({"code": 2}))
            else:

                url_list = rr['data']
                AppVersion.objects.create(app_id=mobj[0], download_url=url_list, version_code=app_version,
                                          version_name=app_version, av_md5='1', create_date=datetime.datetime.utcnow(),
                                          update_date=datetime.datetime.utcnow(), remarks=appversion_remark)
                Message.objects.create(message_content='屏端固件已更新', message_type=int(5),
                                       message_handler_type=int(5),
                                       device_key=key, message_sender=cook_ies, message_target=cook_ies,
                                       create_date=datetime.datetime.utcnow(),
                                       update_date=datetime.datetime.utcnow())
                return HttpResponse(
                    json.dumps({"code": 0, "url": rr['data'], "filename": file.name, "version": app_version}))
        elif action == 'ui_upload_1':
            try:
                store = EbStore(CLOUD_TOKEN)
                rr = store.upload(file.read(), file.name, file.content_type)
                rr = json.loads(rr)
                r = rr['code']
                print(rr)
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({"code": 1}))
            mobj = App.objects.filter(app_id=int(app_ids))
            print(mobj)
            t = AppVersion.objects.filter(app_id_id=int(app_ids), version_code=app_version, version_name=app_version,
                                          upload_type=int(2))

            if t:
                return HttpResponse(json.dumps({"code": 2}))
            else:

                url_list = rr['data']
                AppVersion.objects.create(app_id=mobj[0], download_url=url_list, version_code=app_version,
                                          version_name=app_version, av_md5='1', create_date=datetime.datetime.utcnow(),
                                          update_date=datetime.datetime.utcnow(), remarks=appversion_remark,
                                          upload_type=int(2))
                Message.objects.create(message_content='屏端固件已更新', message_type=int(5),
                                       message_handler_type=int(5),
                                       device_key=key, message_sender=cook_ies, message_target=cook_ies,
                                       create_date=datetime.datetime.utcnow(),
                                       update_date=datetime.datetime.utcnow())
                return HttpResponse(
                    json.dumps({"code": 0, "url": rr['data'], "filename": file.name, "version": app_version}))
        elif action == 'firmware':
            files = request.FILES.get("files", '')
            print(file, files)
            try:
                # 处理上传的pkg文件
                store = EbStore(CLOUD_TOKEN)
                rr = store.upload(file.read(), file.name, file.content_type)
                rr = json.loads(rr)
                r = rr['code']
                print(rr)
                # 处理上传的图片
                stores = EbStore(CLOUD_TOKEN)
                rp = stores.upload(files.read(), files.name, files.content_type)
                rp = json.loads(rp)
                rpp = rp['code']
                print(rpp)
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({"code": 1}))
            sizes = request.POST.get('sizes', '')
            fobj = Firmware.objects.create(firmware_size=int(sizes), firmware_name=appversion_remark,
                                           firmware_image=rp['data'],
                                           firmware_version=app_version, firmware_url=rr['data'],
                                           firmware_create_date=datetime.datetime.utcnow(),
                                           firmware_update_date=datetime.datetime.utcnow())
            if fobj:
                return HttpResponse(json.dumps({"code": 0}))
            else:
                return HttpResponse(json.dumps({"code": 2}))
        else:
            t = int(id) + int(1)
            user1 = request.COOKIES['COOKIE_USER_ACCOUNT']
            b = UserGroup.objects.filter(group__create_user=user1)
            a = App.objects.filter(app_appid__endswith=key)
            email_list = []
            app_name = ''
            developer = ''
            group_id = ''
            for i in a:
                app_name = i.app_name
                group_id = i.group_id
                developer = i.developer_id
            try:
                b = UserGroup.objects.filter(group__group_id=group_id)
                for i in b:
                    email_list.append(i.user_account)
            except Exception as e:
                print(e)
            try:
                # 上传UI文件
                if post_data == 'upload':

                    try:
                        store = EbStore(CLOUD_TOKEN)
                        rr = store.upload(file.read(), file.name, file.content_type)
                        rr = json.loads(rr)
                        r = rr['code']
                        print(rr)
                    except Exception as e:
                        print(e)
                        return HttpResponse(json.dumps({"code": 1}))
                    list_url = rr['data']
                    datas = get_ui_static_conf(key, list_url, id, file.name, user1)
                    product_name = app_name + '上传更新提示'
                    # 需要修改
                    print('id', t)
                    if DocUi.objects.filter(ui_key=key, ui_upload_id=t):
                        next_stemp = [str(i.ui_plan) for i in
                                      DocUi.objects.filter(ui_key=key, ui_upload_id=t)][0]
                    else:
                        next_stemp = '该产品即将量化'
                    # 发送邮件通知send_product_process_email(title, product_name, process_name, next_process, handler, to_user, detail_url, action)
                    try:
                        send_product_process_email(product_name, app_name, file.name, next_stemp, user1, email_list,
                                                   location, "submit")
                        Message.objects.create(message_content=BOOK[id] + ':' + '已上传', message_type=int(4),
                                               message_handler_type=int(4),
                                               device_key=key, message_sender=cook_ies, message_target=cook_ies,
                                               create_date=datetime.datetime.utcnow(),
                                               update_date=datetime.datetime.utcnow())
                    except Exception as e:
                        print(e)
                    dd = ''
                    p = DocUi.objects.filter(ui_key=key, ui_upload_id=id)
                    for i in p:
                        dd = i.ui_content

                    return HttpResponse(json.dumps(datas))
                else:
                    r = 1
            except Exception as e:
                r = 1
                print(e)
        return HttpResponse(json.dumps({"code": 0}))


def wx_scan_code(request):
    def createRandomStr():
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(15))

    if request.method == 'GET':
        url = 'https://' + request.get_host() + request.get_full_path()
        r = requests.get(wx_ticket)
        ret = r.json()
        jsapiTicket = ret.get('jsapi_ticket', None)
        timestamp = int(time.time())
        # 获取（随机字符串）
        nonceStr = createRandomStr()
        ret = {
            'nonceStr': nonceStr,
            'jsapi_ticket': jsapiTicket,
            'timestamp': timestamp,
            'url': url
        }
        string1 = '&'.join(['%s=%s' % (key.lower(), ret[key]) for key in sorted(ret)])
        signature = hashlib.sha1(string1.encode('utf-8')).hexdigest()
        signPackage = {
            "appId": WECAHT_APPID,
            "nonceStr": nonceStr,
            "timestamp": timestamp,
            "url": url,
            "signature": signature,
            "rawString": string1
        }
        key = request.GET.get('key', None)
        device_id = request.GET.get('id', None)
        if key:
            query_app = App.objects.filter(app_appid__endswith=key)
            if query_app:
                app = query_app[0]
                return render(request, 'product/wexin.html', locals())
            else:
                return HttpResponse("该key不存在")
        elif device_id:
            return render(request, 'product/control.html', locals())
        else:
            return HttpResponse("网页错误")
    elif request.method == 'POST':
        device_id = request.POST.get("id", "")
        key = request.POST.get("key", "")
        url = DOWNLOAD_ZIP.format(key)
        code = requests.get(url).status_code
        if code == 404:
            url = ""
        TOKEN = "SvycTZu4hMo21A4Fo3KJ53NNwexy3fu8GNcS8J0kiqaQoi0XvgnvXvyv5UhW8nJj_551657047c2d5d0fd8a30e999b4f7b20f5ea568e"
        url1 = INSIDE_MESSAGE_PUSH.format(TOKEN)
        data = {
            "message": [
                {"TK_TYPE": "DownloadZip", "EB_TASK_PARAM": {"ZipUrl": url, "KEY": key}, "TK_PY_ID": device_id}],
            "touser": [device_id]
        }
        res = requests.post(url=url1, data=json.dumps(data))
        res = res.json()
        return HttpResponse(json.dumps(res))


def ui_conf_main(request, device_key):
    template = "UI/main.html"
    return render(request, template, locals())


def download(request):
    import requests
    url = request.GET.get("url", "")
    filename = request.GET.get("name", "")
    if url:
        r = requests.get(url)
        if not filename:
            filename = os.path.basename(url)
        response = HttpResponse(r.content,
                                content_type='APPLICATION/OCTET-STREAM')  # 设定文件头，这种设定可以让任意文件都能正确下载，而且已知文本文件不是本地打开
        response['Content-Disposition'] = 'attachment; filename=' + urlquote(filename)  # 设定传输给客户端的文件名称
        response['Content-Length'] = r.headers['content-length']  # 传输给客户端的文件大小
        return response
    else:
        return HttpResponse("no")
