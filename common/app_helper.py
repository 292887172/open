# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.core.paginator import Paginator
from model.center.app import App
from model.center.app_history import AppHistory
from model.center.developer import Developer
from base.convert import utctime2localtime
from base.convert import date2ymdhms
from base.util import gen_app_app_id
from base.util import gen_app_app_secret, gen_app_default_conf
from base.const import ConventionValue
from common.api_helper import create_sandbox_api_app
from common.api_helper import create_release_api_app
from common.api_helper import delete_release_api_app
from common.api_helper import delete_api_app
from common.api_helper import reset_api_app_secret
import time
import logging
import datetime
__author__ = 'achais'
_convention = ConventionValue()


def create_app(developer_id, app_name, app_model, app_category, app_category_detail, app_command, device_conf, app_factory_id):
    """
    创建应用
    :param developer_id: 开发者编号
    :param app_name: 应用名称
    :param app_model: 型号
    :param app_category: 分类
    :param app_category_detail: 详细分类
    :param app_command: app是否全指令
    :param app_factory_id: app品牌id
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
                if not device_conf:
                        device_conf = ""
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
                          )
                app.save()
                break
            except Exception as e:
                del e
        # 同步到 RESTFul API
        create_sandbox_api_app(app_app_id, app_app_secret)
        return app
    except Exception as e:
        logging.getLogger("").error(e)
        return ""


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


def update_app_info(app_id, app_name, app_category, app_model, app_describe, app_site, app_logo, app_command, app_device_type):
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
    :return:
    """
    try:
        params = dict(
            app_name=app_name,
            app_describe=app_describe,
            app_site=app_site,
            app_category=app_category,
            app_model=app_model,
            app_command=app_command,
            app_update_date=datetime.datetime.utcnow(),
            app_device_type=app_device_type
        )
        if app_logo:
            params["app_logo"] = app_logo

        update_line = App.objects.filter(app_id=int(app_id)).update(**params)
        if update_line > 0:
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
            return True
        else:
            return False
    except Exception as e:
        logging.getLogger("").error(e)
        return False


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
