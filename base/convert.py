# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'achais'

import string
import datetime


def int2b36(n):
    """
    10进制转36进制
    :param n:
    :return:
    """
    loop = string.digits + string.ascii_uppercase
    a = ""
    while n != 0:
        a += loop[n % 36]
        n //= 36
    return a[::-1]


def utctime2localtime(d):
    """
    utc时间转当地时间
    :param d:
    :return:
    """
    try:
        return d + datetime.timedelta(hours=8)
    except:
        return None


def localtime2utctime(d):
    """
    utc时间转当地时间
    :param d:
    :return:
    """
    try:
        return d - datetime.timedelta(hours=8)
    except:
        return None


def date2ymdhms(d):
    try:
        return d.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return ""
