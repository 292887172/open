# -*- coding: utf-8 -*-
import json
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from common.api_helper import RequestMethod, RestApiClient
from model.center.doc_menu import DocMenu
from model.wiki.wikiapi import Api, ApiDoc
from conf.newuserconf import *
from model.center.app import App
from base.const import ConventionValue

_convention = ConventionValue()

# @login_required


def wiki(request):
    """
    文档导航页面
    :param request:
    :return:
    """
    default_apps = App.objects.filter(developer=DEFAULT_USER).filter(check_status=_convention.APP_DEFAULT)
    menus1,menus2,menus3 = nav_content()
    return render(request, "wiki/index.html", locals())


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
        elif i.dm_parent_id == parent_id2 and i.dm_name !="接口在线调试":
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


def doc_wiki(request):
    """
    文档页面
    :param request:
    :return:
    """
    view = request.GET.get("view", '')
    view = view.split("Navicat")
    name = "Navicat" + view[1][0]
    dm_id = int(view[1][1:])
    try:
        doc = DocMenu.objects.get(dm_id=dm_id)
        isParent = doc.dm_is_parent
    except Exception as e:
        pass
    menus = nav_content(name)
    # 保存菜单到session中
    request.session['menus'] = json.dumps(menus)
    default_apps = App.objects.filter(developer=DEFAULT_USER).filter(check_status=_convention.APP_DEFAULT)
    return render(request, "wiki/doc.html", locals())


def new_wiki(request):
    """

    :param request:
    :return:
    """
    # 获取接口信息
    cnt = Api.objects.all()
    return render(request, "wiki/old/index.html", {"data": cnt})


# @login_required
def wiki_webtools(request):
    """
    接口调试工具
    :param request:
    :return:
    """
    # 获取接口信息
    cnt = Api.objects.all()
    return render(request, "wiki/old/webtools.html", {"data": cnt})


@csrf_exempt
# @login_required
def wiki_service(request):
    """
    接口测试执行程序
    :param request:
    :return:
    """
    apiurl = request.POST.get("api_url", "")
    apimethod = request.POST.get("api_method", "")
    # 使用Http Basic Authentication来验证
    username = request.POST.get("appid", "")
    password = request.POST.get("appsecret", "")
    etag = request.POST.get("etag", "")
    allparams_dict = {}
    header_dict = {}
    if etag != "":
        header_dict["If-Match"] = etag
    for item in request.POST:
        allparams_dict[item] = request.POST.get(item, "")
    del allparams_dict["api_url"]
    del allparams_dict["api_method"]
    del allparams_dict["appid"]
    del allparams_dict["appsecret"]
    del allparams_dict["etag"]
    method = None
    if apimethod == "post":
        method = RequestMethod.POST
    elif apimethod == "put":
        method = RequestMethod.PUT
    elif apimethod == "delete":
        method = RequestMethod.DELETE
    elif apimethod == "patch":
        method = RequestMethod.PATCH
    else:
        method = RequestMethod.GET
    client = RestApiClient(apiurl, method, username, password)
    client.addpara(allparams_dict)
    client.addheader(header_dict)
    r = client.invoke()
    return HttpResponse(r.text)


# @login_required
def wiki_doc(request):
    """
    api文档
    :param request:
    :return:
    """
    apiid = request.REQUEST.get("id", "")
    cnt = ""
    try:
        if id != "":
            cnt = ApiDoc.objects.get(api=int(apiid))
    except:
        pass
    data = ApiDoc.objects.all()
    return render(request, "wiki/old/doc.html", {"data": data, "cnt": cnt})


def wiki_doc_test(request):
    return HttpResponse('doc is ready')


# @login_required
def wiki_download(request):
    """
    资源下载
    :param request:
    :return:
    """
    return render(request, "wiki/old/download.html", locals())
