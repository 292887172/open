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
    smoke = [
        {'isControl': 1, 'state': 1, 'time': '2017-08-01 09:20:19', 'name': '开关', 'corpMark': '', 'widget': 'button', 'widget': 'button', 'min': 0, 'max': 1,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '8', 'id': '1', 'Stream_ID': 'POWER'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:50:35', 'name': '风机', 'corpMark': '', 'widget': 'button', 'widget': 'button', 'min': 0, 'max': 4,
         'mxsNum': '5', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '1档', 'data': '1'}, {'desc': '2档', 'data': '2'},
                                {'desc': '3档', 'data': '3'}, {'desc': '4档', 'data': '4'}], 'corpName': '',
         'paramType': 1, 'mxsLength': '8', 'id': '2', 'Stream_ID': 'FAN'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:50:49', 'name': '照明', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 1,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '8', 'id': '3', 'Stream_ID': 'LAMP'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:50:49', 'name': '延时', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 1,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '8', 'id': '4', 'Stream_ID': 'DELAY'}
        ]
    stove = [
        {'isControl': 1, 'state': 1, 'time': '2017-08-01 09:20:19', 'name': '开关', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 1,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '8', 'id': '1', 'Stream_ID': 'POWER'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:50:35', 'name': '风机', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 4,
         'mxsNum': '5', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '1档', 'data': '1'}, {'desc': '2档', 'data': '2'},
                                {'desc': '3档', 'data': '3'}, {'desc': '4档', 'data': '4'}], 'corpName': '',
         'paramType': 1, 'mxsLength': '8', 'id': '2', 'Stream_ID': 'FAN'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:50:49', 'name': '照明', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 1,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '8', 'id': '3', 'Stream_ID': 'LAMP'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:51:10', 'name': '清洗', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 1,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '8', 'id': '4', 'Stream_ID': 'WASH'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:56', 'name': '清洗时间', 'corpMark': 's', 'widget': 'input', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '秒', 'paramType': 1, 'mxsLength': '16', 'id': '5',
         'Stream_ID': 'DISINFECT_DURATION'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:51:40', 'name': '烘干', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 1,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '8', 'id': '6', 'Stream_ID': 'DRY'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:40', 'name': '烘干时间', 'corpMark': 's', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '秒', 'paramType': 1, 'mxsLength': '16', 'id': '7',
         'Stream_ID': 'DRY_DURATION'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '消毒', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 1,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '8', 'id': '8', 'Stream_ID': 'DISINFECT'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:56', 'name': '消毒时间', 'corpMark': 's', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '秒', 'paramType': 1, 'mxsLength': '16', 'id': '9',
         'Stream_ID': 'DISINFECT_DURATION'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:52:23', 'name': '恒温', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 1,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '8', 'id': '10', 'Stream_ID': 'WARM'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:50:49', 'name': '延时', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 1,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '8', 'id': '11', 'Stream_ID': 'DELAY'},
    ]

    oven = [
        {'isControl': 1, 'state': 1, 'time': '2017-08-01 09:20:19', 'name': '开关', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 1,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '8', 'id': '1', 'Stream_ID': 'POWER'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:50:35', 'name': '童锁', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 1,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '8', 'id': '2',  'Stream_ID': 'BODY_LOCK'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:50:49', 'name': '照明', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 1,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '1', 'id': '3', 'Stream_ID': 'LAMP'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:51:10', 'name': '工作模式', 'corpMark': '', 'widget': 'button', 'min': 0,
         'max': 65535, 'mxsNum': '17',
         'mxs': [{'desc': '无选择', 'data': '0'}, {'desc': '快热', 'data': '1'}, {'desc': '烘焙', 'data': '2'},
                 {'desc': '风扇烤', 'data': '3'}, {'desc': '风焙烤', 'data': '4'}, {'desc': '底加热', 'data': '5'},
                 {'desc': '烧烤', 'data': '6'}, {'desc': '强烧烤', 'data': '7'}, {'desc': '增强焙烤', 'data': '8'},
                 {'desc': '蛋糕', 'data': '9'}, {'desc': '面包', 'data': '10'}, {'desc': '肉类', 'data': '11'},
                 {'desc': '披萨', 'data': '12'}, {'desc': '发酵', 'data': '13'}, {'desc': '饼干', 'data': '14'},
                 {'desc': '家禽', 'data': '15'}, {'desc': '保温', 'data': '16'}
                 ],
         'corpName': '', 'paramType': 1, 'mxsLength': '8', 'id': '4', 'Stream_ID': 'MODEL'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '时间下限', 'corpMark': 's', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '秒', 'paramType': 1, 'mxsLength': '16',
         'id': '5', 'Stream_ID': 'TIME_LOWER_LIMIT'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '建议工作时间', 'corpMark': 's', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '秒', 'paramType': 1, 'mxsLength': '16',
         'id': '6', 'Stream_ID': 'SUGGEST_TIME'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '时间上限', 'corpMark': 's', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '秒', 'paramType': 1, 'mxsLength': '16',
         'id': '7', 'Stream_ID': 'TIME_UPPER_LIMIT'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:51:40', 'name': '工作时间', 'corpMark': 's', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '秒', 'paramType': 1, 'mxsLength': '16',
         'id': '8', 'Stream_ID': 'WORK_TIME'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:51:40', 'name': '剩余时间', 'corpMark': 's', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '秒', 'paramType': 1, 'mxsLength': '16',
         'id': '9', 'Stream_ID': 'REMAIN_TIME'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '温度下限', 'corpMark': '℃', 'widget': 'input', 'min': 0,
         'max': 255, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 1, 'mxsLength': '8',
         'id': '10', 'Stream_ID': 'TEMPE_LOWER_LIMIT'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '建议温度', 'corpMark': '℃', 'widget': 'input', 'min': 0,
         'max': 255, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 1, 'mxsLength': '8',
         'id': '11', 'Stream_ID': 'SUGGEST_TEMPE'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '温度上限', 'corpMark': '℃', 'widget': 'input', 'min': 0,
         'max': 255, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 1, 'mxsLength': '8',
         'id': '12', 'Stream_ID': 'TEMPE_UPPER_LIMIT'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '当前温度', 'corpMark': '℃', 'widget': 'input', 'min': 0,
         'max': 255, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 1, 'mxsLength': '8',
         'id': '13', 'Stream_ID': 'CUR_TEMPE'},
    ]
    steam = [
        {'isControl': 1, 'state': 1, 'time': '2017-08-01 09:20:19', 'name': '开关', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 1,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '8', 'id': '1', 'Stream_ID': 'POWER'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:50:35', 'name': '童锁', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 1,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '8', 'id': '2', 'Stream_ID': 'BODY_LOCK'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:50:49', 'name': '照明', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 1,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '1', 'id': '3', 'Stream_ID': 'LAMP'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:51:10', 'name': '工作模式', 'corpMark': '', 'widget': 'button', 'min': 0,
         'max': 65535, 'mxsNum': '13',
         'mxs': [{'desc': '无选择', 'data': '0'}, {'desc': '肉类', 'data': '1'}, {'desc': '鱼类', 'data': '2'},
                 {'desc': '蛋类', 'data': '3'}, {'desc': '蔬菜', 'data': '4'}, {'desc': '米饭', 'data': '5'},
                 {'desc': '面食', 'data': '6'}, {'desc': '解冻', 'data': '7'}, {'desc': '发酵', 'data': '8'},
                 {'desc': '水果', 'data': '9'}, {'desc': '杀菌', 'data': '10'}, {'desc': '高温', 'data': '11'},
                 {'desc': '清洗', 'data': '12'}
                 ],
         'corpName': '', 'paramType': 1, 'mxsLength': '8', 'id': '4', 'Stream_ID': 'MODEL'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '时间下限', 'corpMark': 's', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '秒', 'paramType': 1, 'mxsLength': '16',
         'id': '5', 'Stream_ID': 'TIME_LOWER_LIMIT'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '建议工作时间', 'corpMark': 's', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '秒', 'paramType': 1, 'mxsLength': '16',
         'id': '6', 'Stream_ID': 'SUGGEST_TIME'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '时间上限', 'corpMark': 's', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '秒', 'paramType': 1, 'mxsLength': '16',
         'id': '7', 'Stream_ID': 'TIME_UPPER_LIMIT'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:51:40', 'name': '工作时间', 'corpMark': 's', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '秒', 'paramType': 1, 'mxsLength': '16',
         'id': '8', 'Stream_ID': 'WORK_TIME'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:51:40', 'name': '剩余时间', 'corpMark': 's', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '秒', 'paramType': 1, 'mxsLength': '16',
         'id': '9', 'Stream_ID': 'REMAIN_TIME'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '温度下限', 'corpMark': '℃', 'widget': 'input', 'min': 0,
         'max': 255, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 1, 'mxsLength': '8',
         'id': '10', 'Stream_ID': 'TEMPE_LOWER_LIMIT'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '建议温度', 'corpMark': '℃', 'widget': 'input', 'min': 0,
         'max': 255, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 1, 'mxsLength': '8',
         'id': '11', 'Stream_ID': 'SUGGEST_TEMPE'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '温度上限', 'corpMark': '℃', 'widget': 'input', 'min': 0,
         'max': 255, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 1, 'mxsLength': '8',
         'id': '12', 'Stream_ID': 'TEMPE_UPPER_LIMIT'},
        {'isControl': 0, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '当前温度', 'corpMark': '℃', 'widget': 'input', 'min': 0,
         'max': 255, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 1, 'mxsLength': '8',
         'id': '13', 'Stream_ID': 'CUR_TEMPE'},
    ]
    fridge = [
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '智能模式', 'corpMark': '', 'widget': 'button', 'min': 0,
         'max': 1, 'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '',
         'paramType': 1, 'mxsLength': '8', 'id': '1', 'Stream_ID': 'SMART_MODE'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '速冻模式', 'corpMark': '', 'widget': 'button', 'min': 0,
         'max': 1, 'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '',
         'paramType': 1, 'mxsLength': '8', 'id': '2', 'Stream_ID': 'FAST_FREMODE'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '速冷模式', 'corpMark': '', 'widget': 'button', 'min': 0,
         'max': 1, 'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '',
         'paramType': 1, 'mxsLength': '8', 'id': '3', 'Stream_ID': 'FAST_FRIMODE'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '变温室温度', 'corpMark': '℃', 'widget': 'input', 'min': -20,
         'max': 20, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 1, 'mxsLength': '8',
         'id': '4', 'Stream_ID': 'VAR_TEMP'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '冷冻室温度', 'corpMark': '℃', 'widget': 'input', 'min': -20,
         'max': 20, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 1, 'mxsLength': '8',
         'id': '5', 'Stream_ID': 'FRE_TEMP'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '冷藏室温度', 'corpMark': '℃', 'widget': 'input', 'min': -20,
         'max': 20, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 1, 'mxsLength': '8',
         'id': '6', 'Stream_ID': 'FRI_TEMP'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '变温室开关', 'corpMark': '', 'widget': 'button', 'min': 0,
         'max': 1, 'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '',
         'paramType': 1, 'mxsLength': '8', 'id': '7', 'Stream_ID': 'VAR_POWER'},
        {'isControl': 1, 'state': 1, 'time': '2017-07-27 16:52:12', 'name': '冷冻室开关', 'corpMark': '', 'widget': 'button', 'min': 0,
         'max': 1, 'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '',
         'paramType': 1, 'mxsLength': '8', 'id': '8', 'Stream_ID': 'FRE_POWER'},
    ]

    if val == 1:
        return smoke
    elif val == 2:
        return stove
    elif val == 6:
        return fridge
    elif val == 11:
        return oven
    elif val == 20:
        return steam
    else:
        return []
