# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from common.app_helper import create_app
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
from common.smart_helper import get_factory_list
from model.center.app import App

import time
import json
import logging

from util.export_excel import date_deal
from util.netutil import verify_push_url

_code = StatusCode()
_convention = ConventionValue()


@login_required
def product_list(request):
    """
    应用列表
    :param request:
    :return:
    """
    def get():
        if not request.user.is_developer:
            return HttpResponseRedirect(reverse("center"))
        else:
            developer = request.user.developer
        keyword = request.GET.get("search", "")
        if keyword:
            user_apps = developer.developer_related_app.all().filter(app_name__contains=keyword)
        else:
            user_apps = developer.developer_related_app.all()
        # 已经发布, 未发布, 未通过审核
        published_apps = []
        unpublished_apps = []
        publishing_apps = []
        failed_apps = []
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
            published_apps=published_apps,
            publishing_apps=publishing_apps,
            unpublished_apps=unpublished_apps,
            failed_apps=failed_apps
        )
        return render(request, template, content)

    def post():
        res = dict(
            code=10000
        )
        app_id = request.POST.get("app_id", "")
        action = request.POST.get("action", "")
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
        if not request.user.is_developer:
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
        app_category_detail = request.POST.get("product_category_detail", "")
        app_factory_id = request.POST.get("brand_id", "")
        app_model = request.POST.get("product_model", "")
        app_command = request.POST.get("product_command")
        device_conf = ''
        if not developer_id:
            ret["code"] = 100001
            ret["msg"] = "missing developer_id"
            ret["message"] = "缺少开发者账号ID"
            return HttpResponse(json.dumps(ret, separators=(",", ':')))
        # 创建一个app
        try:
            if not developer_id or not app_name or not app_category or not app_category_detail or not app_command:
                ret["code"] = 100002
                ret["msg"] = "invalid app_id"
                ret["message"] = "无效的APP_ID"
                return HttpResponse(json.dumps(ret, separators=(",", ':')))
            app_name = create_app(developer_id, app_name, app_model, app_category, app_category_detail, app_command,
                                  device_conf, app_factory_id)
            if app_name:
                return HttpResponseRedirect(reverse("product/list"))
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
        if not request.user.is_developer:
            return HttpResponseRedirect(reverse("center"))
        else:
            developer = request.user.developer
        try:
            app_id = request.GET.get("ID", "")
            user_apps = developer.developer_related_app.get(app_id=int(app_id))
        except Exception as e:
            del e
            return HttpResponseRedirect(reverse("center"))
        if not user_apps:
            return HttpResponseRedirect(reverse("product/list"))

        app = user_apps
        # 获取这个app的API接口列表
        api_handler = ApiHandler(app.app_level, app.app_group)
        api_list = api_handler.api_list

        template = "product/main.html"
        content = dict(
            app=app,
            api_list=api_list
        )
        return render(request, template, locals())

    def save_app(app, opera_data):
        # 保存修改后的device_config
        app.device_conf = json.dumps(opera_data)
        app.save()

    def post():
        # 根据ID获取到数据库中的设备配置信息
        app_id = request.GET.get("ID", "")
        app = App.objects.get(app_id=app_id)
        opera_data = json.loads(app.device_conf)
        opera_data.sort(key = lambda x: int(x.get("id")))
        # 接收页面请求信息
        post_data = request.POST.get("name")
        if post_data == 'list':
            # 显示所有列表信息
            return JsonResponse({'rows': opera_data, 'check_state':app.check_status})
        elif post_data == 'edit':
            # 返回编辑页面信息
            edit_id = request.POST.get("id")
            for i in range(len(opera_data)):
                if opera_data[i].get("id", "不存在id") == edit_id:
                    return JsonResponse({'data': opera_data[i]})
        elif post_data == 'del':
            # 删除信息
            del_id = request.POST.get("id")
            for i in range(len(opera_data)):
                if opera_data[i].get("id", "不存在id") == del_id:
                    opera_data.pop(i)
                    break
            save_app(app, opera_data)
            return HttpResponse(json.dumps('del', separators=(",", ":")))
        elif post_data == 'state':
            # 更改参数状态
            state_id = request.POST.get("id")
            for i in opera_data:
                if i['id'] == state_id:
                    if str(i['state']) == '0':
                        i['state'] = '1'
                    elif str(i['state']) == '1':
                        i['state'] = '0'
                    break
            save_app(app, opera_data)
            return HttpResponse(json.dumps('state', separators=(",", ":")))
        elif post_data == "export":
            res = date_deal(app_id)
            return res
        elif post_data == 'save':
            # 接收要编辑或者添加的数据
            indata = request.POST.get('d')
            indata = json.loads(indata)
            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            indata["time"] = dt
            if indata["id"]:
                # 编辑参数信息
                for i in opera_data:
                    indata['id'] = int(indata['id'])
                    if int(i['id']) == indata['id']:
                        i.update(indata)
                        break
                tt = 0
            else:
                # 添加一条参数信息首先获取当前最大id
                indata['id'] = int(opera_data[-1]['id'])+1
                opera_data.append(indata)
                tt = 1
            save_app(app, opera_data)
            return HttpResponse(json.dumps(tt, separators=(",", ":")))

        #  app操作
        res = dict(
            code=10000
        )
        action = request.POST.get("action", "")
        app_id = request.POST.get("app_id", "")
        app_name = request.POST.get("app_name", "")
        app_category = request.POST.get("app_category", "")
        app_model = request.POST.get("app_model", "")
        app_describe = request.POST.get("app_describe", "")
        app_site = request.POST.get("app_site", "")
        app_logo = request.POST.get("app_logo", "")
        app_push_url = request.POST.get("app_config_push_url", "")
        app_push_token = request.POST.get("app_config_push_token", "")
        app_command = request.POST.get("app_command", "")
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
                ret = update_app_info(app_id, app_name, app_category, app_model, app_describe, app_site, app_logo,
                                      app_command)
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
def export(request):
    # 导出配置文件
    if request.method == 'POST':
        pass
