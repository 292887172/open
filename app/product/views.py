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
        app_model = request.POST.get("product_model", "")
        if not developer_id:
            ret["code"] = 100001
            ret["msg"] = "missing developer_id"
            ret["message"] = "缺少开发者账号ID"
            return HttpResponse(json.dumps(ret, separators=(",", ':')))
        # 创建一个app
        try:
            if not developer_id or not app_name or not app_category:
                ret["code"] = 100002
                ret["msg"] = "invalid app_id"
                ret["message"] = "无效的APP_ID"
                return HttpResponse(json.dumps(ret, separators=(",", ':')))
            app_name = create_app(developer_id, app_name, app_model, app_category)
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
    #  从数据库中读取出来信息，然后将数据保存到grid_data中
    # db=get_db()
    # data=db.argueinfo.find({},{'_id':0})
    # if data:
    #     grid_data=[]
    #     for i in data:
    #         grid_data.append(i)
    #     print(grid_data)
    grid_data=[]
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

    def post():
        app_id = request.GET.get("ID", "")
        app=App.objects.get(app_id=app_id)
        grid_data=app.device_conf
        data=json.loads(grid_data)
        # 获取到数据库中的设备配置信息
        post_data=request.POST.get("name")
         # 接收页面传送信息
        if post_data=='list':

             #  如果是点击list.html页面就将数据传送给grid_data
            return JsonResponse({'data': data})
        # 获取要编辑的id对应的一组信息，将这一组要编辑的信息返回给edit页面，页面编辑后保存，将信息再次返回，然后对修改后的数据进行融合
        elif post_data=='edit':
            edit_id=request.POST.get("id")
            for i in range(len(data)):
                if data[i].get("id","不存在id")==edit_id:
                    return JsonResponse({'data': data[i]})
            edit_data=request.body
            edit_data=edit_data.decode('utf-8')
            print(edit_data)

        elif post_data=='del':
            del_id=request.POST.get("id")
            for i in range(len(data)):
                if data[i].get("id","不存在id")==del_id:
                    data.pop(i)  #del_data.remove(del_data[i])
                    break
            after_data=json.dumps(data)
            app.device_conf=after_data
            app.save()

        # 接受要添加的信息
        indata = request.body
        indata = indata.decode('utf-8')
        indata = json.loads(indata)
        dt=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        indata["time"]=dt
        # 如果取得到id 就是编辑，否则就是添加
        print(indata)
        if indata.get("id"):
            # 找到要更新的一条数据
            print("++++++++++++++++++++++++++++++")
            update_data={}
            for i in range(len(data)):
                if data[i]['id']==indata["id"]:
                    update_data=data[i]
                    data.pop(i)       # 删除要修改的数据
                    break
            update_data.update(indata)  # 更新修改过的数据 
            data.append(update_data)    # 添加到data数据中
            
            app.device_conf=json.dumps(data)
            app.save()
        else:
            print("----------------------------------")
            indata['id']=str(len(data)+1)
            # 保存修改
            old_conf=data
            old_conf.append(indata)
            app.device_conf=json.dumps(old_conf)
            #app.save()


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
