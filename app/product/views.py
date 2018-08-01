# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from base.util import gen_app_default_conf, get_app_default_logo
from common.account_helper import add_team_email, del_team_email
from common.app_helper import create_app, update_app_fun_widget, replace_fun_id, add_fun_id, add_mod_funs, get_mod_funs
from common.app_helper import del_app, save_app, check_cloud
from common.app_helper import release_app
from common.app_helper import cancel_release_app
from common.app_helper import off_app
from common.app_helper import update_app_info
from common.app_helper import update_app_config
from common.app_helper import reset_app_secret

from common.device_online import device_online
from base.const import StatusCode, DefaultProtocol,DefaultSchedule
from base.const import ConventionValue
from common.smart_helper import *
from common.message_helper import save_user_message
from common.device_fun_helper import add_device_fun
from conf.commonconf import CLOUD_TOKEN
from ebcloudstore.client import EbStore
from common.util import parse_response, send_test_device_status
from model.center.app import App

from model.center.protocol import Protocol
from model.center.doc_ui import DocUi

from model.center.app_version import AppVersion
from model.center.group import Group
from model.center.user_group import UserGroup
from base.connection import Redis3
from common.mysql_helper import get_ui_static_conf, remove_up_url
from util.email.send_email_code import send_product_process_email

import hashlib
import time
import json
import logging
import os
import requests
import random
import string
from conf.newuserconf import *
from conf.wxconf import *
from conf.apiconf import *
from conf.message import *
from model.center.user_group import UserGroup
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
                "is_share": 0

            }
            tmp_apps.append(tmp)

        for i in u:
            relate_app = App.objects.filter(group_id=i.group.group_id)
            for j in relate_app:
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
                    "is_share": 1

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
                r = Redis3(rdb=6).client
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
                "is_share": 0

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
                    "is_share": 1
                }
                tmp_apps.append(tmp)
        tmp_apps = sorted(tmp_apps, key=lambda a: a['app_update_date'], reverse=True)
        unpublished_apps = tmp_apps[:5]
        template = "product/controldown.html"
        content = dict(
            keyword=keyword,
            developer=developer,
            unpublished_apps=unpublished_apps,
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
                r = Redis3(rdb=6).client
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
        app_category_detail = request.POST.get("product_category_detail", 0)
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

        device_conf = gen_app_default_conf(app_category_detail)

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

            app_id = create_app(developer_id, app_name, app_model, app_category, app_category_detail, app_command,
                                device_conf, app_factory_id, app_group, app_logo, app_product_fast, 0,
                                app_category_detail2)
            from common.celerytask import add
            add.delay(app_id)

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

    def post():
        # data_protocol = json.loads(request.body.decode('utf-8')).get('key','')
        # data_protocol_list = json.loads(request.body.decode('utf-8'))
        app_id = request.GET.get("ID", "")
        cook_ies = request.COOKIES['COOKIE_USER_ACCOUNT']
        import os
        import os.path
        post_data = request.POST.get("name")

        id = request.POST.get("id")
        r = Redis3(rdb=6).client
        standa = request.POST.get("is_standa", None)  # 标准、自定义
        # 根据ID获取到数据库中的设备配置信息
        app = App.objects.get(app_id=app_id)
        device_conf = gen_app_default_conf(app.app_device_type)
        opera_data = []
        try:
            if app.device_conf:
                opera_data = json.loads(app.device_conf)
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
            res_status = r.exists("product_funs" + app_id)
            if res_status:
                data = r.get("product_funs" + app_id)
                data = json.loads(data.decode())
                opera_data = data["rows"]
            for line in opera_data:
                # if str(line.get("standa_or_define")) == str(standa):
                temp.append(line)
            data = {'rows': opera_data, 'check_state': app.check_status}
            r.set("product_funs" + app_id, json.dumps(data), 3600 * 24 * 3)
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
                message_content = '"' + app.app_name + '"' + funs + CREATE_FUN
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
            data = find(id, opera_data)

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
                replace_fun_id(opera_data, id, is_standa)
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
            save_app(app, opera_data, cook_ies)
            update_app_protocol(app)
            return HttpResponse(tt)

        # 获取设备列表
        if post_data == 'device_table':
            r5 = Redis3(rdb=5).client
            key = app.app_appid
            key = key[-8:]
            device_content = DEVICE + "_" + key
            if r5.exists(device_content):
                device_list = r5.get(device_content)
                device_list = json.loads(device_list.decode())
            else:
                device_list = get_device_list(app.app_appid)
                r5.set(device_content, json.dumps(device_list), 2 * 60)
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
                if ret:
                    update_app_protocol(app)
                res["data"] = ret
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
        if action == 'get_data_content':
            app = App.objects.get(app_appid__endswith=device_key)
            dc = json.loads(app.device_conf)
            data = []
            for i in dc:
                tmp = {'id': i['id'], 'title': i['name'], 'length': i['mxsLength']}
                data.append(tmp)
            return HttpResponse(json.dumps(data))
        try:
            if zdy == "0" or zdy == "1":

                mlist = Protocol.objects.all().filter(protocol_device_key=device_key, protocol_factory_type=zdy)

                if len(mlist) == 0:
                    p = DefaultProtocol().DEFAULT_DATA_ZDY
                    data = {"code": 2, "data": p, "protocol_type": zdy}
                    return HttpResponse(json.dumps(data))
                else:
                    print('xxxxx')
                    for iii in mlist:
                        res_list_data = iii.protocol_factory_content
                        protocol_type1 = iii.protocol_factory_type
                        res_list_data1 = json.loads(res_list_data)
                        res_list_data1['protocol_type'] = protocol_type1
                        data = {"code": 1, "data": res_list_data1, "protocol_type": zdy}
                        return HttpResponse(json.dumps(data))
        except Exception as e:
            print(e)
            logging.getLogger('').info("传入的参数zdy出错", str(e))
            data = {"code": 3, "data": DefaultProtocol().DEFAULT_DATA_ZDY, "protocol_type": 0}
            return HttpResponse(json.dumps(data))
        r = select_protocol(device_key, zdy)

        if r is None:
            rr = DefaultProtocol().DEFAULT_DATA
            print('eee')
            data = {"code": 2, "data": rr, "protocol_type": 0}
        else:
            data = {"code": 1, "data": r, "protocol_type": 0}
        return HttpResponse(json.dumps(data))
    if request.method == "POST":
        r = DefaultProtocol().DEFAULT_DATA_ZDY

        data_protocol_list = json.loads(request.body.decode('utf-8'))
        cook_ies = request.COOKIES['COOKIE_USER_ACCOUNT']

        try:
            if data_protocol_list.get('action', '') == 'update_protocol':
                data_sql = {}
                protocol_type = data_protocol_list.get('protocol_type', 0)
                list_fivechoose = data_protocol_list.get('fivechoose', '')
                list_t = data_protocol_list.get('frame_content', '')
                list_key = data_protocol_list.get('key', '')
                data_sql['is_single_instruction'] = list_fivechoose[0]
                data_sql['support_response_frame'] = list_fivechoose[1]
                data_sql['support_serial'] = list_fivechoose[2]
                data_sql['active_heartbeat'] = list_fivechoose[3]
                data_sql['support_repeat'] = list_fivechoose[4]
                data_sql['heart_rate'] = data_protocol_list.get('heart_rate')
                data_sql['repeat_rate'] = data_protocol_list.get('repeat_rate')
                data_sql['repeat_count'] = data_protocol_list.get('repeat_count')
                data_sql['endian_type'] = data_protocol_list.get('endian_type')
                print("data_sql", data_protocol_list.get('endian_type'))
                data_sql['frame_content'] = list_t
                data_sql['checkout_algorithm'] = data_protocol_list.get('checkout_algorithm')
                data_sql['start_check_number'] = data_protocol_list.get('start_check_number')
                data_sql['end_check_number'] = data_protocol_list.get('end_check_number')
                print("data_sql", data_sql)
                data_sql_update = json.dumps(data_sql, ensure_ascii=False)

                types = data_protocol_list.get('typesss', '')

                if types == "change":
                    ## 上下行  切换
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
            timess = Message.objects.filter(device_key=zy).order_by("-update_date")[0:3]
            for i in timess:
                i.update_date = i.update_date + datetime.timedelta(hours=8)
                tis = i.update_date.strftime("%Y-%m-%d %H:%I:%S")
                times.append({"time": tis, "message": i.message_content})
                print(times)

        return HttpResponse(json.dumps(times))
    elif request.method == 'POST':
        action = request.POST.get("action", "")
        app_id = request.POST.get("app_id", "")
        email = request.POST.get("email", "")
        user_account = request.user

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
    ids = request.GET.get('id', '')
    m = AppVersion.objects.filter(app_ids=ids)
    if m:
        app_list=[]
        for i in m:
            app_dict={}
            app_dict['url'] = eval(i.download_url)
            print(eval(i.download_url),type(eval(i.download_url)))
            app_dict['version'] = i.version_name
            app_list.append(app_dict)
    return HttpResponse(json.dumps(app_list))
@csrf_exempt
def schedule(request):
    if request.method == "GET":
        key = request.GET.get('key', '')
        print(key)
        update_list = []
        try:
            li_ui = DocUi.objects.filter(ui_key=key)
            if li_ui:
                id_list=[]
                for i in li_ui:
                    update_dict = {}
                    update_dict['id'] = i.ui_upload_id
                    update_dict['remark'] = i.ui_remark
                    update_dict['party'] = i.ui_party
                    update_dict['plan'] = i.ui_plan
                    id_list.append(i.ui_upload_id)
                    try:
                        url = eval(i.ui_content)
                    except Exception as e:
                        url = [i.ui_content]
                    if not isinstance(url, list):
                        url = [url]
                    update_dict['url'] = url
                    update_dict['ack'] = i.ui_ack
                    update_dict['time_stemp'] = i.ui_time_stemp

                    update_list.append(update_dict)
                    c_data = update_list[:len(update_list)]
                    c_data.sort(key=lambda x: int(x.get("id")))
                    c_data.extend(update_list[len(update_list):])
                    update_list = c_data
            else:
                update_list = DefaultSchedule().DEFAULT_SCHEDULE
                for i in update_list:
                    DocUi.objects.create(ui_key=key,ui_ack=0,ui_upload_id=i['id'],ui_plan=i['plan'],ui_party='',ui_remark='',ui_time_stemp='',
                                         ui_content="['']",ui_type='')
        except Exception as e:
            print(e)
        return HttpResponse(json.dumps(update_list))
    if request.method == "POST":
        key = request.POST.get('key', '')
        num = request.POST.get('num', '')
        location = request.POST.get('location', '')
        # data:{"key":keysss,"del":"del","del_id":b,"del_url":del_url}
        action = request.POST.get('action', '')
        if action == 'del':
            # 删除下载链接
            del_id = request.POST.get('del_id', '')
            del_url = request.POST.get('del_url', '')
            try:
                if del_id:
                    del_id = int(del_id)
                remove_up_url(key, del_id, del_url)
                return HttpResponse(json.dumps({"code": 0}))
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({"code": 1}))
        elif action == 'delxu':
            #data: {"key": keysss, "action": "delxu", "del_id": id}
            del_xu_id = request.POST.get('del_id','')
            # 删除原有的id对应的数据 大于id的数据id自减1更新
            try:
                DocUi.objects.filter(ui_key=key, ui_upload_id=del_xu_id).delete()
                del_data = DocUi.objects.filter(ui_key=key,ui_upload_id__gt=del_xu_id)
                if del_data:
                    for i in del_data:
                        if int(i.ui_upload_id) > int(del_xu_id):
                             DocUi.objects.filter(ui_key=key,ui_upload_id=i.ui_upload_id).update(ui_upload_id=int(i.ui_upload_id) - 1)
                return HttpResponse(json.dumps({"code": 0}))
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({"code": 1}))
        elif action == 'remark':
            # 备注信息
            remark_value = request.POST.get('value', '')
            remark_id = request.POST.get('id', '')
            try:
                ddd = DocUi.objects.filter(ui_key=key, ui_upload_id=remark_id)
                # 判断是否存在当前计划书id的数据
                if ddd:
                    ddd.update(ui_remark=remark_value)
                else:
                    uw = ['']
                    DocUi.objects.create(ui_time_stemp='', ui_party='', ui_remark=remark_value, ui_upload_id=remark_id,
                                         ui_key=key, ui_content=uw, ui_type='UI', ui_title='1.0',
                                         create_date=datetime.datetime.utcnow(), update_date=datetime.datetime.utcnow())
                return HttpResponse(json.dumps({"code": 0}))
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({"code": 1}))
        elif action == 'party':
            # 负责方
            party_value = request.POST.get('value', '')
            party_id = request.POST.get('id', '')
            try:
                ddd = DocUi.objects.filter(ui_key=key, ui_upload_id=party_id)
                if ddd:
                    ddd.update(ui_party=party_value)
                else:
                    uw = ['']
                    DocUi.objects.create(ui_time_stemp='', ui_party=party_value, ui_remark='', ui_upload_id=party_id,
                                         ui_key=key, ui_content=uw, ui_type='UI', ui_title='1.0',
                                         create_date=datetime.datetime.utcnow(), update_date=datetime.datetime.utcnow())
                return HttpResponse(json.dumps({"code": 0}))
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({"code": 1}))
        elif action == 'time_strmp':
            # 时间搓
            time_value = request.POST.get('value', '')
            time_id = request.POST.get('id', '')
            ddd = DocUi.objects.filter(ui_key=key, ui_upload_id=time_id)
            try:
                if ddd:
                    print(time_id,time_value)
                    ddd.update(ui_time_stemp=time_value)
                else:
                    uw = ['']
                    DocUi.objects.create(ui_time_stemp=time_value, ui_party='', ui_remark='', ui_upload_id=time_id,
                                         ui_key=key, ui_content=uw, ui_type='UI', ui_title='1.0',
                                         create_date=datetime.datetime.utcnow(), update_date=datetime.datetime.utcnow())
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
                    DocUi.objects.create(ui_plan=time_value, ui_party='',ui_time_stemp='', ui_remark='', ui_upload_id=time_id,
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
                print('组id', i.group_id)
                group_id = i.group_id
            ack_name = app_name + '第' + num + '步操作确认通知'
            try:
                b = UserGroup.objects.filter(group__group_id=group_id)
                for i in b:
                    print(i.user_account)
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
        ui_info = request.POST.get('ui_info', '')
        ui_time_stemp = request.POST.get('ui_time_stemp', '')
        location = request.POST.get('location', '')
        # action 判断
        action = request.POST.get('action','')
        app_ids = request.POST.get('app_id','')
        app_version = request.POST.get('app_version','')

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
            print(app_ids)
            mobj = App.objects.filter(app_id=int(app_ids))
            print(mobj)
            t = AppVersion.objects.filter(app_ids_id=int(app_ids),version_code=app_version,version_name=app_version)
            for i in t:
                print(i.app_ids)
                print(i.app_ids_id)

            if t:
                return HttpResponse(json.dumps({"code": 2}))
            else:

                url_list = [{"url": rr['data'], "filename": file.name}]
                AppVersion.objects.create(app_ids=mobj[0], download_url=url_list, version_code=app_version,version_name=app_version,av_md5='1')
                return HttpResponse(json.dumps({"code": 0,"url": rr['data'], "filename": file.name,"version":app_version}))

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
                    get_ui_static_conf(key, post_data, list_url, cook_ies, id, ui_info, ui_time_stemp,file.name)
                    product_name = app_name + '上传更新提示'
                    if t >= 9:
                        next_stemp = "量产阶段"
                    else:
                        next_stemp = BOOK[str(t)]
                    # 发送邮件通知send_product_process_email(title, product_name, process_name, next_process, handler, to_user, detail_url, action)
                    try:
                        send_product_process_email(product_name, app_name, BOOK[id], next_stemp, user1, email_list,
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

                    return HttpResponse(json.dumps({"url": dd, "code": 0}))
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
