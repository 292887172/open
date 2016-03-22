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
