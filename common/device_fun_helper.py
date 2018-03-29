# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from model.center.device_fun import Device_Fun
from django.core.paginator import Paginator
from base.convert import date2ymdhms
from base.convert import utctime2localtime
from base.const import ConventionValue

from common.app_helper import save_app

import logging
import datetime
__author__ = 'gmy'
_convention = ConventionValue()


def add_device_fun(key, indata):
    """
    统一产品key重复添加的相同的功能覆盖待完善
    :param key:
    :param indata:
    :return:
    """
    try:
        df = Device_Fun(
            device_key=key[-8:],
            device_function=json.dumps(indata),
            df_check_status=1,
            df_update_date=datetime.datetime.utcnow(),
            df_create_date=datetime.datetime.utcnow()
        )
        df.save()
    except Exception as e:
        print("新增产品保存信息",e)


def pass_fun(app, id):
    try:
        df = Device_Fun.objects.get(df_id=id)
        devices = json.loads(app.device_conf)
        fun = json.loads(df.device_function)
        df.df_check_status = _convention.FUN_CHECKED
        flag = True
        for device in devices:
            if device["Stream_ID"] == fun["Stream_ID"]:
                flag = False
                break
        if flag:
            devices.append(fun)
            save_app(app, devices)
        df.save()
        return True
    except Exception as e:
        logging.getLogger("功能审核通过出错").error(e)
        print(e)
        return False


def denied_fun(app, id):
    try:
        df = Device_Fun.objects.get(df_id=id)
        devices = json.loads(app.device_conf)
        fun = json.loads(df.device_function)
        df.df_check_status = _convention.FUN_CHECKING
        for index,device in enumerate(devices):
            if device["Stream_ID"] == fun["Stream_ID"]:
                devices.pop(index)
                break
        save_app(app,devices)
        df.save()
        return True
    except Exception as e:
        logging.getLogger("功能审核不通过出错").error(e)
        print(e)
        return False


def fetch_all_fun_data(page, limit, order_by_names):
    """
    获取所有的功能信息
    :param page:
    :param limit:
    :return:
    """
    try:
        pager = Paginator(Device_Fun.objects.filter().order_by(order_by_names),
                          int(limit))
        dfs = pager.page(int(page))
        total_count = pager.count
        data = []
        for df in dfs:
            fun = json.loads(df.device_function)
            d = dict(
                id = df.df_id,
                key=df.device_key,
                name=fun["Stream_ID"],
                status=df.df_check_status,
                update_time=date2ymdhms(utctime2localtime(df.df_update_date)),
                create_time=date2ymdhms(utctime2localtime(df.df_create_date)),
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


def fetch_published_fun_data(page, limit, order_by_names):
    """
    获取所有审核通过的功能
    :param page:
    :param limit:
    :return:
    """
    try:
        pager = Paginator(Device_Fun.objects.filter(df_check_status=_convention.FUN_CHECKED).order_by(order_by_names),
                          int(limit))
        dfs = pager.page(int(page))
        total_count = pager.count
        data = []
        for df in dfs:
            fun = json.loads(df.device_function)
            d = dict(
                id = df.df_id,
                key=df.device_key,
                name=fun["Stream_ID"],
                status=df.df_check_status,
                update_time=date2ymdhms(utctime2localtime(df.df_update_date)),
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


def fetch_publishing_fun_data(page, limit, order_by_names):
    """
    获取所有待审核功能
    :param page:
    :param limit:
    :return:
    """
    try:
        pager = Paginator(Device_Fun.objects.filter(df_check_status=_convention.FUN_CHECKING).order_by(order_by_names),
                          int(limit))
        dfs = pager.page(int(page))
        total_count = pager.count
        data = []
        for df in dfs:
            fun = json.loads(df.device_function)
            d = dict(
                id = df.df_id,
                key=df.device_key,
                name=fun["Stream_ID"],
                status=df.df_check_status,
                update_time=date2ymdhms(utctime2localtime(df.df_update_date)),
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