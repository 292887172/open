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
    return HttpResponseRedirect('/center/login')
    # return render(request, "home/home.html", locals())


def guide(request):
    if request.user.account_type == _convention.USER_IS_ADMIN:
        return HttpResponseRedirect(reverse("admin_center"))
    return render(request, "home/guide.html", locals())


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