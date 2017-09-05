# !/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

__author__ = 'achais'

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.http.response import HttpResponse
from common.app_helper import fetch_publishing_app_data
from common.app_helper import fetch_published_app_data
from common.app_helper import pass_app
from common.app_helper import denied_app
from common.app_helper import fetch_app_data
from common.app_api_helper import fetch_api_list_data
from common.app_api_helper import fetch_api_data
from common.app_api_helper import del_api
from common.app_api_helper import add_api
from common.app_api_helper import update_api
from common.developer_helper import fetch_checking_developer_data
from common.developer_helper import fetch_developer_list_data
from common.developer_helper import fetch_developer_data
from common.developer_helper import denied_developer
from common.developer_helper import pass_developer
from common.developer_helper import toggle_forbid_developer
from common.account_helper import fetch_user_list_data
from common.account_helper import toggle_forbid_user
from common.smart_helper import update_app_protocol
from base.convert import date2ymdhms
from base.convert import utctime2localtime
from django.contrib.auth import authenticate
from model.center.account import Account, MyUserManager
from model.center.app import App
from common.app_helper import create_app
import logging
from conf.sessionconf import *
from conf.newuserconf import *

import simplejson as json

from base.const import ConventionValue

_convention = ConventionValue()


@login_required
def admin_home(request):
    if not request.user.account_type == _convention.USER_IS_ADMIN:
        return HttpResponseRedirect(reverse("center"))

    def get():
        template = "admin/index.html"
        content = dict()
        return render(request, template, content)

    def post():
        res = {"code": 10000}
        action = request.POST.get("action", "")
        if action in ("toggle_forbid_developer", "fail_developer", "pass_developer", "toggle_forbid_user",
                      "fail_product", "pass_product",
                      "del_api", "add_api", "update_api"):
            if action == "fail_developer":
                # 开发者审核不通过
                developer_id = request.POST.get("developer_id", "")
                remark = request.POST.get("remark", "")
                ret = denied_developer(developer_id, remark)
                res["data"] = ret

                return HttpResponse(json.dumps(res, separators=(",", ":")))
            elif action == "pass_developer":
                # 开发者审核通过
                developer_id = request.POST.get("developer_id", "")
                ret = pass_developer(developer_id)
                res["data"] = ret
                for i in range(len(APP_NAME)):
                    result = create_app(developer_id, APP_NAME[i], APP_MODEL[i], APP_CATEGORY[i], DEVICE_TYPE[i], APP_COMMAND[i], DEVICE_CONF[i], APP_FACTORY_UID[i], 0, 3)
                    result.app_logo = APP_LOGO[i]
                    result.save()
                return HttpResponse(json.dumps(res, separators=(",", ":")))
            elif action == "toggle_forbid_developer":
                # 切换开发者禁用状态
                developer_id = request.POST.get("developer_id", "")
                ret = toggle_forbid_developer(developer_id)
                res["data"] = ret
                return HttpResponse(json.dumps(res, separators=(",", ":")))
            elif action == "toggle_forbid_user":
                # 切换用户禁用状态
                user_id = request.POST.get("user_id", "")
                ret = toggle_forbid_user(user_id)
                res["data"] = ret
                return HttpResponse(json.dumps(res, separators=(",", ":")))
            elif action == "fail_product":
                # 产品审核不通过
                app_id = request.POST.get("app_id", "")
                remark = request.POST.get("remark", "")
                ret = denied_app(app_id, remark)
                res["data"] = ret
                return HttpResponse(json.dumps(res, separators=(",", ":")))
            elif action == "pass_product":
                # 产品审核通过
                app_id = request.POST.get("app_id", "")
                ret = pass_app(app_id)
                app = App.objects.get(app_id=app_id)
                if str(app.app_group) == '2':
                    update_app_protocol(app)
                res["data"] = ret
                return HttpResponse(json.dumps(res, separators=(",", ":")))
            elif action == "del_api":
                # 删除接口
                api_id = request.POST.get("api_id", "")
                ret = del_api(api_id)
                res["data"] = ret
                return HttpResponse(json.dumps(res, separators=(",", ":")))
            elif action == "add_api":
                # 添加接口
                api_name = request.POST.get("api_name", "")
                api_url = request.POST.get("api_url", "")
                api_type = request.POST.get("api_type", "")
                api_request_type = request.POST.get("api_request_type", "")
                api_params = request.POST.get("api_params", "")
                api_return = request.POST.get("api_return", "")
                api_describe = request.POST.get("api_describe", "")
                api_doc_url = request.POST.get("api_doc_url", "")
                api_action_url = request.POST.get("api_action_url", "")
                api_classify = request.POST.get("api_classify", "")
                api_function = request.POST.get("api_function", "")
                api_level = request.POST.get("api_level", "")
                api_group = request.POST.get("api_group", "")
                api_invoke_total = request.POST.get("api_invoke_total", "")
                api_port = request.POST.get("api_port", "")

                ret = add_api(api_name=api_name, api_url=api_url, api_type=api_type, api_method=api_request_type,
                              api_params=api_params, api_return=api_return, api_describe=api_describe,
                              api_doc_url=api_doc_url, api_action_url=api_action_url, api_classify=api_classify,
                              api_function=api_function, api_level=api_level, api_group=api_group,
                              api_invoke_total=api_invoke_total, api_port=api_port)
                if ret:
                    res["data"] = ret
                else:
                    res["code"] = -1
                    res["msg"] = "missing import param"
            elif action == "update_api":
                # 更新接口
                api_id = request.POST.get("api_id", "")
                api_name = request.POST.get("api_name", "")
                api_url = request.POST.get("api_url", "")
                api_type = request.POST.get("api_type", "")
                api_request_type = request.POST.get("api_request_type", "")
                api_params = request.POST.get("api_params", "")
                api_return = request.POST.get("api_return", "")
                api_describe = request.POST.get("api_describe", "")
                api_doc_url = request.POST.get("api_doc_url", "")
                api_action_url = request.POST.get("api_action_url", "")
                api_classify = request.POST.get("api_classify", "")
                api_function = request.POST.get("api_function", "")
                api_level = request.POST.get("api_level", "")
                api_group = request.POST.get("api_group", "")
                api_invoke_total = request.POST.get("api_invoke_total", "")
                api_port = request.POST.get("api_port", "")

                ret = update_api(api_id=api_id, api_name=api_name, api_url=api_url, api_type=api_type,
                                 api_method=api_request_type, api_params=api_params, api_return=api_return,
                                 api_describe=api_describe, api_doc_url=api_doc_url, api_action_url=api_action_url,
                                 api_classify=api_classify, api_function=api_function, api_level=api_level,
                                 api_group=api_group, api_invoke_total=api_invoke_total, api_port=api_port)
                if ret:
                    res["data"] = ret
                else:
                    res["code"] = -1
                    res["msg"] = "missing import param"
            return HttpResponse(json.dumps(res, separators=(",", ":")))

    if request.method == "GET":
        return get()
    elif request.method == "POST":
        return post()


def account_list_data(request):
    """
    所有用户列表
    :param request:
    :return:
    """

    def get():
        page = request.GET.get("page", 1)
        limit = request.GET.get("limit", 20)
        sort = request.GET.get("sort", "")
        (sort_name, sort_status) = sort.split(".")
        order_by_names = ""
        if sort_status == "desc":
            order_by_names = "-"
        if sort_name == "createtime":
            order_by_names += "account_create_date"
        ret = fetch_user_list_data(page, limit, order_by_names)
        return HttpResponse(json.dumps(ret, separators=(",", ":")))

    if request.method == "GET":
        return get()


def developer_list_data(request):
    """
    开发者列表
    :param request:
    :return:
    """

    def get():
        page = request.GET.get("page", 1)
        limit = request.GET.get("limit", 20)
        sort = request.GET.get("sort", "")
        (sort_name, sort_status) = sort.split(".")
        order_by_names = ""
        if sort_status == "desc":
            order_by_names = "-"
        if sort_name == "createtime":
            order_by_names += "developer_create_date"
        ret = fetch_developer_list_data(page, limit, order_by_names)
        return HttpResponse(json.dumps(ret, separators=(",", ":")))

    if request.method == "GET":
        return get()


def developer_checking_data(request):
    """
    审核中的开发者数据
    :param request:
    :return:
    """

    def get():
        page = request.GET.get("page", 1)
        limit = request.GET.get("limit", 20)
        sort = request.GET.get("sort", "")
        (sort_name, sort_status) = sort.split(".")
        order_by_names = ""
        if sort_status == "desc":
            order_by_names = "-"
        if sort_name == "createtime":
            order_by_names += "developer_update_date"
        ret = fetch_checking_developer_data(page, limit, order_by_names)
        return HttpResponse(json.dumps(ret, separators=(",", ":")))

    if request.method == "GET":
        return get()


def developer_detail_modal(request):
    """
    开发者详情modal详情
    :param request:
    :return:
    """

    def get():
        developer_id = request.GET.get("id", "")
        modal_title = "开发者信息"
        modal_content = "数据加载失败"
        template = """
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal">&times;</button>
              <h4 class="modal-title">{0}</h4>
            </div>
            <div class="modal-body">
              {1}
            </div>
            <div class="modal-footer">
              <a href="#" class="btn btn-default btn-s-xs" data-dismiss="modal">关闭</a>
            </div>
          </div><!-- /.modal-content -->
        </div><!-- /.modal-dialog -->
        """
        content_template = """
        <form class="form-horizontal">
        <div class="form-group">
            <label class="col-lg-3 control-label">开发者账号</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">用户账号</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">用户来源</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">唯一标识</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">是否禁用</label>
            <div class="col-lg-9">
            <p class="form-control-static">{} (1: 禁用, 0: 不禁用)</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">厂家</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">公司</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">网站</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">职位</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">团队人数</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">真实姓名</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">地址</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">手机号</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">邮箱</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">更新时间</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">创建时间</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        </form>
        """
        if developer_id:
            developer = fetch_developer_data(developer_id=developer_id)
            if developer:
                account = developer.developer_account if developer.developer_account else ""
                factory = developer.developer_factory if developer.developer_factory else ""
                inc = developer.developer_inc if developer.developer_inc else ""
                site = developer.developer_site if developer.developer_site else ""
                job = developer.developer_job if developer.developer_job else ""
                person = developer.developer_person if developer.developer_person else "0"
                developer_from = developer.developer_from if developer.developer_from else ""
                symbol = developer.developer_symbol if developer.developer_symbol else ""
                is_forbid = developer.developer_is_forbid if developer.developer_is_forbid is not None else ""
                address = developer.developer_address if developer.developer_address else ""
                real_name = developer.developer_realname if developer.developer_realname else ""
                mobile = developer.developer_mobile if developer.developer_mobile else ""
                email = developer.developer_email if developer.developer_email else ""
                developer_create_date = date2ymdhms(utctime2localtime(developer.developer_create_date))
                developer_update_date = date2ymdhms(utctime2localtime(developer.developer_update_date))

                modal_content = content_template.format(developer_id, account, developer_from, symbol, is_forbid,
                                                        factory, inc, site, job, person, real_name, address, mobile,
                                                        email, developer_update_date, developer_create_date)
        ret = template.format(modal_title, modal_content)
        return HttpResponse(ret)

    if request.method == "GET":
        return get()


def application_checked_data(request):
    """
    已经发布的应用数据接口
    :param request:
    :return:
    """

    def get():
        page = request.GET.get("page", 1)
        limit = request.GET.get("limit", 20)
        sort = request.GET.get("sort", "")
        (sort_name, sort_status) = sort.split(".")
        order_by_names = ""
        if sort_status == "desc":
            order_by_names = "-"
        if sort_name == "createtime":
            order_by_names += "app_update_date"
        ret = fetch_published_app_data(page, limit, order_by_names)
        return HttpResponse(json.dumps(ret, separators=(",", ":")))

    def post():
        pass

    if request.method == "GET":
        return get()
    elif request.method == "POST":
        return post()


def application_checking_data(request):
    """
    发布需要审核的应用的数据接口
    :param request:
    :return:
    """

    def get():
        page = request.GET.get("page", 1)
        limit = request.GET.get("limit", 20)
        sort = request.GET.get("sort", "")
        (sort_name, sort_status) = sort.split(".")
        order_by_names = ""
        if sort_status == "desc":
            order_by_names = "-"
        if sort_name == "createtime":
            order_by_names += "app_update_date"
        ret = fetch_publishing_app_data(page, limit, order_by_names)
        return HttpResponse(json.dumps(ret, separators=(",", ":")))

    def post():
        pass

    if request.method == "GET":
        return get()
    elif request.method == "POST":
        return post()


def application_detail_modal(request):
    """
    应用详情modal详情
    :param request:
    :return:
    """

    def get():
        app_id = request.GET.get("id", "")
        modal_title = "应用详情"
        modal_content = "数据加载失败"
        template = """
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal">&times;</button>
              <h4 class="modal-title">{0}</h4>
            </div>
            <div class="modal-body">
              {1}
            </div>
            <div class="modal-footer">
              <a href="#" class="btn btn-default btn-s-xs" data-dismiss="modal">关闭</a>
            </div>
          </div><!-- /.modal-content -->
        </div><!-- /.modal-dialog -->
        """
        content_template = """
        <form class="form-horizontal">
        <div class="form-group">
            <label class="col-lg-3 control-label">应用名称</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">应用描述</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">推送Url地址</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">推送UrlToken</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">品牌</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">分类</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">型号</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">等级</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">分组</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">设备类型</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}（0：未知,1：油烟机，2：集成灶，3：冰柜，4：洗衣机）</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">协议类型</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}（1:53iq协议，2：阿里小智协议，3：京东协议）</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">更新时间</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">创建时间</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        </form>
        """

        if app_id:
            app = fetch_app_data(app_id)
            if app:
                app_name = app.app_name if app.app_name else ""
                app_describe = app.app_describe if app.app_describe else ""
                # 设备品牌
                app_brand = app.app_brand if app.app_brand else ""
                app_category = app.app_category if app.app_category else ""
                app_model = app.app_model if app.app_model else ""
                app_level = app.app_level if app.app_level is not None else ""
                app_group = app.app_group if app.app_group is not None else ""
                app_push_url = app.app_push_url if app.app_push_url else ""
                app_push_token = app.app_push_token if app.app_push_token else ""
                # 设备类型（0：未知,1：油烟机，2：集成灶，3：冰柜，4：洗衣机）
                app_device_type = app.app_device_type if app.app_device_type is not None else ""
                # 协议类型（1:53iq协议，2：阿里小智协议，3：京东协议）
                app_protocol_type = app.app_protocol_type if app.app_protocol_type is not None else ""
                app_create_date = date2ymdhms(utctime2localtime(app.app_create_date))
                app_update_date = date2ymdhms(utctime2localtime(app.app_update_date))
                modal_content = content_template.format(app_name, app_describe, app_push_url, app_push_token,
                                                        app_brand, app_category, app_model, app_level, app_group,
                                                        app_device_type, app_protocol_type,
                                                        app_update_date, app_create_date)
        ret = template.format(modal_title, modal_content)
        return HttpResponse(ret)

    if request.method == "GET":
        return get()


def api_list_data(request):
    """
    所有"接口"数据接口
    :param request:
    :return:
    """

    def get():
        page = request.GET.get("page", 1)
        limit = request.GET.get("limit", 20)
        sort = request.GET.get("sort", "")
        (sort_name, sort_status) = sort.split(".")
        order_by_names = ""
        if sort_status == "desc":
            order_by_names = "-"
        if sort_name == "createtime":
            order_by_names += "api_create_date"
        ret = fetch_api_list_data(page, limit, order_by_names)
        return HttpResponse(json.dumps(ret, separators=(",", ":")))

    def post():
        pass

    if request.method == "GET":
        return get()
    elif request.method == "POST":
        return post()


def api_data(request):
    def get():
        ret = {"code": 10000}
        api_id = request.GET.get("id", "")
        if not api_id:
            return HttpResponse("")
        api = fetch_api_data(api_id)
        if api:
            api_name = api.api_name if api.api_id else ""
            api_describe = api.api_describe if api.api_describe else ""
            api_url = api.api_url if api.api_url else ""
            api_request_type = api.api_request_type if api.api_request_type else ""
            api_type = api.api_type if api.api_type is not None else ""
            api_params = api.api_params if api.api_params else ""
            api_return = api.api_return if api.api_return else ""
            api_doc_url = api.api_doc_url if api.api_doc_url else ""
            api_action_url = api.api_action_url if api.api_action_url else ""
            api_port = api.api_port if api.api_port is not None else "80"
            api_classify = api.api_classify if api.api_classify else ""
            api_function = api.api_function if api.api_function else ""
            api_level = api.api_level if api.api_level is not None else ""
            api_group = api.api_group if api.api_group is not None else ""
            api_invoke_total = api.api_invoke_total if api.api_invoke_total is not None else ""
            api_is_forbid = api.api_is_forbid if api.api_is_forbid is not None else ""
            api_create_date = api.api_create_date if api.api_create_date else ""
            data = dict(
                api_name=api_name,
                api_describe=api_describe,
                api_url=api_url,
                api_request_type=api_request_type,
                api_type=api_type,
                api_params=api_params,
                api_return=api_return,
                api_doc_url=api_doc_url,
                api_action_url=api_action_url,
                api_port=api_port,
                api_classify=api_classify,
                api_function=api_function,
                api_level=api_level,
                api_group=api_group,
                api_invoke_total=api_invoke_total,
                api_is_forbid=api_is_forbid,
                api_create_date=date2ymdhms(api_create_date)
            )
            ret["data"] = data
            if data:
                return HttpResponse(json.dumps(ret, separators=(",", ":")))
        else:
            return HttpResponse("")

    if request.method == "GET":
        return get()


def api_detail_modal(request):
    """
    "接口"详情modal详情
    :param request:
    :return:
    """

    def get():
        api_id = request.GET.get("id", "")
        modal_title = "应用详情"
        modal_content = "数据加载失败"
        template = """
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal">&times;</button>
              <h4 class="modal-title">{0}</h4>
            </div>
            <div class="modal-body">
              {1}
            </div>
            <div class="modal-footer">
              <a href="#" class="btn btn-default btn-s-xs" data-dismiss="modal">关闭</a>
            </div>
          </div><!-- /.modal-content -->
        </div><!-- /.modal-dialog -->
        """
        content_template = """
        <form class="form-horizontal">
        <div class="form-group">
            <label class="col-lg-3 control-label">接口名称</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">接口描述</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">接口地址</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">请求方式</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">请求端口</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">接口类型</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">参数</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">文档地址</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">未获得时操作地址</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">分类</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">功能</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">等级</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">分组</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">每日调用次数上限</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">禁用</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        <div class="line line-dashed b-b line-lg pull-in"></div>
        <div class="form-group">
            <label class="col-lg-3 control-label">创建时间</label>
            <div class="col-lg-9">
            <p class="form-control-static">{}</p>
            </div>
        </div>
        </form>
        """

        if api_id:
            api = fetch_api_data(api_id)
            if api:
                api_name = api.api_name if api.api_id else ""
                api_describe = api.api_describe if api.api_describe else ""
                api_url = api.api_url if api.api_url else ""
                api_request_type = api.api_request_type if api.api_request_type else ""
                api_type = api.api_type if api.api_type is not None else ""
                api_params = api.api_params if api.api_params else ""
                api_doc_url = api.api_doc_url if api.api_doc_url else ""
                api_action_url = api.api_action_url if api.api_action_url else ""
                api_port = api.api_port if api.api_port is not None else "80"
                api_classify = api.api_classify if api.api_classify else ""
                api_function = api.api_function if api.api_function else ""
                api_level = api.api_level if api.api_level is not None else ""
                api_group = api.api_group if api.api_group is not None else ""
                api_invoke_total = api.api_invoke_total if api.api_invoke_total is not None else ""
                api_is_forbid = api.api_is_forbid if api.api_is_forbid is not None else ""
                api_create_date = api.api_create_date if api.api_create_date else ""

                modal_content = content_template.format(api_name, api_describe, api_url, api_request_type.upper(),
                                                        api_port, api_type, api_params, api_doc_url, api_action_url,
                                                        api_classify, api_function, api_level, api_group,
                                                        api_invoke_total, api_is_forbid, api_create_date)
        ret = template.format(modal_title, modal_content)
        return HttpResponse(ret)

    if request.method == "GET":
        return get()

@login_required
def modify_pwd_admin(request):
    """
    管理员修改密码
    :param request:
    :return:
    """
    if request.method == 'POST':
        code = request.POST.get('code', '')
        if code is None:
            msg = '未输入验证码'
            return HttpResponse(json.dumps({'status': 3, 'error': '', 'msg': msg}))
        if code.lower() == str(request.session[SESSION_LOGIN_VALIDATE]).lower():

            account_id = request.user.account_id
            old_pwd = request.POST.get('old_pwd', '')
            new_pwd = request.POST.get('new_pwd', '')
            new_pwd2 = request.POST.get('new_pwd2', '')
            user_id = request.POST.get('user_id', '')
            print(account_id, user_id)
            account_type = request.user.account_type
            print('account_type:', account_type)

            if old_pwd is None:
                msg = '未输入当前密码'
                return HttpResponse(json.dumps({'status': 4, 'error': '', 'msg': msg}))
            if new_pwd is None:
                msg = '未输入新密码'
                return HttpResponse(json.dumps({'status': 5, 'error': '', 'msg': msg}))
            if new_pwd2 is None:
                msg = '未确认新密码'
                return HttpResponse(json.dumps({'status': 6, 'error': '', 'msg': msg}))
            if new_pwd != new_pwd2:
                msg = '两次密码不一致'
                return HttpResponse(json.dumps({'status': 7, 'error': '', 'msg': msg}))
            if account_id == user_id:
                r = authenticate(username=account_id, password=old_pwd)
                if r:
                    try:
                        Account.objects.admin_change_password(account_id, new_pwd, account_type)
                        msg = '修改成功'
                    except Exception as e:
                        logging.getLogger('').info(str(e))
                        msg = '修改失败'
                    return HttpResponse(json.dumps({'status': 0, 'error': '', 'msg': msg}))

                else:
                    return HttpResponse(json.dumps({'status': 1, 'error': '密码错误'}))
            else:
                return HttpResponse(json.dumps({'status': -1, 'error': '请求异常'}))
        else:
            return HttpResponse(json.dumps({'status': 2, 'error': '验证码错误'}))
    else:
        try:
            account_id = request.user.account_id
            phone = request.user.account_phone
            email = request.user.account_email
        except Exception as e:
            logging.getLogger('').info(str(e))
    return render(request, 'admin/modify-pwd-admin.html', locals())