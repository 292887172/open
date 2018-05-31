# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from base.util import gen_app_default_conf, get_app_default_logo
from common.app_helper import create_app, update_app_fun_widget, replace_fun_id, add_fun_id, add_mod_funs, get_mod_funs
from common.app_helper import del_app, save_app, check_cloud
from common.app_helper import release_app
from common.app_helper import cancel_release_app
from common.app_helper import off_app
from common.app_helper import update_app_info
from common.app_helper import update_app_config
from common.app_helper import reset_app_secret
from common.app_api_helper import ApiHandler
from common.app_api_helper import remove_conf_prefix
from common.device_online import device_online
from base.const import StatusCode
from base.const import ConventionValue
from common.smart_helper import *
from common.message_helper import save_user_message
from common.device_fun_helper import add_device_fun
from conf.commonconf import CLOUD_TOKEN,KEY_URL
from ebcloudstore.client import EbStore
from common.util import parse_response, send_test_device_status
from model.center.app import App
from base.connection import Redis3

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
from util.export_excel import date_deal
from util.netutil import verify_push_url

_code = StatusCode()
_convention = ConventionValue()


@csrf_exempt
def product_kitchen(request):
    default_apps = App.objects.filter(developer=DEFAULT_USER).filter(check_status=_convention.APP_DEFAULT)
    return render(request, "product/kitchen.html", locals())

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
        if len(app_names) < 3:
            for i in range(len(APP_NAME)):
                if APP_NAME[i] not in app_names:
                    result = create_app(DEFAULT_USER, APP_NAME[i], APP_MODEL[i], APP_CATEGORY[i], DEVICE_TYPE[i],
                                    APP_COMMAND[i], DEVICE_CONF[i], APP_FACTORY_UID[i], 0, 3)
                    if result:
                        result.app_logo = APP_LOGO[i]
                        result.save()
        try:
            if request.user.developer:
                developer = request.user.developer
            else:
                developer = ''
            keyword = request.GET.get("search", "")
            if keyword:
                user_apps = developer.developer_related_app.all().filter(app_name__contains=keyword).order_by("-app_create_date")
            else:
                user_apps = developer.developer_related_app.all().order_by("-app_create_date")
        except Exception as e:
            user_apps=[]
            developer = ''
            keyword = ''
            print(e)
        # 已经发布, 未发布, 正在请求发布，未通过审核,默认状态
        published_apps = []
        unpublished_apps = []
        publishing_apps = []
        failed_apps = []
        default_apps = App.objects.filter(developer=DEFAULT_USER).filter(check_status=_convention.APP_DEFAULT)
        for app in user_apps:
            # 已经发布
            if app.check_status == _convention.APP_CHECKED:
                published_apps.append(app)
            elif app.check_status == _convention.APP_CHECKING:
                publishing_apps.append(app)
            # 未发布
            elif app.check_status == _convention.APP_UN_CHECK:
                unpublished_apps.append(app)
            # 未通过审核
            elif app.check_status == _convention.APP_CHECK_FAILED:
                failed_apps.append(app)
        template = "product/list.html"
        content = dict(
            keyword=keyword,
            developer=developer,
            published_apps=published_apps,
            publishing_apps=publishing_apps,
            unpublished_apps=unpublished_apps,
            failed_apps=failed_apps,
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
                r.delete("product_funs"+app_id)
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
        factory_list = get_factory_list()
        template = "product/add.html"
        default_apps = App.objects.filter(developer=DEFAULT_USER).filter(check_status=_convention.APP_DEFAULT)
        content = dict(
            developer=developer,
            factory_list=factory_list,
            default_apps=default_apps
        )
        return render(request, template,content)

    def post():
        developer_id = request.POST.get("developer_id", "")
        app_name = request.POST.get("product_name", "")
        app_category = request.POST.get("product_category", "")
        app_category_detail = request.POST.get("product_category_detail", 0)
        if app_category_detail:
            try:
                app_category_detail = int(app_category_detail)
            except Exception as e:
                app_category_detail = 0
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
            if not developer_id or not app_name or not app_category or not app_command \
                    or not app_group:
                ret["code"] = 100002
                ret["msg"] = "invalid app_id"
                ret["message"] = "无效的APP_ID"
                return HttpResponse(json.dumps(ret, separators=(",", ':')))
            app_id = create_app(developer_id, app_name, app_model, app_category, app_category_detail, app_command,
                        device_conf, app_factory_id, app_group, app_logo)
            from common.celerytask import add
            r = Redis3(rdb=6).client
            add.delay(app_id)
            app = App.objects.get(app_id=app_id)
            update_app_protocol(app)
            url = '/product/main/?ID=' + str(app_id) + '#/argue'
            return HttpResponseRedirect(url)
        except Exception as e:
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
        if res:
            return HttpResponse(res)
        if not request.user.developer:
            developer = ''
        else:
            developer = request.user.developer
        try:
            user_related_app = App.objects.filter(developer=developer)
            app_id = request.GET.get("ID", "")
            user_apps = App.objects.filter(developer=developer,app_id=int(app_id))
            if not user_apps:
                user_apps = App.objects.filter(developer=DEFAULT_USER,app_id=int(app_id))
        except Exception as e:
            print(e)
            logging.getLogger('').info("应用出错", str(e))
            return HttpResponseRedirect(reverse("product/list"))
        if not user_apps:
            return HttpResponseRedirect(reverse("product/list"))

        app = user_apps[0]
        all_app = user_related_app
        default_apps = App.objects.filter(developer=DEFAULT_USER).filter(check_status=_convention.APP_DEFAULT)
        device_name = get_device_type(app.app_device_type)

        # 获取这个app的API接口列表
        api_handler = ApiHandler(app.app_level, app.app_group)
        api_list = api_handler.api_list
        band_name = get_factory_name(app.app_factory_uid)
        app_key = app.app_appid
        key = app_key[-8:]
        template = "product/main.html"
        default_apps = App.objects.filter(developer=DEFAULT_USER).filter(check_status=_convention.APP_DEFAULT)
        content = dict(
            all_app=all_app,
            app=app,
            api_list=api_list,
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
        app_id = request.GET.get("ID", "")
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
                if str(line.get("standa_or_define")) == str(standa):
                    temp.append(line)
            data = {'rows': opera_data, 'check_state': app.check_status}
            r.set("product_funs" + app_id, json.dumps(data), 3600 * 24 * 3)
            data["rows"] = temp[(page-1)*rows:page*rows]
            data["total"] = len(temp)//rows + 1
            data["records"] = len(temp)
            return JsonResponse(data)
        elif post_data in ['show_mod', "add_mod"]:
            # 显示默认模板的功能  添加模板功能
            if post_data == "show_mod":
                mod = get_mod_funs(opera_data, device_conf)
                return JsonResponse({"data": mod})
            elif post_data == "add_mod":
                funs = request.POST.get("funs")
                add_mod_funs(opera_data, device_conf, funs)
                save_app(app, opera_data)
                update_app_protocol(app)
                return HttpResponse('add_mod_success')
        elif post_data == 'edit':
            # 返回编辑页面信息
            edit_data = find(id, opera_data)
            mods_name = list(map(lambda x: x["Stream_ID"], device_conf))
            mods_name1 = list(map(lambda x: x["Stream_ID"], opera_data))
            mods_name.extend(mods_name1)
            mods_name = list(set(mods_name))
            if edit_data:
                edit_data = edit_data[1]
                mods_name.remove(edit_data["Stream_ID"])
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
                save_app(app, opera_data)
                update_app_protocol(app)
                message_content = '"' + app.app_name + '"' + fun_name + DEL_FUN
                save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id)
                return HttpResponse('del_success')
        elif post_data == 'update':
            funs = request.POST.get("funs")
            funs = json.loads(funs)
            for i in range(len(opera_data)):
                for j in range(len(funs)):
                    if str(opera_data[i].get("Stream_ID")) == funs[j]:
                        opera_data[i]["id"] = j + 1
            c_data = opera_data[:len(funs)]
            c_data.sort(key=lambda x: int(x.get("id")))
            c_data.extend(opera_data[len(funs):])
            save_app(app, c_data)
            update_app_protocol(app)
            return HttpResponse('update_success')
        elif post_data == 'toSwitch':
            for switch in opera_data:
                if int(switch["id"]) == int(id):
                    switch["toSwitch"] = 1
                else:
                    switch["toSwitch"] = 0
            save_app(app, opera_data)
            update_app_protocol(app)
            return HttpResponse('select_success')
        elif post_data in ['isShow', 'isControl', 'isDisplay', "isCloudMenu"]:
            val = request.POST.get("dd")
            data = find(id, opera_data)
            if data:
                data[1][post_data] = val
                if post_data == "isCloudMenu":
                    app.app_is_cloudmenu_device = check_cloud(opera_data)
                save_app(app, opera_data)
                update_app_protocol(app)
                return HttpResponse('change_success')
        elif post_data == "export":
            res = date_deal(app_id)
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
                save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id)
            else:
                # 添加一条参数信息需要申请审核
                indata = add_fun_id(opera_data, indata)
                add_device_fun(app.app_appid, indata)
                opera_data.append(indata)
                opera_data.sort(key=lambda x: int(x.get("id")))
                # message_content = '"' + app.app_name + '"' + fun_name + CREATE_FUN
                tt = "add_success"
            save_app(app, opera_data)
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
                r5.set(device_content, json.dumps(device_list), 2*60)
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
        else:
            res["code"] = 10002
        return HttpResponse(json.dumps(res, separators=(",", ":")))

    if request.method == "GET":
        return get()

    elif request.method == "POST":
        return post()


@csrf_exempt
def key_verify(request):
    # 验证key
    if request.method == 'POST':
        key = request.POST.get("key", "")
        if not key:
            return JsonResponse(parse_response(code=_code.MISSING_APP_KEY_CODE, msg=_code.MISSING_APP_KEY_MSG))
        app = App.objects.filter(app_appid__endswith=key)
        flag = os.path.exists('static/file/'+key+'.zip')
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


@csrf_exempt
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
            query_app = App.objects.filter(app_appid__endswith = key)
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
            "message": [{"TK_TYPE": "DownloadZip", "EB_TASK_PARAM": {"ZipUrl": url, "KEY": key}, "TK_PY_ID": device_id}],
            "touser": [device_id]
        }
        res = requests.post(url=url1, data=json.dumps(data))
        res = res.json()
        return HttpResponse(json.dumps(res))


def ui_conf_main(request, device_key):
    template = "UI/main.html"
    return render(request, template, locals())
