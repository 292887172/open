# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'achais'

import logging

from django.core.paginator import Paginator
from django.db.models import Q

from base.connection import Redis3_ClientDB6
from base.convert import date2ymdhms
from common.code import ResponseCode
from model.center.api import Api

_cache_key = ResponseCode()


class ApiHandler(object):
    """
    AppApi处理类
    """

    def __init__(self, level, group):
        """
        注入筛选的等级和分组
        :param level:
        :param group:
        :return:
        """
        self._api_list = None
        self._api_list = Api.objects.filter(
            Q(api_type=0) |
            Q(api_group=0, api_level__lte=level) |
            Q(api_group=group, api_level__lte=level),
            api_is_forbid=0
        )

    @property
    def api_list(self):
        """
        获取所有筛选出来的API接口列表
        :return:
        """
        return self._api_list


def add_api(api_name, api_url, api_type, api_method, api_params, api_return, api_describe, api_doc_url, api_action_url,
            api_classify, api_function, api_level, api_group, api_invoke_total, api_port=80):
    """
    添加一条API接口
    :param api_name:
    :param api_url:
    :param api_type:
    :param api_method:
    :param api_params:
    :param api_return:
    :param api_describe:
    :param api_doc_url:
    :param api_action_url:
    :param api_port:
    :param api_classify:
    :param api_function:
    :param api_level:
    :param api_group:
    :param api_invoke_total:
    :return:
    """
    try:
        api = Api(api_name=api_name, api_url=api_url, api_type=api_type, api_request_type=api_method,
                  api_params=api_params, api_return=api_return, api_describe=api_describe, api_doc_url=api_doc_url,
                  api_action_url=api_action_url, api_classify=api_classify, api_function=api_function,
                  api_level=int(api_level), api_group=int(api_group), api_invoke_total=int(api_invoke_total),
                  api_port=int(api_port))
        api.save()
        return True
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def update_api(api_id, api_name, api_url, api_type, api_method, api_params, api_return, api_describe, api_doc_url,
               api_action_url, api_classify, api_function, api_level, api_group, api_invoke_total, api_port=80):
    """
    更新API接口
    :param api_id:
    :param api_name:
    :param api_url:
    :param api_type:
    :param api_method:
    :param api_params:
    :param api_return:
    :param api_describe:
    :param api_doc_url:
    :param api_action_url:
    :param api_port:
    :param api_classify:
    :param api_function:
    :param api_level:
    :param api_group:
    :param api_invoke_total:
    :return:
    """
    try:
        Api.objects.filter(api_id=api_id).update(api_name=api_name, api_url=api_url, api_type=api_type,
                                                 api_request_type=api_method,
                                                 api_params=api_params, api_return=api_return,
                                                 api_describe=api_describe, api_doc_url=api_doc_url,
                                                 api_action_url=api_action_url, api_classify=api_classify,
                                                 api_function=api_function,
                                                 api_level=int(api_level), api_group=int(api_group),
                                                 api_invoke_total=int(api_invoke_total),
                                                 api_port=int(api_port))
        return True
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def del_api(api_id):
    """
    删除接口
    :param api_id:
    :return:
    """
    try:
        api = Api.objects.get(api_id=int(api_id))
        api.delete()
        return True
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def fetch_api_list_data(page, limit, order_by_names):
    try:
        pager = Paginator(Api.objects.all().order_by(order_by_names),
                          int(limit))
        api_list = pager.page(int(page))
        total_count = pager.count
        data = []
        for api in api_list:
            d = dict(
                id=api.api_id,
                name=api.api_name,
                method=api.api_request_type.upper() if api.api_request_type else "",
                describe=api.api_describe,
                doc=api.api_doc_url,
                createtime=date2ymdhms(api.api_create_date)
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


def fetch_api_data(api_id):
    """
    获取接口信息
    :param api_id:
    :return:
    """
    try:
        api = Api.objects.get(api_id=int(api_id))
        if api:
            return api
        else:
            return None
    except Exception as e:
        logging.getLogger("").error(e)
        return None


def gen_group_key(*args):
    return ":".join(str(_) for _ in args)


def remove_control_id(device_id):
    r = Redis3_ClientDB6
    try:
        r.delete(gen_group_key(_cache_key.DEVICE_CONTROL_PREFIX, device_id.upper()))
    except Exception as e:
        pass


def remove_conf_prefix(key):
    r = Redis3_ClientDB6
    try:
        r.delete(gen_group_key(_cache_key.DEVICE_CONF_PREFIX, key))
    except Exception as e:
        print(e)
        pass
