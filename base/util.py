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


def get_app_default_logo(value):
    category = {1: 'http://storage.56iq.net/group1/M00/27/79/CgoKQ1ok7EqAV4cjAAAJEEiqGrI732.png',
                2: 'http://storage.56iq.net/group1/M00/27/79/CgoKQ1ok6-KAJ2WKAAAHByAZqnw209.png',
                6: 'http://storage.56iq.net/group1/M00/27/79/CgoKQ1ok6sSAB3aaAAAGU1GU_50524.png',
                11: 'http://storage.56iq.net/group1/M00/27/B6/CgoKQ1onfHuAFkXQAAAGs5b60BI117.png',
                20: 'http://storage.56iq.net/group1/M00/27/B6/CgoKQ1onfKmACVD1AAAGY2NWOAc179.png',
                25: 'http://storage.56iq.net/group1/M00/27/B6/CgoKQ1onfCKADlDtAAAHmuiIXls002.png',
                26: 'http://storage.56iq.net/group1/M00/27/79/CgoKQ1ok65uAE6WvAAAJoXjpBUE995.png',
                27: 'http://storage.56iq.net/group1/M00/27/79/CgoKQ1ok7CiAad4FAAAIZ6wuFKI298.png'}
    try:
        app_logo = category.get(value)
        return app_logo
    except Exception as e:
        print("获取默认app_logo失败",e)
        return ''


def gen_app_default_conf(val):
    smoke = [
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-08-01 09:20:19', 'name': '开关', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '1', 'Stream_ID': 'POWER','toSwitch':'0','isFunction':'1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:50:35', 'name': '风机', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '5', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '1档', 'data': '1'}, {'desc': '2档', 'data': '2'},
                                {'desc': '3档', 'data': '3'}, {'desc': '4档', 'data': '4'}], 'corpName': '',
         'paramType': 4, 'mxsLength': '8', 'id': '2', 'Stream_ID': 'FAN','toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:50:49', 'name': '照明', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '3', 'Stream_ID': 'LAMP','toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:50:49', 'name': '延时', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '4', 'Stream_ID': 'DELAY','toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-08-01 09:20:19', 'name': '工作状态', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '5', 'Stream_ID': 'STATE', 'toSwitch': '0','isFunction': '1'},
        ]
    stove = [
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-08-01 09:20:19', 'name': '开关', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '1', 'Stream_ID': 'POWER','toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:50:35', 'name': '风机', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '5', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '1档', 'data': '1'}, {'desc': '2档', 'data': '2'},
                                {'desc': '3档', 'data': '3'}, {'desc': '4档', 'data': '4'}], 'corpName': '',
         'paramType': 4, 'mxsLength': '8', 'id': '2', 'Stream_ID': 'FAN','toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:50:49', 'name': '照明', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '3', 'Stream_ID': 'LAMP','toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:51:10', 'name': '清洗', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '4', 'Stream_ID': 'WASH','toSwitch': '0','isFunction': '1'},
        {'isControl': 0, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:56', 'name': '清洗时间', 'corpMark': 's', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '秒', 'paramType': 4, 'mxsLength': '16', 'id': '5',
         'Stream_ID': 'WASH_DURATION','toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:51:40', 'name': '烘干', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '6', 'Stream_ID': 'DRY','toSwitch': '0','isFunction': '1'},
        {'isControl': 0, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:40', 'name': '烘干时间', 'corpMark': 's', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '秒', 'paramType': 4, 'mxsLength': '16', 'id': '7',
         'Stream_ID': 'DRY_DURATION','toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '消毒', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '8', 'Stream_ID': 'DISINFECT','toSwitch': '0','isFunction': '1'},
        {'isControl': 0, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:56', 'name': '消毒时间', 'corpMark': 's', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '秒', 'paramType': 4, 'mxsLength': '16', 'id': '9',
         'Stream_ID': 'DISINFECT_DURATION','toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:23', 'name': '恒温', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '10', 'Stream_ID': 'WARM','toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:50:49', 'name': '延时', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '11', 'Stream_ID': 'DELAY','toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-08-01 09:20:19', 'name': '工作状态', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '12', 'Stream_ID': 'STATE', 'toSwitch': '0','isFunction': '1'},
    ]

    oven = [
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-08-01 09:20:19', 'name': '开关', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '1', 'id': '1', 'Stream_ID': 'POWER', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:50:35', 'name': '童锁', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '1', 'id': '2',  'Stream_ID': 'BODY_LOCK', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:50:35', 'name': '风机', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '',
         'paramType': 1, 'mxsLength': '1', 'id': '3', 'Stream_ID': 'FAN','toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:50:49', 'name': '照明', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '1', 'id': '4', 'Stream_ID': 'LAMP', 'toSwitch': '0','isFunction': '1'},

        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-08-01 09:20:19', 'name': '工作状态', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 15,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '4', 'id': '5', 'Stream_ID': 'STATE', 'toSwitch': '0','isFunction': '1'},

        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:51:10', 'name': '模式', 'corpMark': '', 'widget': 'button', 'min': 0,
         'max': 65535, 'mxsNum': '21',
         'mxs': [{'desc': '自定义模式', 'data': '0'}, {'desc': '顶部加热', 'data': '1','advice':'建议使用上电热管'}, {'desc': '底加热', 'data': '2','advice':'建议使用下电热管'},
                 {'desc': '顶部风扇烤', 'data': '3','advice':'建议使用上加热管+风扇'}, {'desc': '底部风扇烤', 'data': '4','advice':'建议使用下电热管+风扇'}, {'desc': '背部风扇考', 'data': '5','advice':'建议使用上下电热管+风扇'},
                 {'desc': '快热', 'data': '6','advice':'建议使用上下电热管'}, {'desc': '烤鸡', 'data': '7','advice':'建议使用上下电热管+风机+转插'}, {'desc': '嫩烤', 'data': '8','advice':'建议s还有上下电热管+风机+蒸汽'},
                 {'desc': '4D烤', 'data': '9','advice':'建议使用上下电热管+风机+蒸汽+转插'}, {'desc': '蛋糕', 'data': '10','advice':'建议使用上电热管+风扇'}, {'desc': '烧烤风扇', 'data': '11','advice':'建议使用上下电热管+风扇+转插'},
                 {'desc': '节能模式', 'data': '12','advice':'建议使用下电热管'}, {'desc': '披萨', 'data': '13','advice':'建议使用上下电热管+风扇'}, {'desc': '烘焙', 'data': '14','advice':'建议使用上电热管'},
                 {'desc': '肉类', 'data': '15','advice':'建议使用上下电热管'}, {'desc': '饼干', 'data': '16','advice':'建议使用上电热管'},{'desc': '发酵模式', 'data': '17','advice':'建议使用下电热管+风扇'},
                 {'desc': '暖盘模式', 'data': '18','advice':'建议使用下电热管'},{'desc': '解冻模式', 'data': '19','advice':'建议使用下电热管+风扇'},{'desc': '保温', 'data': '20','advice':'建议使用上电热管'}
                 ],
         'corpName': '', 'paramType': 4, 'mxsLength': '16', 'id': '6', 'Stream_ID': 'MODEL', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 0, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '设定工作时间', 'corpMark': 'm', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '分', 'paramType': 4, 'mxsLength': '16',
         'id': '7', 'Stream_ID': 'SET_WORK_TIME', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 0, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '剩余工作时间', 'corpMark': 'm', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '分', 'paramType': 4, 'mxsLength': '16',
         'id': '8', 'Stream_ID': 'REMAIN_WORK_TIME', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 0, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '预约时间', 'corpMark': 'm', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '分', 'paramType': 4, 'mxsLength': '16',
         'id': '9', 'Stream_ID': 'APPOINT_TIME', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:51:40', 'name': '预约剩余时间', 'corpMark': 'm', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '分', 'paramType': 4, 'mxsLength': '16',
         'id': '10', 'Stream_ID': 'REMAIN_APPOINT_TIME', 'toSwitch': '0','isFunction': '1'},

        {'isControl': 0, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '设定温度', 'corpMark': '℃', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 4, 'mxsLength': '16',
         'id': '11', 'Stream_ID': 'SET_TEMPE', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 0, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '当前温度', 'corpMark': '℃', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 4, 'mxsLength': '16',
         'id': '12', 'Stream_ID': 'CUR_TEMPE', 'toSwitch': '0','isFunction': '1'},

        {'isControl': 0, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '肉针温度', 'corpMark': '℃', 'widget': 'input','min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 4, 'mxsLength': '16',
         'id': '13', 'Stream_ID': 'MEAT_TEMPE', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 0, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '故障', 'corpMark': '', 'widget': 'input',
         'mxsNum': '0', 'mxs': [], 'corpName': '', 'paramType': 3, 'mxsLength': '8',
         'id': '14', 'Stream_ID': 'ERROR', 'toSwitch': '0','isFunction': '1'},
    ]
    steam = [
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-08-01 09:20:19', 'name': '开关', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 3,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '2', 'id': '1', 'Stream_ID': 'POWER', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:50:35', 'name': '童锁', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '1', 'id': '2',  'Stream_ID': 'BODY_LOCK', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:50:49', 'name': '照明', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '', 'paramType': 1,
         'mxsLength': '1', 'id': '3', 'Stream_ID': 'LAMP', 'toSwitch': '0','isFunction': '1'},

        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-08-01 09:20:19', 'name': '工作状态', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 15,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '4', 'id': '4', 'Stream_ID': 'STATE', 'toSwitch': '0','isFunction': '1'},

        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:51:10', 'name': '模式', 'corpMark': '', 'widget': 'button', 'min': 0,
         'max': 65535, 'mxsNum': '13',
         'mxs': [{'desc': '自定义', 'data': '0'}, {'desc': '肉类', 'data': '1'}, {'desc': '鱼类', 'data': '2'},
                 {'desc': '蛋类', 'data': '3'}, {'desc': '蔬菜', 'data': '4'}, {'desc': '米饭', 'data': '5'},
                 {'desc': '面食', 'data': '6'}, {'desc': '水果', 'data': '7'}, {'desc': '杀菌', 'data': '8'},
                 {'desc': '解冻', 'data': '9'}, {'desc': '发酵', 'data': '10'}, {'desc': '保温', 'data': '11'},
                 {'desc': '清洗', 'data': '12'}
                 ],
         'corpName': '', 'paramType': 4, 'mxsLength': '16', 'id': '5', 'Stream_ID': 'MODEL', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 0, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '设定工作时间', 'corpMark': 'm', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '分', 'paramType': 4, 'mxsLength': '16',
         'id': '6', 'Stream_ID': 'SET_WORK_TIME', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 0, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '剩余工作时间', 'corpMark': 'm', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '分', 'paramType': 4, 'mxsLength': '16',
         'id': '7', 'Stream_ID': 'REMAIN_WORK_TIME', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 0, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '预约时间', 'corpMark': 'm', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '分', 'paramType': 4, 'mxsLength': '16',
         'id': '8', 'Stream_ID': 'APPOINT_TIME', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:51:40', 'name': '预约剩余时间', 'corpMark': 'm', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '分', 'paramType': 4, 'mxsLength': '16',
         'id': '9', 'Stream_ID': 'REMAIN_APPOINT_TIME', 'toSwitch': '0','isFunction': '1'},

        {'isControl': 0, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '设定温度', 'corpMark': '℃', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 4, 'mxsLength': '16',
         'id': '10', 'Stream_ID': 'SET_TEMPE', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 0, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '当前温度', 'corpMark': '℃', 'widget': 'input', 'min': 0,
         'max': 65535, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 4, 'mxsLength': '16',
         'id': '11', 'Stream_ID': 'CUR_TEMPE', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 0, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '故障', 'corpMark': '', 'widget': 'input',
         'mxsNum': '0', 'mxs': [], 'corpName': '', 'paramType': 3, 'mxsLength': '8',
         'id': '12', 'Stream_ID': 'ERROR', 'toSwitch': '0','isFunction': '1'},
    ]
    fridge = [
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-08-01 09:20:19', 'name': '开关', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '1', 'Stream_ID': 'POWER', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '智能模式', 'corpMark': '', 'widget': 'button', 'min': 0,
         'max': 255, 'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '',
         'paramType': 4, 'mxsLength': '8', 'id': '2', 'Stream_ID': 'SMART_MODE', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '速冻模式', 'corpMark': '', 'widget': 'button', 'min': 0,
         'max': 255, 'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '',
         'paramType': 4, 'mxsLength': '8', 'id': '3', 'Stream_ID': 'FAST_FREMODE', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '速冷模式', 'corpMark': '', 'widget': 'button', 'min': 0,
         'max': 255, 'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '',
         'paramType': 4, 'mxsLength': '8', 'id': '4', 'Stream_ID': 'FAST_FRIMODE', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '变温室温度', 'corpMark': '℃', 'widget': 'input', 'min': -20,
         'max': 255, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 4, 'mxsLength': '8',
         'id': '5', 'Stream_ID': 'VAR_TEMP', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '冷冻室温度', 'corpMark': '℃', 'widget': 'input', 'min': -20,
         'max': 255, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 4, 'mxsLength': '8',
         'id': '6', 'Stream_ID': 'FRE_TEMP', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '冷藏室温度', 'corpMark': '℃', 'widget': 'input', 'min': -20,
         'max': 255, 'mxsNum': '0', 'mxs': [], 'corpName': '摄氏度', 'paramType': 4, 'mxsLength': '8',
         'id': '7', 'Stream_ID': 'FRI_TEMP', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '变温室开关', 'corpMark': '', 'widget': 'button', 'min': 0,
         'max': 255, 'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '',
         'paramType': 4, 'mxsLength': '8', 'id': '8', 'Stream_ID': 'VAR_POWER', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-07-27 16:52:12', 'name': '冷冻室开关', 'corpMark': '', 'widget': 'button', 'min': 0,
         'max': 255, 'mxsNum': '2', 'mxs': [{'desc': '关', 'data': '0'}, {'desc': '开', 'data': '1'}], 'corpName': '',
         'paramType': 4, 'mxsLength': '8', 'id': '9', 'Stream_ID': 'FRE_POWER', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-08-01 09:20:19', 'name': '工作状态', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '10', 'Stream_ID': 'STATE', 'toSwitch': '0','isFunction': '1'},
    ]
    small_oven = [
    {
        "corpMark": "",
        "time": "2017-12-04 15:40:34",
        "Stream_ID": "POWER",
        "corpName": "",
        "min": 0,
        "mxs": [
            {
                "data": "0",
                "desc": "关"
            },
            {
                "data": "1",
                "desc": "开"
            }
        ],
        "isControl": 1,
        "state": 1,'isDisplay':1,'isCloudMenu':0,'isShow':0,
        "max": 255,
        "mxsLength": "8",
        "mxsNum": "2",
        "widget": "button",
        "name": "电源",
        "id": "1",
        'paramType': 4,
        'toSwitch': '0',
        'isFunction': '1'
    },
    {
        "corpMark": "",
        "time": "2017-12-04 15:40:41",
        "Stream_ID": "FREEZE",
        "corpName": "",
        "min": 0,
        "isControl": 1,
        "mxs": [
            {
                "data": "0",
                "desc": "关"
            },
            {
                "data": "1",
                "desc": "开"
            }
        ],
        "state": 1, 'isDisplay': 1, 'isCloudMenu': 0, 'isShow': 0,
        "max": 255,
        "mxsLength": "8",
        "mxsNum": "2",
        "widget": "button",
        "name": "解冻",
        "id": "2",
        'paramType': 4,
        'toSwitch': '0',
        'isFunction': '1'
    },
    {
        "corpMark": "",
        "min": 0,
        "state": 1,'isDisplay':1,'isCloudMenu':0,'isShow':0,
        "mxsNum": "2",
        "widget": "button",
        "name": "蛋糕",
        "time": "2017-12-04 15:40:47",
        "Stream_ID": "CAKE",
        "corpName": "",
        "mxs": [
            {
                "data": "0",
                "desc": "关"
            },
            {
                "data": "1",
                "desc": "开"
            }
        ],
        "isControl": 1,
        "max": 255,
        "mxsLength": "8",
        "id": "3",
        'paramType': 4,
        'toSwitch': '0',
        'isFunction': '1'
    },
    {
        "corpMark": "",
        "time": "2017-12-04 15:28:34",
        "Stream_ID": "BREAD",
        "corpName": "",
        "min": 0,
        "mxs": [
            {
                "data": "0",
                "desc": "关"
            },
            {
                "data": "1",
                "desc": "开"
            }
        ],
        "isControl": 1,
        "state": 1,'isDisplay':1,'isCloudMenu':0,'isShow':0,
        "max": 255,
        "mxsLength": "8",
        "mxsNum": "2",
        "widget": "button",
        "name": "面包",
        "id": "4",
        'paramType': 4,
        'toSwitch': '0',
        'isFunction': '1'
    },
    {
        "corpMark": "",
        "time": "2017-12-04 15:29:12",
        "Stream_ID": "poultry",
        "corpName": "",
        "min": 0,
        "isControl": 1,
        "mxs": [
            {
                "data": "0",
                "desc": "关"
            },
            {
                "data": "1",
                "desc": "开"
            }
        ],
        "state": 1,'isDisplay':1,'isCloudMenu':0,'isShow':0,
        "max": 255,
        "mxsLength": "8",
        "mxsNum": "2",
        "widget": "button",
        "name": "家禽",
        "id": "5",
        'paramType': 4,
        'toSwitch': '0',
        'isFunction': '1'
    },
    {
        "corpMark": "",
        "time": "2017-12-04 15:30:27",
        "Stream_ID": "bake",
        "corpName": "",
        "min": 0,
        "mxs": [
            {
                "data": "0",
                "desc": "关"
            },
            {
                "data": "1",
                "desc": "开"
            }
        ],
        "isControl": 1,
        "state": 1,'isDisplay':1,'isCloudMenu':0,'isShow':0,
        "max": 255,
        "mxsLength": "8",
        "mxsNum": "2",
        "widget": "button",
        "name": "烘烤",
        "id": "6",
        'paramType': 4,
        'toSwitch': '0',
        'isFunction': '1'
    },
    {
        "corpMark": "",
        "time": "2017-12-04 15:30:46",
        "Stream_ID": "fast_heat",
        "corpName": "",
        "min": 0,
        "isControl": 1,
        "mxs": [
            {
                "data": "0",
                "desc": "关"
            },
            {
                "data": "1",
                "desc": "开"
            }
        ],
        "state": 1,'isDisplay':1,'isCloudMenu':0,'isShow':0,
        "max": 255,
        "mxsLength": "8",
        "mxsNum": "2",
        "widget": "button",
        "name": "快热",
        "id": "7",
        'paramType': 4,
        'toSwitch': '0',
        'isFunction': '1'
    },
    {
        "corpMark": "",
        "time": "2017-12-04 15:31:24",
        "Stream_ID": "fermentation",
        "corpName": "",
        "min": 0,
        "mxs": [
            {
                "data": "0",
                "desc": "关"
            },
            {
                "data": "1",
                "desc": "开"
            }
        ],
        "isControl": 1,
        "state": 1,'isDisplay':1,'isCloudMenu':0,'isShow':0,
        "max": 255,
        "mxsLength": "8",
        "mxsNum": "2",
        "widget": "button",
        "name": "发酵",
        "id": "8",
        'paramType': 4,
        'toSwitch': '0',
        'isFunction': '1'
    },
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-08-01 09:20:19', 'name': '工作状态', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '9', 'Stream_ID': 'STATE', 'toSwitch': '0','isFunction': '1'},
]
    other = [
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-08-01 09:20:19', 'name': '开关', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '1', 'Stream_ID': 'POWER', 'toSwitch': '0','isFunction': '1'},
        {'isControl': 1, 'state': 1, 'isDisplay':1,'isCloudMenu':0,'isShow':0, 'time': '2017-08-01 09:20:19', 'name': '工作状态', 'corpMark': '', 'widget': 'button', 'min': 0, 'max': 255,
         'mxsNum': '2', 'mxs': [{'desc': '开', 'data': '1'}, {'desc': '关', 'data': '0'}], 'corpName': '', 'paramType': 4,
         'mxsLength': '8', 'id': '2', 'Stream_ID': 'STATE', 'toSwitch': '0','isFunction': '1'},
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
    elif val == 27:
        return small_oven
    else:
        return other
