# !/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import logging
import json

from base.connection import RedisBaseHandler, Redis3
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import simplejson as simplejson
from common.doc_helper import DocBll, execute_menu,save_device_menu
from common.code import ResponseCode
from conf.commonconf import CLOUD_TOKEN
from conf.docconfig import DOC_RET_MSG
from model.center.api import Api
from model.center.doc import Doc
from model.center.doc_menu import DocMenu
from model.center.device_menu import DeviceMenu
from util.jsonutil import MyEncoder
_code = ResponseCode()

@csrf_exempt
@login_required
def editormd(request):
    """
    在线markdown编辑器
    只考虑doc_id已经存在的情况

    :param request:doc_id
    :return:
    """
    ret_msg = copy.deepcopy(DOC_RET_MSG)
    if request.method == 'GET':
        doc_id = request.GET.get('doc_id', None)
        if doc_id is None:
            return HttpResponse("缺少doc_id")
        else:
            try:
                doc = Doc.objects.get(doc_id=doc_id)
            except Exception as e:
                logging.getLogger("").info(str(e))
                return HttpResponse("不存在此编号的文档，请先添加")
            markdown_str = doc.doc_markdown
            if doc.doc_type == 0 and markdown_str is None:
                markdown_str = DocBll.get_api_doc(doc.api_id)
            elif markdown_str is None:
                if doc.doc_type == 1:
                    markdown_str = "# 这是普通文档"
                elif doc.doc_type == 2:
                    markdown_str = "# 这是内部加密文档"
                else:
                    markdown_str = ""

        return render(request, 'center/editormd.html', {
            'doc_id': doc_id,
            'markdown_textarea': markdown_str
        })
    if request.method == 'POST':
        doc_id = request.POST.get('doc_id', None)
        if doc_id is None:
            ret_msg["status"] = -1
            ret_msg["msg"] = "doc_id为空"
            return JsonResponse(ret_msg)

        md_html = request.POST.get('html', None)
        md_markdown = request.POST.get('markdown', '')

        # destination_html = ""
        # tpl = open(os.path.join(DOC_TPL_PATH, "base.html"), 'r', encoding='utf-8')
        # for line in tpl.readlines():
        # destination_html += line.replace('[mdEditor.getPreviewedHTML()]', md_html)
        # tpl.close()
        # 将html文件上传到云存储
        if md_html is not None:
            doc = Doc.objects.get(doc_id=doc_id)
            doc.doc_markdown = md_markdown
            doc.doc_html = md_html
            doc.save()
            ret_msg["data"] = "/center/doc_show/" + str(doc.doc_id)
        else:
            ret_msg["status"] = 0
            ret_msg["msg"] = "参数错误"

        return JsonResponse(ret_msg)


@csrf_exempt
def doc_image_upload(request):
    """
    处理从markdown编辑器中上传的图片
    返回图片路径
    :param request:
    :return:
    """
    flag = 'editormd-image-file'
    if request.method == "POST":
        if len(request.FILES.dict()) >= 1:
            f = request.FILES[flag]
            from ebcloudstore.client import EbStore

            store = EbStore(CLOUD_TOKEN)
            r = store.upload(f.read(), f.name, f.content_type)
            r_obj = json.loads(r)
            if r_obj["code"] == 0:
                ret = {
                    "success": 1,
                    "message": "上传成功",
                    "url": r_obj["data"]
                }
            else:
                ret = {
                    "success": 0,
                    "message": "上传失败 %s" % r_obj["msg"],
                    "url": None
                }
            return JsonResponse(ret)


@csrf_exempt
def doc_menu(request):
    """
    文档菜单
    :param request:
    :return:
    """
    if request.method == "POST":
        ret_msg = copy.deepcopy(DOC_RET_MSG)
        data = request.body.decode("utf-8")
        menu_arr = json.loads(data)
        # 处理菜单数据
        ret = execute_menu(menu_arr)
        if not ret:
            ret_msg["status"] = -1
        return JsonResponse(ret_msg)
    else:
        doc_menu = DocMenu.objects.all()
        ret = []
        for i in doc_menu:
            dm = dict({
                "id": i.dm_id,
                "name": i.dm_name,
                "is_parent": i.dm_is_parent,
                "url": i.dm_url,
                "depth": i.dm_depth,
                "ordernum": i.dm_order_num,
                "parent_id": i.dm_parent_id
            })
            ret.append(dm)
        # print(ret)
        return HttpResponse(json.dumps(ret))


@csrf_exempt
def doc_device(request):
    """
    设备菜单
    :param request:
    :return:
    """
    if request.method == "POST":
        ret_msg = copy.deepcopy(DOC_RET_MSG)
        data = request.body.decode("utf-8")
        menu_data = json.loads(data)
        r = Redis3().client  # 调用redis存储
        r_key = _code.DEVICE_MENU_PREFIX
        # 处理菜单数据
        ret = save_device_menu(menu_data)
        if not ret:
            ret_msg["status"] = -1
        else:
            doc_device = DeviceMenu.objects.all()
            ret = []
            for i in doc_device:
                dm = dict({
                    "id": i.device_menu_id,
                    "name": i.menu_name,
                    "url": i.menu_url,
                    "device_key": i.device_key,
                    "sort": i.device_type
                })
                ret.append(dm)
            ret = json.dumps(ret)
            r.set(r_key, ret)
        return JsonResponse(ret_msg)
    if request.method == "GET":
        doc_device = DeviceMenu.objects.all()
        r = Redis3().client  # 调用redis存储
        r_key = _code.DEVICE_MENU_PREFIX
        r_value = r.get(r_key)

        if not r_value:
            ret = []
            for i in doc_device:
                dm = dict({
                    "id": i.device_menu_id,
                    "name": i.menu_name,
                    "url": i.menu_url,
                    "device_key": i.device_key,
                    "sort":i.device_type
                })
                ret.append(dm)
            ret = json.dumps(ret)
            r.set(r_key,ret)
        else:
            ret = r_value.decode("utf-8")
            ret = json.loads(ret)
        return HttpResponse(json.dumps(ret))



def action_doc_menu_view(request):
    """
    创建或更新doc_menu
    接受json
    {
        menu_info: {},
        sub_menu: [{},{},{},]
    }

    :param request:
    :return:
    """
    if request.method == 'POST':
        dm_id = request.POST.get('dm_id', '')

        req = simplejson.loads(request.body)

        if dm_id != '':
            pass


        else:
            pass
    else:
        return HttpResponseForbidden()


def doc_show(request, doc_id):
    ret = ""
    try:
        doc = Doc.objects.get(doc_id=doc_id)
        if doc.doc_html is not None:
            ret = doc.doc_html
    except Exception as e:
        logging.getLogger("").info(str(e))
    return HttpResponse(ret)


@csrf_exempt
def api_create_doc(request):
    ret_msg = copy.deepcopy(DOC_RET_MSG)
    if request.method == "GET":
        action = request.REQUEST.get("action", None)
        if action:
            if action == "get-api":
                ret = Api.objects.all()
                ret_msg["data"] = ret
                return HttpResponse(json.dumps(ret_msg, cls=MyEncoder))
    if request.method == "POST":

        doc_type = request.POST.get('doc_type', None)
        api_id = request.POST.get('api_id', None)
        doc_name = request.POST.get('doc_name', "")
        if doc_type is None:
            ret_msg["status"] = -2
            ret_msg["msg"] = "文档类型为空"
            return JsonResponse(ret_msg)
        if doc_type == "0":
            # 接口文档
            ret = DocBll.add_api_doc(api_id)
            if ret[1]:
                ret_msg["status"] = 1

            else:
                ret_msg["status"] = 2
                ret_msg["msg"] = "已存在直接编辑即可"
                pass
            ret_msg["data"] = ret[0].doc_id
            return JsonResponse(ret_msg)
        elif doc_type in ["1", "2"]:
            doc = DocBll.add_doc(doc_type, doc_name)
            ret_msg["status"] = 1
            ret_msg["data"] = doc.doc_id
            return JsonResponse(ret_msg)


@csrf_exempt
def api_delete_doc(request):
    if request.method == "POST":
        doc_id = request.REQUEST.get('doc_id', '')
        try:
            Doc.objects.filter(doc_id=doc_id).delete()
        except Exception as e:
            logging.getLogger('').error(e)
            statu = False
        else:
            statu = True
        if statu:
            data = {
                "status": 1,
                "message": "删除成功",
            }
            return JsonResponse(data)
        else:
            data = {
                "status": 0,
                "message": "删除失败",
            }
            return JsonResponse(data)
    else:
        return HttpResponse(status='200')


def api_select_doc(reqeust):
    if reqeust.method == "POST":
        try:
            doc_id = reqeust.REQUEST.get('doc_id', '')
        except Exception as e:
            logging.getLogger('').error(e)

        else:
            if Doc.objects.filter(doc_id=doc_id).exists():
                doc = Doc.objects.get(doc_id=doc_id)
                data = dict(

                )
    else:
        return HttpResponse('ready to select doc!')


def api_doc_fetch(request):
    """
    获取所有文档信息
    :param request:
    :return:
    """

    def get():
        page = request.GET.get("page", 1)
        limit = request.GET.get("limit", 20)
        sort = request.GET.get("sort", "")
        (sort_name, sort_status) = sort.split(".")
        order_by_names = ""
        if sort_status == "desc":
            order_by_names = "-"
        if sort_name == "doc_id":
            order_by_names += "doc_id"
        ret = DocBll.fetch(page, limit, order_by_names)
        return HttpResponse(json.dumps(ret, separators=(",", ":")))

    def post():
        pass

    if request.method == "GET":
        return get()
    elif request.method == "POST":
        return post()


def get_api_info(api_id):
    """
    查询api 信息
    :param api_id:
    :return:
    """
    if Api.objects.filter(api_id=api_id).exists():
        api = Api.objects.get(api_id=api_id)

        data = {
            "api_url": api.api_url,
            "api_type": api.api_type,
            "api_request_type": api.api_request_type,
            "api_params": api.api_params,
            "api_name": api.api_name,
            "api_return": api.api_return,
            "api_describe": api.api_describe,
            "api_doc_url": api.api_doc_url,
            "api_action_url": api.api_action_url,
            "api_port": api.api_port,
            "api_classify": api.api_classify,
            "api_function": api.api_function,
            "api_level": api.api_level,
            "api_group": api.api_group,
            "api_invoke_total": api.api_invoke_total,
            "api_is_forbid": api.api_is_forbid,
            "api_create_date": api.api_create_date
        }
        for key, item in data.items():
            if item is None:
                data[key] = ""
        return data
