# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt

from model.center.app import App

from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http.response import HttpResponse,JsonResponse
from django.http.response import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.db import models

import time

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

import json
import logging
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

        template = "product/add.html"
        content = dict(
            developer=developer
        )
        return render(request, template, content)

    def post():
        developer_id = request.POST.get("developer_id", "")
        app_name = request.POST.get("product_name", "")
        app_category = request.POST.get("product_category", "")
        app_category_detail = request.POST.get("product_category_detail", "")
        app_model = request.POST.get("product_model", "")
        if not developer_id:
            ret["code"] = 100001
            ret["msg"] = "missing developer_id"
            ret["message"] = "缺少开发者账号ID"
            return HttpResponse(json.dumps(ret, separators=(",", ':')))
        # 创建一个app
        try:
            if not developer_id or not app_name or not app_category or not app_category_detail:
                ret["code"] = 100002
                ret["msg"] = "invalid app_id"
                ret["message"] = "无效的APP_ID"
                return HttpResponse(json.dumps(ret, separators=(",", ':')))
            print('开始注册',time.time())
            app_name = create_app(developer_id, app_name, app_model, app_category, app_category_detail)
            print('结束注册', time.time())
            if app_name:
                return HttpResponseRedirect(reverse("product/list"))
            else:
                ret["code"] = 100002
                ret["msg"] = "invalid app_id"
                ret["message"] = "无效的产品编号"
                return HttpResponse(json.dumps(ret, separators=(",", ':')))
        except Exception as e:
            logging.getLogger("root").error(e)
            logging.getLogger("root").error("创建应用失败")
            return HttpResponse("")

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
    def save_app(app,opera_data,data):
        app.device_conf=json.dumps(opera_data)
        app.save()
        return JsonResponse({'data': data})
    def post():
        app_id = request.GET.get("ID", "")
        app=App.objects.get(app_id=app_id)
        opera_data=json.loads(app.device_conf)
        # 获取到数据库中的设备配置信息
        post_data=request.POST.get("name")
         # 接收页面传送信息
        if post_data=='list':
            return JsonResponse({'rows': opera_data})
        elif post_data=='edit':
            edit_id=request.POST.get("id")
            for i in range(len(opera_data)):
                if opera_data[i].get("id","不存在id")==edit_id:
                    return JsonResponse({'data': opera_data[i]})
        elif post_data=='del':
            del_id=request.POST.get("id")
            for i in range(len(opera_data)):
                if opera_data[i].get("id","不存在id")==del_id:
                    opera_data.pop(i)  #del_data.remove(del_data[i])
                    break
            save_app(app,opera_data,"del")
        elif post_data=='state':
            state_id=request.POST.get("id")
            for i in range(len(opera_data)):
                if opera_data[i]['id']==state_id:
                    if opera_data[i]['state']=='0':
                        opera_data[i]['state']='1'
                    else:
                        opera_data[i]['state']='0'
                    break
            save_app(app,opera_data,"state")
        elif post_data=='title':
            id=request.POST.get('id')
            for i in range(len(opera_data)):
                if opera_data[i]['id']==id:
                    return JsonResponse({'data': opera_data[i]['mxs']})
        else:
            # 页面传递过来的数据，选择编辑、添加
            indata = request.body
            indata = indata.decode('utf-8')
            indata = json.loads(indata)
            dt=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            indata["time"]=dt
            # 如果取得到id 就是编辑，否则就是添加
            if indata["id"]!=" ":
                # 找到要更新的一条数据
                update_data={}
                for i in range(len(opera_data)):
                    if opera_data[i]['id']==indata["id"]:
                        update_data=opera_data[i]
                        opera_data.pop(i)       # 删除要修改的数据
                        break
                update_data.update(indata)  # 更新修改过的数据
                opera_data.append(update_data)
                tt="modify_success"
                save_app(app,opera_data,"modify_success")
            else:
                max_id=0
                for i in opera_data:
                    v_id=int(i['id'])
                    if max_id<v_id:
                        max_id=v_id
                indata['id']=str(max_id+1)
                opera_data.append(indata)
                tt="add_success"
            save_app(app,opera_data,tt)
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
                ret = update_app_info(app_id, app_name, app_category, app_model, app_describe, app_site, app_logo)
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
