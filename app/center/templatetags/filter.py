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
            menu = [{"url": "/", "title": "首页"},
                    # {"url": "/wiki", "title": "文档"},
                    {"url": "/product/list/", "title": "产品管理"},
                    {"url": "/guide", "title": "开发指南"},
                    {"url": "/center", "title": "帐号管理"}]

        else:
            menu = [{"url": "/", "title": "首页"},
                    {"url": "/guide", "title": "开发指南"},
                    # {"url": "/wiki", "title": "文档"},
                    {"url": "/center/", "title": "加入我们"}]
        ret["menu"] = menu

    return ret