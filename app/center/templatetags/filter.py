# -*- coding: utf-8 -*-
import datetime
from django.db import models
from django import template
from conf.message import BOOK
from model.center.doc_ui import DocUi

register = template.Library()
'''自定义django模板过滤器'''


def xxxx(key):
    try:

        vv = ''
        obj = DocUi.objects.filter(ui_key=key)
        if not obj:
            return "制定计划书"
        else:
            ack_list = []
            for i in obj:
                if i.ui_ack == int(1):
                    pass
                else:
                    ack_list.append(i.ui_upload_id)

            if not ack_list:
                return "等待上线"
            num = sorted(ack_list)[0]
            for i in obj.filter(ui_upload_id=num):
                vv = i.ui_plan
            if vv:

                return vv
            else:
                return "制定计划书"
    except Exception as e:
        print(e)


register.filter(xxxx)


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
        dtstr = date4.strftime("%Y-%m-%d %H:%I:%S")
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


def num_app(app):
    return len(app) - 1


register.filter(num_app)


def category_detail(obj):
    try:
        type = str(obj)
        category = {'31': '洗碗机', '1': '油烟机', '2': '集成灶', '6': '冰箱', '11': '烤箱', '21': "蒸烤箱", '20': '蒸箱', '25': ' 电压力锅',
                    '26': '电饭煲', '27': '台式小烤箱', '30': '微蒸烤', '0': '其他'}
        return category[type]
    except Exception as e:
        print(e)


register.filter(category_detail)


def category_detail1(obj):
    try:
        type = str(obj)
        category = {'':' ','0': '', '1': '4.3寸屏', '2': '5寸屏', '3': '6.8寸长条屏'}
        return category[type]
    except Exception as e:
        print(e)


register.filter(category_detail1)


def is_none(value):
    """
    检测是否为空
    :param value:
    :return:
    """
    if value is None:
        return ""
    elif value == 0:
        return ""
    else:
        return value


register.filter(is_none)


@register.inclusion_tag('component/menu.html', takes_context=True)
def create_menu(context, cur=0, username=None):
    ret = {
        'menu': None,
        "cur": cur
    }
    if "menu" in context:
        ret["menu"] = context["menu"]
    else:
        if username:
            menu = [

                {"url": "/product/console/", "title": "控制台"},
                {"url": "/product/list/", "title": "厨电开发"},
                {"url": "/product/kitchen/", "title": "厨电方案"},
                {"url": "/SmartRecipe/", "title": "智能菜谱"},
                {"url": "/product/community/", "title": "厨房社区"},

            ]

        else:
            menu = [
                {"url": "/", "title": "首页"},
                {"url": "/product/console/", "title": "控制台"},
                {"url": "/product/kitchen/", "title": "厨电方案"},
                {"url": "/SmartRecipe/", "title": "智能菜谱"},
                {"url": "/product/community/", "title": "厨房社区"},

            ]
        ret["menu"] = menu
    return ret


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


def cover_user_name(user_id, nickname):
    """    转换微信昵称
    :param user_id:
    :param nickname
    :return:
    """
    try:
        if nickname:
            return nickname
        else:
            a = list(user_id)
            if "com" in user_id:
                a[3:-9] = "****"
            elif len(user_id) == 11:
                a[3:-4] = "****"
            user_id = ''.join(a)
            return user_id
    except:
        return ""


register.filter(cover_user_name)


def check_isphone_mail(val, type):
    """
    检查是否为电话或者邮箱
    :param val:
    :return:
    """
    import re
    if type == 'phone':
        if re.match('1[34578]\\d{9}', val):
            return val

    elif type == 'mail':
        if "@" in val:
            return val
    return ''


register.filter(check_isphone_mail)


def check_first_child(menus, id):
    for m in menus:
        if int(m["menu_parent_id"]) == int(id):
            print(id, m["menu_parent_id"])
            return m["menu_id"]
    return id


register.filter(check_first_child)


def cover_product_key(val):
    """
    转换产品key
    :param val:
    :return:
    """
    try:
        s1 = str(val)
        s2 = s1[-8:]
        return s2
    except:
        return ""


register.filter(cover_product_key)


@register.inclusion_tag('component/fast_create.html')
def fast_create_product(developer_id):
    # 暂时没有用到的参数
    ret = {"developer_id": developer_id}
    return ret
