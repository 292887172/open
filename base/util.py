# !/usr/bin/env python
# -*- coding: utf-8 -*-

from base.convert import int2b36
from base.crypto import sha1_en

import time
import random
import string

__author__ = 'achais'

UNICODE_ASCII_CHARACTERS = string.ascii_letters + string.digits


def gen_cache_key(*args):
    """
    生成缓存前缀
    :param args:
    :return:
    """
    return "_".join(str(_) for _ in args)


def gen_cron_id(*args):
    """
    生成定时任务的编号前缀
    :param args:
    :return:
    """
    return "_".join(str(_) for _ in args)


def random_ascii_string(length):
    """
    随机字符串(指定长度)
    :param length:
    :return:
    """
    return ''.join(random.choice(UNICODE_ASCII_CHARACTERS) for _ in range(0, length))


def random_ascii_digits(length):
    """
    随机数字(指定长度)
    :param length:
    :return:
    """
    return "".join(random.choice(string.digits) for _ in range(0, length))


def gen_app_uuid():
    """
    随机生成应用编号app_uuid(36进制)
    :return:
    """
    return int2b36(int(time.time()))


def gen_app_app_id():
    """
    随机生成应用调用API接口的app_id
    :return:
    """
    app_app_id = "53" + random_ascii_string(16)
    return app_app_id


def gen_app_app_secret():
    """
    随机生成应用调用API接口的app_secret
    :return:
    """
    app_secret = random_ascii_string(32)
    return app_secret


def gen_app_access_token():
    """
    随机生成应用调用API接口的access_token
    :return:
    """
    access_token = random_ascii_string(64) + "_" + sha1_en(int(time.time()))
    return access_token


def gen_app_default_conf(val):
    hood = [{'isControl': 1, 'state': '0', 'time': '2017-07-27 16:50:35', 'name': '风机', 'corpMark': '', 'min': 0, 'max': 15,
      'mxs': [{'desc': 'u5173', 'data': '0'}, {'desc': '1u6863', 'data': '1'}, {'desc': '2u6863', 'data': '2'},
              {'desc': '3u6863', 'data': '3'}], 'corpName': '', 'paramType': 1, 'mxsLength': '4', 'id': '2',
      'Stream_ID': 'FAN'},
     {'isControl': 1, 'state': '0', 'time': '2017-07-27 16:50:49', 'name': '照明', 'corpMark': '', 'min': 0, 'max': 1,
      'mxs': [{'desc': 'u5173', 'data': '0'}, {'desc': 'u5f00', 'data': '1'}], 'corpName': '', 'paramType': 1,
      'mxsLength': '2', 'id': '3', 'Stream_ID': 'LAMP'},
     {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:51:10', 'name': '清洗', 'corpMark': '', 'min': 0, 'max': 1,
      'mxs': [{'desc': 'u5173', 'data': '0'}, {'desc': 'u5f00', 'data': '1'}], 'corpName': '', 'paramType': 1,
      'mxsLength': '2', 'id': '4', 'Stream_ID': 'WASH'},
     {'isControl': 1, 'state': 0, 'time': '2017-07-27 16:51:40', 'name': '烘干', 'corpMark': '', 'min': 0, 'max': 1,
      'mxs': [{'desc': 'u5173', 'data': '0'}, {'desc': 'u5f00', 'data': '1'}, {'desc': 'u6682u505c', 'data': '1'}],
      'corpName': '', 'paramType': 1, 'mxsLength': '3', 'id': '5', 'Stream_ID': 'DRY'},
     {'isControl': 1, 'state': 0, 'time': '2017-07-27 16:52:12', 'name': '消毒', 'corpMark': '', 'min': 0, 'max': 1,
      'mxs': [{'desc': 'u5173', 'data': '0'}, {'desc': 'u5f00', 'data': '1'}, {'desc': 'u6682u505c', 'data': '1'}],
      'corpName': '', 'paramType': 1, 'mxsLength': '3', 'id': '6', 'Stream_ID': 'DISINFECT'},
     {'isControl': 1, 'state': '0', 'time': '2017-07-27 16:52:23', 'name': '恒温', 'corpMark': '', 'min': 0, 'max': 1,
      'mxs': [{'desc': 'u5173', 'data': '0'}, {'desc': 'u5f00', 'data': '1'}], 'corpName': '', 'paramType': 1,
      'mxsLength': '2', 'id': '7', 'Stream_ID': 'WARM'},
     {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:52:40', 'name': '烘干时间', 'corpMark': 's', 'min': 0,
      'max': 65535, 'mxs': [], 'corpName': 'u79d2', 'paramType': 1, 'mxsLength': '0', 'id': '8',
      'Stream_ID': 'DRY_DURATION'},
     {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:52:56', 'name': '消毒时间', 'corpMark': 's', 'min': 0,
      'max': 65535, 'mxs': [], 'corpName': 'u79d2', 'paramType': 1, 'mxsLength': '0', 'id': '9',
      'Stream_ID': 'DISINFECT_DURATION'},
     {'isControl': 1, 'state': 0, 'time': '2017-08-01 09:20:19', 'name': '开关', 'corpMark': '', 'min': 0, 'max': 1,
      'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 1, 'mxsLength': '2',
      'id': '1', 'Stream_ID': 'POWER'}]

    oven = [{'isControl': 1, 'state': '0', 'time': '2017-07-27 16:50:35', 'name': '童锁', 'corpMark': '', 'min': 0, 'max': 1,
      'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1, 'mxsLength': '1', 'id': '2',
      'Stream_ID': 'BODYLOCK'},
     {'isControl': 1, 'state': '0', 'time': '2017-07-27 16:50:49', 'name': '照明', 'corpMark': '', 'min': 0, 'max': 1,
      'mxs': [{'desc': 'u5173', 'data': '0'}, {'desc': 'u5f00', 'data': '1'}], 'corpName': '', 'paramType': 1,
      'mxsLength': '1', 'id': '3', 'Stream_ID': 'LAMP'},
     {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:51:10', 'name': '工作模式', 'corpMark': '', 'min': 0, 'max': 65535,
      'mxs': [], 'corpName': '', 'paramType': 1, 'mxsLength': '16', 'id': '4', 'Stream_ID': 'MODEL'},
     {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:51:40', 'name': '工作时间', 'corpMark': 's', 'min': 0, 'max': 65535,
      'mxs': [], 'corpName': '秒', 'paramType': 1, 'mxsLength': '16', 'id': '5', 'Stream_ID': 'WORK_TIME'},
     {'isControl': 0, 'state': 0, 'time': '2017-07-27 16:52:12', 'name': '当前温度', 'corpMark': '℃', 'min': 0, 'max': 255,
      'mxs': [], 'corpName': '摄氏度', 'paramType': 1, 'mxsLength': '8', 'id': '6', 'Stream_ID': 'CURTEMPE'},
     {'isControl': 1, 'state': 0, 'time': '2017-08-01 09:20:19', 'name': '开关', 'corpMark': '', 'min': 0, 'max': 1,
      'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 1, 'mxsLength': '2',
      'id': '1', 'Stream_ID': 'POWER'}]

    if val == '1':
        return hood
    else:
        return oven
