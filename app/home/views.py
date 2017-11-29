# -*- coding: utf-8 -*-
import codecs
import json
from base.const import ConventionValue
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
import markdown
from model.center.doc_menu import DocMenu
from common.message_helper import *
from conf.message import *

from open import settings
_convention = ConventionValue()


def home(request):
    # return HttpResponseRedirect('/center/login')
    return render(request, "home/home.html", locals())


def guide(request):
    try:
        if request.user.account_type == _convention.USER_IS_ADMIN:
            return HttpResponseRedirect(reverse("admin_center"))
    except AttributeError:
        pass
    menus1,menus2,menus3 = nav_content()
    return render(request, "home/index.html", locals())


def nav_content(name=''):
    menus1 = []
    menus2 = []
    menus3 = []
    parent_id2 = ''
    parent_id1 = ''
    temp = ["开发者必读", '开发者工具']
    dm = DocMenu.objects.all()
    for i in dm:
        menu = dict()
        menu['menu_id'] = i.dm_id
        menu['menu_name'] = i.dm_name
        menu['menu_is_parent'] = i.dm_is_parent
        menu['menu_url'] = i.dm_url
        menu['menu_depth'] = i.dm_depth
        menu['menu_ordernum'] = i.dm_order_num
        menu['menu_parent_id'] = i.dm_parent_id
        menu['menu_class'] = i.dm_class
        if i.dm_name in temp[0]:
            parent_id1 = i.dm_id
            menus1.append(menu)
        elif i.dm_name in temp[1]:
            parent_id2 = i.dm_id
            menus2.append(menu)
    for i in dm:
        menu = dict()
        menu['menu_id'] = i.dm_id
        menu['menu_name'] = i.dm_name
        menu['menu_is_parent'] = i.dm_is_parent
        menu['menu_url'] = i.dm_url
        menu['menu_depth'] = i.dm_depth
        menu['menu_ordernum'] = i.dm_order_num
        menu['menu_parent_id'] = i.dm_parent_id
        menu['menu_class'] = i.dm_class
        if i.dm_parent_id == parent_id1:
            menus1.append(menu)
        elif i.dm_parent_id == parent_id2 and i.dm_name != "接口在线调试":
            menus2.append(menu)
        elif i.dm_id!=parent_id1 and i.dm_id!=parent_id2:
            menus3.append(menu)
    if name == '':
        return [menus1,menus2,menus3]
    elif name =='Navicat1':
        return menus1
    elif name =='Navicat2':
        default_dubug = {'menu_id': '10000', 'menu_name': '下载中心', 'menu_url': '/sdk', 'menu_parent_id': parent_id2, 'menu_ordernum': '10000', 'menu_depth': '2'}
        menus2.append(default_dubug)
        return menus2
    elif name =='Navicat3':
        return menus3


def test(request):
    # code = codecs.open(settings.BASE_DIR + "/static/file/BUILD.md", "r", "utf-8").read()
    # ret = markdown.markdown(code, ['codehilite'])
    return render(request, "home/test.html", locals())


def left(request):
    """
    加载左侧菜单
    :param request:
    :return:
    """
    dm = DocMenu.objects.all()
    menus = []
    for i in dm:
        menu = dict()
        menu['menu_id'] = i.dm_id
        menu['menu_name'] = i.dm_name
        menu['menu_is_parent'] = i.dm_is_parent
        menu['menu_url'] = i.dm_url
        menu['menu_depth'] = i.dm_depth
        menu['menu_ordernum'] = i.dm_order_num
        menu['menu_parent_id'] = i.dm_parent_id
        menu['menu_class'] = i.dm_class
        menus.append(menu)
    # 保存菜单到session中
    request.session['menus'] = json.dumps(menus)
    return render(request, 'home/left_menu.html', locals())


def top(request):
    """
    加载顶部导航
    :param request:
    :return:
    """
    return render(request, 'home/right_main.html', locals())


def hz(request):
    """
    合作流程
    :param request:
    :return:
    """
    return render(request, 'home/hz.html', locals())


def zny(request):
    """
    53iq智能云
    :param request:
    :return:
    """
    return render(request, 'home/zny.html', locals())


def dynamic(request):
    """
    最新动态
    :param request:
    :return:
    """
    developer_id = request.user.developer.developer_id
    message = read_user_message(developer_id, USER_TYPE)
    m = get_sys_message(SYS_SENDER)
    if not m:
        save_user_message('', SYS_CONTENT, SYS_TYPE, SYS_SENDER)
    sys = read_user_message(SYS_SENDER, SYS_TYPE)
    return render(request, 'home/dynamic.html', locals())


def zy(request):
    """
    资源提供
    :param request:
    :return:
    """
    return render(request, 'home/zny.html', locals())


def kfz(request):
    """
    注册成为开发者
    :param request:
    :return:
    """
    return render(request, 'home/kfz.html', locals())


def sdk(request):
    """
    sdk及文档下载
    :param request:
    :return:
    """
    return render(request, 'home/sdk.html', locals())


def error(request):
    """
    浏览器版本过低
    :param request:
    :return:
    """
    return render(request, 'home/error.html', locals())


def big(request):
    """
    大屏智能方案
    :param request:
    :return:
    """
    return render(request, 'home/big.html', locals())


def contact(request):
    """
    联系我们
    :param request:
    :return:
    """
    return render(request, 'home/contact.html', locals())