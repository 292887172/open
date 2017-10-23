# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.http.response import HttpResponseRedirect
import requests

from django.contrib.auth.decorators import login_required

from base.util import gen_app_default_conf
from common.app_helper import create_app,update_app_fun_widget
from common.app_helper import del_app
from common.app_helper import release_app
from common.app_helper import cancel_release_app
from common.app_helper import off_app
from common.app_helper import update_app_info
from common.app_helper import update_app_config
from common.app_helper import reset_app_secret
from common.app_api_helper import ApiHandler
from base.const import StatusCode
from base.const import ConventionValue
from common.smart_helper import *
from common.message_helper import save_user_message
from conf.commonconf import CLOUD_TOKEN,KEY_URL
from ebcloudstore.client import EbStore
from common.util import parse_response, send_test_device_status
from model.center.app import App

import time
import json
import logging
import os
from conf.newuserconf import *
from conf.message import *
from util.export_excel import date_deal
from util.netutil import verify_push_url

_code = StatusCode()
_convention = ConventionValue()


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
        if len(app_names)<3:
            for i in range(len(APP_NAME)):
                if APP_NAME[i] not in app_names:
                    result = create_app(DEFAULT_USER, APP_NAME[i], APP_MODEL[i], APP_CATEGORY[i], DEVICE_TYPE[i],
                                    APP_COMMAND[i], DEVICE_CONF[i], APP_FACTORY_UID[i], 0, 3)
                    if result:
                        result.app_logo = APP_LOGO[i]
                        result.save()
        if not request.user.developer:
            return HttpResponseRedirect(reverse("center"))
        else:
            developer = request.user.developer
        keyword = request.GET.get("search", "")
        if keyword:
            user_apps = developer.developer_related_app.all().filter(app_name__contains=keyword)
        else:
            user_apps = developer.developer_related_app.all()
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
            default_apps=default_apps
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
                ret = del_app(app_id)
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
        if not request.user.developer.developer_id:
            return HttpResponseRedirect(reverse("center"))
        else:
            developer = request.user.developer
        factory_list = get_factory_list()
        template = "product/add.html"
        content = dict(
            developer=developer,
            factory_list=factory_list
        )
        return render(request, template, content)

    def post():
        developer_id = request.POST.get("developer_id", "")
        app_name = request.POST.get("product_name", "")
        app_category = request.POST.get("product_category", "")
        app_category_detail = request.POST.get("product_category_detail", 0)
        if app_category_detail:
            try:
                app_category_detail = int(app_category_detail)
            except ValueError:
                app_category_detail = 0
                pass
        factory_name = request.POST.get("brandName", "")
        app_factory_id = get_factory_id(factory_name)
        app_model = request.POST.get("product_model", "")
        app_command = request.POST.get("product_command", "")
        app_group = request.POST.get("product_group", "")
        device_conf = gen_app_default_conf(app_category_detail)
        if not developer_id:
            ret["code"] = 100001
            ret["msg"] = "missing developer_id"
            ret["message"] = "缺少开发者账号ID"
            return HttpResponse(json.dumps(ret, separators=(",", ':')))
        # 创建一个app
        try:
            if not developer_id or not app_name or not app_category or not app_command \
                    or not app_group:
                ret["code"] = 100002
                ret["msg"] = "invalid app_id"
                ret["message"] = "无效的APP_ID"
                return HttpResponse(json.dumps(ret, separators=(",", ':')))
            result = create_app(developer_id, app_name, app_model, app_category, app_category_detail, app_command,
                                device_conf, app_factory_id, app_group)
            if result.app_id:
                # 将产品key值推送到接口
                try:
                    app_key = result.app_appid
                    key = app_key[-8:]
                    requests.get(KEY_URL, params={'key': key}, timeout=5)
                except Exception as e:
                    print(e)
                    pass
                url = '/product/main/?ID=' + str(result.app_id) + '#/argue'
                return HttpResponseRedirect(url)
            else:
                ret["code"] = 100003
                ret["msg"] = "invalid app_id"
                ret["message"] = "无效的产品编号"
                return HttpResponse(json.dumps(ret, separators=(",", ':')))
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
        if not request.user.developer.developer_id:
            return HttpResponseRedirect(reverse("center"))
        else:
            developer = request.user.developer
        try:
            user_related_app = App.objects.filter(developer=developer)
            app_id = request.GET.get("ID", "")
            user_apps = App.objects.get(app_id=int(app_id))
            # user_apps = developer.developer_related_app.get(app_id=int(app_id))
        except Exception as e:
            print(e)
            return HttpResponseRedirect(reverse("home/guide"))
        if not user_apps:
            return HttpResponseRedirect(reverse("product/list"))

        developer_account = request.user.developer.developer_account
        app = user_apps
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

    def save_app(app, opera_data):
        # 保存修改后的device_config
        app.device_conf = json.dumps(opera_data)
        update_app_protocol(app)
        app.save()

    def post():
        # 根据ID获取到数据库中的设备配置信息
        app_id = request.GET.get("ID", "")
        app = App.objects.get(app_id=app_id)
        opera_data = []
        fun_name = ''
        message_content = ''
        try:
            if app.device_conf:
                opera_data = json.loads(app.device_conf)
                opera_data.sort(key=lambda x: int(x.get("id")))
        except Exception as e:
            logging.info("读取数据库中设备配置信息失败", e)
            print(e)
        # 接收页面请求信息
        post_data = request.POST.get("name")
        if post_data == 'list':
            # 显示所有列表信息
            return JsonResponse({'rows': opera_data, 'check_state': app.check_status})
        elif post_data == 'edit':
            # 返回编辑页面信息
            edit_id = request.POST.get("id", "")
            streamId = []
            for i in range(len(opera_data)):
                streamId.append(opera_data[i]['Stream_ID'])
                if str(opera_data[i]['id']) == edit_id:
                    edit_data = opera_data[i]
                    return JsonResponse({'data': edit_data})
            return JsonResponse({'streamIds': streamId})
        elif post_data == 'del':
            # 删除信息
            del_id = request.POST.get("id")
            for i in range(len(opera_data)):
                if str(opera_data[i].get("id")) == del_id:
                    fun_name = opera_data[i]["name"]
                    opera_data.pop(i)
                    break
            save_app(app, opera_data)
            message_content = '"' + app.app_name + '"' + fun_name + DEL_FUN
            save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id)
            return HttpResponse('del_success')
        elif post_data == 'state':
            # 更改参数状态
            state_id = request.POST.get("id")
            for i in opera_data:
                if str(i['id']) == state_id:
                    fun_name = i['name']
                    if str(i['state']) == '0':
                        i['state'] = '1'
                        message_content = '"' + app.app_name + '"' + fun_name + UPDATE_FUN_OPEN
                    elif str(i['state']) == '1':
                        i['state'] = '0'
                        message_content = '"' + app.app_name + '"' + fun_name + UPDATE_FUN_CLOSE
                    save_app(app, opera_data)
                    save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id)
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
            fun_name = indata['name']
            if indata["id"]:
                # 编辑参数信息
                for i in opera_data:
                    if str(i['id']) == indata['id']:
                        i.update(indata)
                        break
                message_content = '"' + app.app_name + '"' + fun_name + UPDATE_FUN
                tt = "modify_success"
            else:
                # 添加一条参数信息首先获取当前最大id
                if opera_data:
                    indata['id'] = str(int(opera_data[-1]['id'])+1)
                else:
                    indata['id'] = '1'
                opera_data.append(indata)
                message_content = '"' + app.app_name + '"' + fun_name + CREATE_FUN
                tt = "add_success"
            save_app(app, opera_data)
            save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id)
            return HttpResponse(tt)

        # 获取设备列表
        device_table = request.POST.get("device", "")
        if device_table == 'device_table':
            key = app.app_appid
            key = key[-8:]
            device_list = get_device_list(app.app_appid)
            return JsonResponse({'data': device_list, 'key': key})
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

            url_add = 'http://'+http_host+'/static/file/'+key+'.zip'
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
