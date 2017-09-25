# -*- coding: utf-8 -*-
import datetime

from django import template


register = template.Library()
'''自定义django模板过滤器'''


def utc2local(obj):
    """
    将utc时间转为本地时间年-月-日
    :param obj:
    :return:
    """
    try:
        date4 = obj + datetime.timedelta(hours=8)
        dtstr = date4.strftime("%Y-%m-%d")
        return dtstr
    except:
        return ""


register.filter(utc2local)


def utc2local2(obj):
    """
    将utc时间转为本地时间年-月-日 时：分：秒
    :param obj:
    :return:
    """
    try:
        date4 = obj + datetime.timedelta(hours=8)
        dtstr = date4.strftime("%Y-%m-%d")
        return dtstr
    except:
        return ""


register.filter(utc2local2)


def cover_str(obj):
    """
    隐藏字符串中间四位
    :param obj:
    :return:
    """
    try:
        s1 = str(obj)
        s2 = '*'
        dtstr = s1[:3] + 4 * s2 + s1[7:]
        return dtstr
    except:
        return ""


register.filter(cover_str)


def is_none(value):
    """
    检测是否为空
    :param value:
    :return:
    """
    if value is None:
        return ""
    else:
        return value


register.filter(is_none)


@register.inclusion_tag('component/menu.html', takes_context=True)
def create_menu(context, cur=0, dev_id=None):
    ret = {
        'menu': None,
        "cur": cur
    }
    if "menu" in context:
        ret["menu"] = context["menu"]
    else:
        if dev_id:
            menu = [
                    {"url": "/product/list/", "title": "产品管理"},
                    {"url": "/guide", "title": "开发指南"},
                    {"url": "/wiki/", "title": "开发文档"}
                    ]

        else:
            if cur > 1:
                ret['cur'] = 1
            menu = [
                    {"url": "/guide", "title": "开发指南"},
                    {"url": "/wiki/", "title": "开发文档"}
                    ]
        ret["menu"] = menu


    return ret


def cover_device_type(obj):
    """
    转换产品类别
    :param obj:
    :return:
    """
    try:
        t = {'1': '油烟机', '2': '集成灶', '6': '冰箱', '11': '烤箱', '20': '蒸箱'}
        s1 = str(obj)
        if s1 in t.keys():
            return t[s1]
        else:
            return ''
    except:
        return ""


register.filter(cover_device_type)


def cover_str8(obj):
    """
    截取字符串后8位
    :param obj:
    :return:
    """
    try:
        s1 = str(obj)

        dtstr = s1[-8:]
        return dtstr
    except:
        return ""


register.filter(cover_str8)
