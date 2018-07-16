# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.core.paginator import Paginator
from model.center.app import App
from model.center.app_history import AppHistory
from model.center.developer import Developer
from model.center.account import Account
from model.center.message import Message
from model.center.device_fun import Device_Fun
from base.convert import utctime2localtime
from base.convert import date2ymdhms
from base.util import gen_app_app_id
from base.util import gen_app_app_secret, gen_app_default_conf
from base.connection import Redis3
from base.const import ConventionValue
from common.api_helper import create_sandbox_api_app
from common.api_helper import create_release_api_app
from common.api_helper import delete_release_api_app
from common.api_helper import delete_api_app
from common.api_helper import reset_api_app_secret
from common.app_api_helper import remove_conf_prefix
from common.message_helper import save_user_message
from conf.message import *

from django.db.models import Q

import logging
import datetime
__author__ = 'achais'
_convention = ConventionValue()


def create_app(developer_id, app_name, app_model, app_category, app_category_detail, app_command, device_conf,
               app_factory_id, app_group, app_logo,app_product_fast, check_status=0):
    """
    创建应用
    :param developer_id: 开发者编号
    :param app_name: 应用名称
    :param app_model: 型号
    :param app_category: 分类
    :param app_category_detail: 详细分类
    :param app_command: 指令类型
    :param device_conf: 产品默认功能配置
    :param app_factory_id: app品牌id
    :param app_group: 设备类型
    :param check_status: 产品审核状态
    :param app_product_fast: 是否快速创建
    :return:
    """
    try:
        developer = Developer.objects.get(developer_id=developer_id)
        app_app_id = ""
        app_app_secret = ""
        while True:
            try:
                app_app_id = gen_app_app_id()
                app_app_secret = gen_app_app_secret()
                try:
                    device_conf = json.dumps(device_conf)
                except Exception as e:
                    pass
                app = App(developer=developer,
                          app_name=app_name,
                          app_appid=app_app_id,
                          app_appsecret=app_app_secret,
                          app_model=app_model,
                          app_command=app_command,
                          app_category=app_category,
                          app_device_type=app_category_detail,
                          device_conf=device_conf,
                          app_config_path='',
                          package_name='',
                          app_factory_uid=app_factory_id,
                          app_group=app_group,
                          app_logo=app_logo,
                          app_create_source=app_product_fast,
                          check_status=check_status,
                          app_create_date=datetime.datetime.utcnow(),
                          app_update_date=datetime.datetime.utcnow()
                          )
                app.save()
                print('保存成功')
                message_content = '"'+ app_name + '"' + CREATE_APP
                save_user_message(developer_id, message_content, USER_TYPE, developer_id)
                break
            except Exception as e:
                del e
        # 同步到 RESTFul API
        create_sandbox_api_app(app_app_id, app_app_secret)
        return app.app_id
    except Exception as e:
        logging.getLogger("").error(e)
        return ""


def update_app_fun_widget(data):
    """

    :param data: 修改该功能点的widget值,有单位、不可控的是input
    :return:
    """
    if not data["mxs"]:
        return "input"
    else:
        return "button"


def del_app(app_id):
    """
    删除应用(移除到历史应用表)
    :param app_id: 应用编号
    :return:
    """
    try:
        app = App.objects.get(app_id=int(app_id))
        new_app_history = AppHistory(app_id=app.app_id,
                                     developer=app.developer,
                                     app_name=app.app_name,
                                     app_describe=app.app_describe,
                                     app_logo=app.app_logo,
                                     app_action=app.app_action,
                                     check_status=app.check_status,
                                     check_remarks=app.check_remarks,
                                     app_appid=app.app_appid,
                                     app_appsecret=app.app_appsecret,
                                     app_is_forbid=app.app_is_forbid,
                                     app_brand=app.app_brand,
                                     app_category=app.app_category,
                                     app_model=app.app_model,
                                     app_level=app.app_level,
                                     app_group=app.app_group,

                                     app_push_url=app.app_push_url,
                                     app_push_token=app.app_push_token,
                                     app_device_type=app.app_device_type,
                                     app_protocol_type=app.app_protocol_type,
                                     app_create_date=app.app_create_date,
                                     app_update_date=app.app_update_date)
        new_app_history.save()
        app.delete()
        message_content = '"'+ app.app_name + '"' + DEL_APP
        save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id)
        # 删除应用, 同步到 RESTFul API
        delete_api_app(app.app_appid)
        return True
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def release_app(app_id):
    """
    申请发布应用
    :param app_id:
    :return:
    """
    try:
        update_line = App.objects.filter(app_id=int(app_id)).update(check_status=_convention.APP_CHECKING,
                                                                    app_update_date=datetime.datetime.utcnow())
        if update_line > 0:
            app = App.objects.get(app_id=int(app_id))
            message_content = '"'+ app.app_name + '"' + RELEASE_APP
            save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id)
            return True
        else:
            return False
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def cancel_release_app(app_id):
    """
    取消发布应用
    :param app_id:
    :return:
    """
    try:
        update_line = App.objects.filter(app_id=int(app_id)).update(check_status=_convention.APP_UN_CHECK,
                                                                    app_update_date=datetime.datetime.utcnow())
        if update_line > 0:
            # 应用下架, 同步到 RESTFul API
            app = App.objects.get(app_id=int(app_id))
            message_content = '"'+ app.app_name + '"' + CANCEL_RELEASE_APP
            save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id)
            delete_release_api_app(app.app_appid)
            return True
        else:
            return False
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def off_app(app_id):
    """
    下架应用
    :param app_id:
    :return:
    """
    try:
        update_line = App.objects.filter(app_id=int(app_id)).update(check_status=_convention.APP_UN_CHECK,
                                                                    app_update_date=datetime.datetime.utcnow())
        if update_line > 0:
            # 应用下架, 同步到 RESTFul API
            app = App.objects.get(app_id=int(app_id))
            message_content = '"'+ app.app_name + '"' + OFF_APP
            save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id)
            delete_release_api_app(app.app_appid)
            return True
        else:
            return False
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def pass_app(app_id):
    """
    通过app, 审核通过
    :param app_id:
    :return:
    """
    try:
        update_line = App.objects.filter(app_id=int(app_id)).update(check_status=_convention.APP_CHECKED,
                                                                    app_update_date=datetime.datetime.utcnow())
        if update_line > 0:
            # APP审核通过, 同步到 RESTFul API
            app = App.objects.get(app_id=int(app_id))
            message_content = '"'+ app.app_name + '"' + PASS_APP
            save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id)
            create_release_api_app(app.app_appid)
            return True
        else:
            return False
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def denied_app(app_id, remark):
    """
    拒绝app, 审核不通过
    :param app_id:
    :param remark:
    :return:
    """
    try:
        if not remark:
            return False
        update_line = App.objects.filter(app_id=int(app_id)).update(check_status=_convention.APP_CHECK_FAILED,
                                                                    check_remarks=remark,
                                                                    app_update_date=datetime.datetime.utcnow())
        if update_line > 0:
            app = App.objects.get(app_id=int(app_id))
            message_content = '"'+ app.app_name + '"' + DENIED_APP
            save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id)
            return True
        else:
            return False
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def fetch_app_data(app_id):
    """
    获取应用信息
    :param app_id:
    :return:
    """
    try:
        app = App.objects.get(app_id=int(app_id))
        if app:
            return app
        else:
            return None
    except Exception as e:
        logging.getLogger("").error(e)
        return None


def update_app_info(app_id, app_name, app_model, app_describe, app_site, app_logo, app_command, app_group, app_factory_uid):
    """
    更新应用基础信息
    :param app_id:
    :param app_name:
    :param app_category:
    :param app_model:
    :param app_describe:
    :param app_site:
    :param app_logo:
    :param app_command:
    :param app_device_type:
    :param app_group：
    :param app_factory_uid:
    :return:
    """
    try:
        params = dict(
            app_name=app_name,
            app_describe=app_describe,
            app_site=app_site,
            app_model=app_model,
            app_command=app_command,
            app_update_date=datetime.datetime.utcnow(),
            app_group=app_group,
            app_factory_uid=app_factory_uid,
        )
        if app_logo:
            params["app_logo"] = app_logo
        update_line = App.objects.filter(app_id=int(app_id)).update(**params)
        if update_line > 0:
            app = App.objects.get(app_id=int(app_id))
            message_content = '"'+ app.app_name + '"' + UPDATE_APP
            save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id)
            return True
        else:
            return False
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def update_app_config(app_id, app_push_url, app_push_token):
    """
    更新应用配置信息
    :param app_id:
    :param app_push_url:
    :param app_push_token:
    :return:
    """
    try:
        update_line = App.objects.filter(app_id=int(app_id)).update(app_push_url=app_push_url,
                                                                    app_push_token=app_push_token,
                                                                    app_update_date=datetime.datetime.utcnow())
        if update_line > 0:
            app = App.objects.get(app_id=int(app_id))
            message_content = '"'+ app.app_name + '"' + UPDATE_APP_CONFIG
            save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id)
            return True
        else:
            return False
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def replace_fun_id(opera_data, del_id, is_standa):
    for i in range(len(opera_data)):
        id = int(opera_data[i].get("id"))
        #  标准
        if is_standa is None:
            if id < 101 and (id > int(del_id)):
                opera_data[i]['id'] = id - 1
        elif id >= 101 and (id > int(del_id)):
            opera_data[i]['id'] = id - 1


def add_fun_id(opera_data, indata):
    is_define = int(indata.get("standa_or_define", 0))
    indata['standa_or_define'] = str(is_define)
    if opera_data:
        id = int(opera_data[-1].get("id"))
        # if is_define == 1:
        #     if id < 101:
        #         indata["id"] = '101'
        #     else:
        indata["id"] = str(id + 1)
    else:
        indata["id"] = '101'
    return indata


def add_mod_funs(opera_data, device_conf, funs,app_device_type):
    funs = json.loads(funs)
    add_funs = []
    max_num = 0
    k = 0
    for data in opera_data:
        temp = int(data.get("id"))
        if temp < 101 and temp > max_num:
            max_num = temp
    if int(app_device_type) == 0:
        for device in PROTOCOL_KU:
            if device.get("Stream_ID") in funs:
                k += 1
                device["id"] = max_num + k
                add_funs.append(device)
        opera_data.extend(add_funs)
    else:
        for device in device_conf:
            if device.get("Stream_ID") in funs:
                k += 1
                device["id"] = max_num + k
                add_funs.append(device)
        opera_data.extend(add_funs)
    opera_data.sort(key=lambda x: int(x.get("id")))


def get_mod_funs(opera_data, device_conf,app_device_type):
    mod = []
    modd = []
    fun_name = list(map(lambda x: x["Stream_ID"], opera_data))
    print('data',device_conf)
    if int(app_device_type) == 0:

        for device in PROTOCOL_KU:

            if device.get("Stream_ID") in fun_name:
                modd.append({"name": device.get("name"), "Stream_ID": device.get("Stream_ID")})
            if device.get("Stream_ID") not in fun_name:
                mod.append({"name": device.get("name"), "Stream_ID": device.get("Stream_ID")})
        print(modd)
    else:
        for device in device_conf:

            if device.get("Stream_ID") in fun_name:
                modd.append({"name": device.get("name"), "Stream_ID": device.get("Stream_ID")})
            if device.get("Stream_ID") not in fun_name:
                mod.append({"name": device.get("name"), "Stream_ID": device.get("Stream_ID")})
        print(modd)
    return mod


def reset_app_secret(app_id):
    """
    重置应用的AppSecret
    :param app_id:
    :return:
    """
    try:
        app = App.objects.get(app_id=int(app_id))
        new_app_secret = gen_app_app_secret()
        update_line = App.objects.filter(app_id=int(app_id)).update(app_appsecret=new_app_secret,
                                                                    app_update_date=datetime.datetime.utcnow())
        if update_line > 0:
            # 同步到 RESTFul API
            message_content = '"'+ app.app_name + '"' + RESET_APP_SECRET
            save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id)
            reset_api_app_secret(app.app_appid, new_app_secret)
            return new_app_secret
        else:
            return ""
    except Exception as e:
        logging.getLogger("").error(e)
        return ""


def fetch_published_app_data(page, limit, order_by_names):
    """
    获取所有已经发布的应用信息
    :param page:
    :param limit:
    :return:
    """
    try:
        pager = Paginator(App.objects.filter(check_status=_convention.APP_CHECKED).order_by(order_by_names),
                          int(limit))
        apps = pager.page(int(page))
        total_count = pager.count
        data = []
        for app in apps:
            d = dict(
                id=app.app_id,
                name=app.app_name,
                logo=app.app_logo,
                describe=app.app_describe,
                site=app.app_site,
                createtime=date2ymdhms(utctime2localtime(app.app_update_date))
            )
            data.append(d)
        result = dict(
            totalCount=total_count,
            items=data
        )
        return result
    except Exception as e:
        logging.getLogger("").error(e)
        return ""


def fetch_publishing_app_data(page, limit, order_by_names):
    """
    获取所有发布中的应用信息
    :param page:
    :param limit:
    :return:
    """
    try:
        pager = Paginator(App.objects.filter(check_status=_convention.APP_CHECKING).order_by(order_by_names),
                          int(limit))
        apps = pager.page(int(page))
        total_count = pager.count
        data = []
        for app in apps:
            d = dict(
                id=app.app_id,
                name=app.app_name,
                logo=app.app_logo,
                describe=app.app_describe,
                site=app.app_site,
                createtime=date2ymdhms(utctime2localtime(app.app_update_date))
            )
            data.append(d)
        result = dict(
            totalCount=total_count,
            items=data
        )
        return result
    except Exception as e:
        logging.getLogger("").error(e)
        return ""


def fetch_all_app_data(page, limit, order_by_names):
    """
    获取所有的应用信息
    :param page:
    :param limit:
    :return:
    """
    try:
        pager = Paginator(App.objects.filter().order_by(order_by_names),
                          int(limit))
        apps = pager.page(int(page))
        total_count = pager.count
        data = []

        for app in apps:
            try:
                an = Account.objects.filter(account_id__contains=app.developer.developer_id[2:]).extra(
                    order_by=('account_create_date',))[0:1]
                nickname = an[0].account_nickname
                if not nickname:
                    nickname = app.developer.developer_id
            except Exception as e:
                print(e)
                nickname = ''
                pass

            d = dict(
                id=app.app_id,
                name=app.app_name,
                logo=app.app_logo,
                describe=app.app_appid[-8:],
                site=app.app_site,
                nickname=nickname,
                createtime=date2ymdhms(utctime2localtime(app.app_update_date))
            )

            data.append(d)

        result = dict(
            totalCount=total_count,
            items=data
        )
        return result
    except Exception as e:
        print(e)
        logging.getLogger("").error(e)
        return ""
def fetch_one_app_data(serach,page, limit, order_by_names):
    try:
        pager = Paginator(App.objects.filter(Q(app_appid__icontains=serach)|Q(app_name__icontains=serach)).order_by(order_by_names),
                          int(limit))
        apps = pager.page(int(page))
        total_count = pager.count
        data = []

        for app in apps:
            try:
                an = Account.objects.filter(account_id__contains=app.developer.developer_id[2:]).extra(
                    order_by=('account_create_date',))[0:1]
                nickname = an[0].account_nickname
                if not nickname:
                    nickname = app.developer.developer_id
            except Exception as e:
                print(e)
                nickname = ''
                pass

            d = dict(
                id=app.app_id,
                name=app.app_name,
                logo=app.app_logo,
                describe=app.app_appid[-8:],
                site=app.app_site,
                nickname=nickname,
                createtime=date2ymdhms(utctime2localtime(app.app_update_date))
            )

            data.append(d)

        result = dict(
            totalCount=total_count,
            items=data
        )
        return result
    except Exception as e:
        print(e)
        logging.getLogger("").error(e)
        return ""

def save_app(app, opera_data,cook_ies):
    # 保存修改后的device_config
    r = Redis3(rdb=6).client
    app.device_conf = json.dumps(opera_data)
    key = app.app_appid[-8:]
    try:
        Message.objects.create(message_content='功能更新',message_type=int(1),message_handler_type=int(1),device_key=key,message_sender=cook_ies,message_target=cook_ies,create_date=datetime.datetime.utcnow(),update_date=datetime.datetime.utcnow())

    except Exception as e:
        print(e)
        logging.getLogger("").error(e)
    remove_conf_prefix(key)
    app.app_update_date = datetime.datetime.utcnow()
    app.save()
    data = {'rows': opera_data, 'check_state': app.check_status}
    r.set("product_funs" + str(app.app_id), json.dumps(data), 3600*24*3)

def check_cloud(opera_data):
    # 检查功能是否被设为云菜谱可控
    flag = 0
    for data in opera_data:
        value = data.get("isCloudMenu")
        if value and int(value) == 1:
            flag = 1
            break
    return flag