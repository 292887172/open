# -*- coding: utf-8 -*-
import time
import math
from functools import cmp_to_key
from base.connection import Redis3_ClientDB6, Redis3_ClientDB5
from base.util import gen_app_default_conf
from common.app_helper import cancel_release_app
from common.app_helper import update_app_fun_widget, add_fun_id, add_mod_funs, \
    get_mod_funs
from common.app_helper import save_app, check_cloud, new_mxs_data
from common.app_helper import off_app
from common.app_helper import release_app
from common.app_helper import reset_app_secret
from common.app_helper import update_app_config
from common.app_helper import update_app_info
from common.app_helper import get_docui
from common.device_fun_helper import add_device_fun
from common.device_online import device_online
from common.message_helper import save_user_message
from common.smart_helper import *
from common.util import reverse_numeric
from conf.message import *
from model.center.app import App
from model.center.user_group import UserGroup
from util.export_excel import date_deal
from util.netutil import verify_push_url
from base.const import ConventionValue
from common.mysql_helper import get_ui_static_conf, remove_up_url
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, JsonResponse
from common.mysql_helper import query_data, get_ui_base_conf, query_ui_conf
from util.email.send_email_code import send_product_process_email
import json
import logging
import datetime
from conf.commonconf import CLOUD_TOKEN
from model.center.account import Account
from model.center.account_info import AccountIfo
from model.center.app_version import AppVersion
from model.center.firmware import Firmware
from model.center.doc_ui import DocUi
from ebcloudstore.client import EbStore
from base.const import StatusCode, DefaultProtocol, DefaultSchedule


_convention = ConventionValue()


@csrf_exempt
def pull_ui_conf(request):
    if request.method == 'POST':
        device_key = request.POST.get('key')
        if device_key:
            a = query_data(device_key)
            if a:
                new_functions = []
                function_list = json.loads(a['ebf_pc_conf'])['functions']
                # print(json.loads(a['ebf_page_conf'])['name'])
                for i in function_list:
                    if int(i['isUiShow']) == 1:
                        new_functions.append(
                            {'name': i['name'], "id": i['id'], 'title': i['title'], 'values': i['values'],
                             'type': i['type'], 'permission': i['permission']})
                json.loads(a['ebf_pc_conf'])['functions'] = new_functions

                new_list = {'name': json.loads(a['ebf_pc_conf'])['name'], 'key': json.loads(a['ebf_pc_conf'])['key'],
                            "model": json.loads(a['ebf_pc_conf'])['model'], "functions": new_functions,
                            }
                back_data = {"data": new_list, "code": 0}
                return JsonResponse(back_data)
            else:
                data = {'code': -1, 'msg': 'no  conf'}
                return HttpResponse(json.dumps(data), content_type="application/json")

        else:
            data = {'code': -1, 'msg': 'no key'}
            return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def upload_ui_conf(request):
    if request.method == 'POST':
        device_id = request.POST.get('key')

        device_conf = request.POST.get('ui_conf')
        cook_ies = request.COOKIES['COOKIE_USER_ACCOUNT']

        if device_id:
            if device_conf:
                back_data = get_ui_base_conf(device_id, device_conf, cook_ies)
                if back_data == 'ok':
                    data = {'code': 0, 'msg': 'ok'}
                    return HttpResponse(json.dumps(data), content_type="application/json")
                else:
                    data = {'code': 1, 'msg': 'save failed'}
                    return HttpResponse(json.dumps(data), content_type="application/json")
            else:
                data = {'code': -1, 'msg': 'no conf'}
                return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            data = {'code': -1, 'msg': 'no key'}
            return HttpResponse(json.dumps(data), content_type="application/json")


@csrf_exempt
def diy_ui_conf(request):
    device_key = request.GET.get('key')
    if device_key:
        try:
            a = query_data(device_key)
            back_data = query_ui_conf(device_key)
            new_functions = []
            if a:
                function_list = json.loads(a['ebf_pc_conf'])['functions']
                # print(json.loads(a['ebf_page_conf'])['name'])
                for i in function_list:
                    if int(i['isUiShow']) == 1:
                        new_functions.append(
                            {"id": i['id'], 'values': i['values'],
                             'type': i['type'], 'permission': i['permission']})
            if back_data and back_data != 'error':
                p = json.loads(back_data['ebf_page_conf'])['function']
                for ii in range(len(p)):
                    p[ii].update(new_functions[ii])
                return HttpResponse(json.dumps({"function": p}), content_type="application/json")
        except Exception as e:
            print(e)
        return JsonResponse({})


@csrf_exempt
def save_user_address(request):
    if request.method == 'POST':
        user_account = request.POST.get('user_account', '')
        contact_name = request.POST.get('contact_name', '')
        contact_phone = request.POST.get('contact_phone', '')
        contact_address = request.POST.get('contact_address', '')

        if user_account:
            try:
                ac = Account.objects.get(account_id=user_account)
                ai = AccountIfo(
                    account_id=ac,
                    contact_name=contact_name,
                    contact_phone=contact_phone,
                    contact_address=contact_address,
                    account_create_date=datetime.datetime.utcnow()
                )
                ai.save()
                return JsonResponse({'code': 0, 'msg': 'success'})
            except Exception as e:
                logging.getLogger('').info(' 创建用户邮寄地址信息失败' + str(e))
            return JsonResponse({'code': -2, 'msg': 'account save error'})
        else:
            return JsonResponse({'code': -3, 'msg': 'miss parameters'})
    else:
        return JsonResponse({'code': -1, 'msg': 'error request method'})


@csrf_exempt
def get_factory(request):
    if request.method == "GET":
        data = request.GET.get("data", "")
        if data == "factory_list":
            factory_list = {"data":get_factory_list()}

            response = HttpResponse(json.dumps(factory_list))
            response["Access-Control-Allow-Origin"] = "*"
            return response


@csrf_exempt
def get_function_list(request):

    def findname(names, opera_data):
        names_list = eval(names)
        names = []
        for i in range(len(opera_data)):
            for j in names_list:
                if str(opera_data[i]['Stream_ID']) == j:
                    names.append(opera_data[i]['name'])
        return names
    def find(id, opera_data):
        for i in range(len(opera_data)):
            if str(opera_data[i]['id']) == id:
                return [i, opera_data[i]]
        return []

    if request.method == "GET":
        app_id = request.GET.get("ID", "")
        post_data = request.GET.get("name", '')
        app = App.objects.get(app_id=app_id)
        device_conf = gen_app_default_conf(app.app_device_type)

        opera_data = []
        if post_data == 'list':
            # 显示所有列表信息
            temp = []
            try:
                if app.device_conf:
                    opera_data = json.loads(app.device_conf)
                    opera_data.sort(key=lambda x: int(x.get("id")))
            except Exception as e:
                logging.info("读取数据库中设备配置信息失败", e)
                print(e)
            for line in opera_data:
                temp.append(line)
            data = {'rows': opera_data, 'check_state': app.check_status}

            # data["records"] = len(temp)
            return JsonResponse(data)
        elif post_data == "show_mod":
            app_device_type = app.app_device_type
            mod = get_mod_funs(opera_data, device_conf, app_device_type)
            return JsonResponse({"data": mod})
    if request.method == "POST":
        funs = request.POST.get("funs",'')
        app_id = request.GET.get("ID", "")
        post_data = request.POST.get("name", '')
        idsd = request.POST.get("nums",'')
        app = App.objects.get(app_id=app_id)
        app_device_type = app.app_device_type
        device_conf = gen_app_default_conf(app.app_device_type)
        opera_data = []
        try:
            if app.device_conf:
                opera_data = json.loads(app.device_conf)
                opera_data.sort(key=lambda x: int(x.get("id")))
        except Exception as e:
            logging.info("读取数据库中设备配置信息失败", e)
            print(e)
        if post_data == 'add_mod':
            add_mod_funs(opera_data, device_conf, funs, app_device_type)
            save_app(app, opera_data, '重构')
            update_app_protocol(app)
            # 新增功能message
            namess = findname(funs, opera_data)
            for i in namess:
                message_content = '"' + app.app_name + '"' + i + CREATE_FUN
                save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id, app.app_appid)
            return HttpResponse('add_mod_success')
        elif post_data == 'del':
            # 删除信息
            data = find(idsd, opera_data)
            if data:
                i = data[0]
                fun_name = data[1].get("name")
                is_standa = data[1].get("standa_or_define", None)
                opera_data.pop(i)
                for j in range(len(opera_data)):
                    opera_data[j]['id'] = str(int(j) + int(1))
                c_data = opera_data[:len(opera_data)]
                c_data.sort(key=lambda x: int(x.get("id")))
                c_data.extend(opera_data[len(opera_data):])
                opera_data = c_data
                save_app(app, opera_data, '重构')
                update_app_protocol(app)
                message_content = '"' + app.app_name + '"' + fun_name + DEL_FUN
                save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id, app.app_appid)
                return HttpResponse('del_success')
            return HttpResponse('del_fail')
        elif post_data == 'del_all':
            # 这里对后台发送来对数据进行筛选,重新排序 从大到小 避免勿删除操作
            idsd = eval(idsd)
            # 删除一个与多个判断
            if isinstance(idsd, int):
                print('1')
                data = find(str(idsd), opera_data)
                if data:
                    i = data[0]
                    fun_name = data[1].get("name")
                    is_standa = data[1].get("standa_or_define", None)
                    opera_data.pop(i)
                    for j in range(len(opera_data)):
                        opera_data[j]['id'] = str(int(j) + int(1))
                    c_data = opera_data[:len(opera_data)]
                    c_data.sort(key=lambda x: int(x.get("id")))
                    c_data.extend(opera_data[len(opera_data):])
                    opera_data = c_data
                    # 排序？？？？？？
                    # replace_fun_id(opera_data, id, is_standa)
                    save_app(app, opera_data, '重构')
                    update_app_protocol(app)
                    message_content = '"' + app.app_name + '"' + fun_name + DEL_FUN
                    save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id, app.app_appid)
            else:
                print('2')
                ids_list = list(idsd)
                ids_list = sorted(ids_list, key=cmp_to_key(reverse_numeric))
                for id_i in ids_list:
                    data = find(str(id_i), opera_data)
                    if data:
                        i = data[0]
                        fun_name = data[1].get("name")
                        is_standa = data[1].get("standa_or_define", None)
                        opera_data.pop(i)
                        for j in range(len(opera_data)):
                            opera_data[j]['id'] = str(int(j) + int(1))
                        c_data = opera_data[:len(opera_data)]
                        c_data.sort(key=lambda x: int(x.get("id")))
                        c_data.extend(opera_data[len(opera_data):])
                        opera_data = c_data
                        # 排序？？？？？？
                        # replace_fun_id(opera_data, id, is_standa)
                        save_app(app, opera_data, '')
                        update_app_protocol(app)
                        message_content = '"' + app.app_name + '"' + fun_name + DEL_FUN
                        save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id, app.app_appid)

            return HttpResponse('del_success')
        elif post_data in ['isShow', 'isControl', 'isDisplay', "isCloudMenu"]:
            val = request.POST.get("dd")
            data = find(idsd, opera_data)
            if data:
                data[1][post_data] = val
                fun_name = data[1].get("name")
                if post_data == "isCloudMenu":
                    app.app_is_cloudmenu_device = check_cloud(opera_data)
                save_app(app, opera_data, '重构')
                update_app_protocol(app)
                if val == str(1):
                    message_content = '"' + app.app_name + '"' + fun_name + UPDATE_FUN_OPEN
                else:
                    message_content = '"' + app.app_name + '"' + fun_name + UPDATE_FUN_CLOSE
                save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id, app.app_appid)
                return HttpResponse('change_success')
        elif post_data == 'toSwitch':
            for switch in opera_data:
                if int(switch["id"]) == int(idsd):
                    switch["toSwitch"] = 1
                else:
                    switch["toSwitch"] = 0
            save_app(app, opera_data, '重构')
            update_app_protocol(app)

            return HttpResponse('select_success')
        elif post_data == 'edit':
            # 返回编辑页面信息

            if len(idsd) > 3:
                idsd = idsd.split("#")[0]


            edit_data = find(idsd, opera_data)
            mods_name = list(map(lambda x: x["Stream_ID"], device_conf))
            mods_name1 = list(map(lambda x: x["Stream_ID"], opera_data))
            mods_name.extend(mods_name1)
            mods_name = list(set(mods_name))
            if edit_data:
                edit_data = edit_data[1]
                mods_name.remove(edit_data["Stream_ID"])
                message_content = '"' + app.app_name + '"' + UPDATE_FUN
                save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id, app.app_appid)
            else:
                edit_data = ''
            return JsonResponse({'data': edit_data, 'funs': opera_data, 'mods': mods_name})
        elif post_data == 'save':
            # 接收要编辑或者添加的数据
            indata = request.POST.get('d')
            indata = json.loads(indata)
            dt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            indata["time"] = dt
            indata["widget"] = update_app_fun_widget(indata)
            indata["isDisplay"] = 1
            try:
                indata['control'] = new_mxs_data(indata['control'])
            except Exception as e:
                print(e)
            fun_name = indata['name']
            if indata["id"]:
                # 编辑参数信息
                data = find(indata['id'], opera_data)
                data[1].update(indata)
                message_content = '"' + app.app_name + '"' + fun_name + UPDATE_FUN
                tt = "modify_success"
                save_user_message(app.developer_id, message_content, USER_TYPE, app.developer_id, app.app_appid)
            else:
                # 添加一条参数信息需要申请审核
                indata = add_fun_id(opera_data, indata)
                add_device_fun(app.app_appid, indata)
                opera_data.append(indata)
                opera_data.sort(key=lambda x: int(x.get("id")))
                # message_content = '"' + app.app_name + '"' + fun_name + CREATE_FUN
                tt = "modify_success"
            # 版本区别,在新版本加{"version":"1"} # 区分方法control
            # opera_data = save_control(opera_data)
            save_app(app, opera_data, '重构')
            update_app_protocol(app)
            return HttpResponse(tt)
        elif post_data == 'update':
            if funs:
                data1 = json.loads(funs)
                for i in range(len(data1)):
                    ids = int(i) + 1
                    try:
                        opera_data[int(data1[i])-1]['id'] = int(ids * 100)
                    except Exception as e:
                        print(e)
                list_up_id = []
                for i in opera_data:
                    list_up_id.append(i)
                for isd in list_up_id:
                    isd['id'] = str(int(int(isd['id'])/100))
                list_up_id.sort(key=lambda x: int(x.get("id")))
                print('new',list_up_id)
                save_app(app,list_up_id,'改版')
                return HttpResponse(json.dumps({"code": 0}))


@csrf_exempt
def protocol(request):
    # code说明 1 非表 2 标准 3 错误
    if request.method == 'GET':
        # 协议类型 1为下行 0为上行
        device_key = request.GET.get('key', '')
        zdy = request.GET.get('zdy', '')
        action = request.GET.get('action', '')
        protocol_type = request.GET.get('protocol_type', '0')
        pt = ''
        screen = request.GET.get('screen', '')
        device_types = request.GET.get('device_types', '')

        if action == 'get_data_content':
            app = App.objects.get(app_appid__endswith=device_key)
            dc = json.loads(app.device_conf)
            data = []
            for i in dc:
                tmp = {'id': i['id'], 'title': i['name'], 'length': i['mxsLength'], 'mxs': i['mxs']}
                data.append(tmp)
            return HttpResponse(json.dumps(data))
        elif action == 'get_frame_data':
            # 帧结构数据
            try:
                mlist = Protocol.objects.all().filter(protocol_device_key=device_key)
                if len(mlist) == 0:
                    # 没有定义过，返回标准协议，若请求自定义协议，则返回默认标准自定义协议

                    # p = DefaultProtocol().DEFAULT_DATA
                    p = DefaultProtocol().DEFAULT_DATA_ZDY
                    data = {"code": 2, "data": p, "protocol_type": protocol_type}
                    return HttpResponse(json.dumps(data))
                else:
                    # 根据请求，返回定义的上下行数据
                    # 如果定义过上行和下行数据，会有两条
                    for iii in mlist:
                        res_list_data = iii.protocol_factory_content
                        protocol_type1 = iii.protocol_factory_type  # 库中保存的数据 protocol类型0/1
                        res_list_data1 = json.loads(res_list_data)

                        res_list_data1['protocol_type'] = protocol_type1

                        if str(protocol_type1) == str(protocol_type):
                            data = {"code": 2, "data": res_list_data1, "protocol_type": protocol_type}
                            return HttpResponse(json.dumps(data))
                    # 请求的数据暂时未定义，比如自定义了上行数据，请求下行数据，或者自定义了下行数据，请求上行数据
                    # 返回空， 前端不处理
                        else:
                            pass
                    data = {"code": 1, "data": "", "protocol_type": protocol_type}
                    return HttpResponse(json.dumps(data))
            except Exception as e:
                print(e)
                logging.getLogger('').info("传入的参数zdy出错", str(e))
                data = {"code": 3, "data": DefaultProtocol().DEFAULT_DATA_ZDY, "protocol_type": 0}
                return HttpResponse(json.dumps(data))

    if request.method == 'POST':
        r = DefaultProtocol().DEFAULT_DATA_ZDY
        action = request.POST.get("action",'')
        try:
            if action == 'update_protocol':
                protocol_type = request.POST.get("protocol_type", '')
                list_key = request.POST.get('key', '')
                data_protocol_list = request.POST.get("data", '')
                data_protocol_list = json.loads(data_protocol_list)
                print('==',type(data_protocol_list))

                protocol_endian = data_protocol_list.get("protocol_endian", 1)
                list_t = data_protocol_list.get('frame_content', '')

                data_sql = {}
                data_sql['is_single_instruction'] = True
                data_sql['support_response_frame'] = True
                data_sql['support_serial'] = True
                data_sql['active_heartbeat'] = True
                data_sql['support_repeat'] = True
                data_sql['heart_rate'] = "500"
                data_sql['repeat_rate'] = "500"
                data_sql['repeat_count'] = "3"
                data_sql['endian_type'] = protocol_endian  # 1:大端编码， 0：小端编码， 默认大端编码

                tmp_list_t = []
                for i in list_t:
                    if i.get("is_enable", None):
                        tmp_f = {
                            "id": i.get("id"),
                            "length": i.get("length"),
                            "name": i.get("name"),
                            "title": i.get("title"),
                            "value": i.get("value"),
                            "is_enable": i.get("is_enable")
                        }
                    else:
                        tmp_f = {
                            "id": i.get("id"),
                            "length": i.get("length"),
                            "name": i.get("name"),
                            "title": i.get("title"),
                            "value": i.get("value")
                        }
                    if i.get("name") == "data":
                        # 处理数据域
                        l = 0
                        tmp_d = []
                        for j in i.get("value"):
                            if j.get('content'):
                                l += int(j.get('length'))
                                tmp_d.append(j)
                        tmp_f['length'] = math.ceil(l / 8)
                        tmp_f['value'] = tmp_d
                    elif i.get("name") == "check":
                        # 处理校验
                        tmp_f['value'] = {"check_algorithm": i.get('value').get("check_algorithm"),
                                          "check_start": i.get('value').get("check_start"),
                                          "check_end": i.get('value').get("check_end")}
                        data_sql['checkout_algorithm'] = i.get('value').get("check_algorithm")
                        data_sql['start_check_number'] = i.get('value').get("check_start")
                        data_sql['end_check_number'] = i.get('value').get("check_end")
                    tmp_list_t.append(tmp_f)
                data_sql['frame_content'] = tmp_list_t
                data_sql_update = json.dumps(data_sql, ensure_ascii=False)
                mlist = []
                if str(protocol_type) == '0':
                    # 上行
                    print('0', mlist)
                    update_protocol(list_key, data_sql_update, protocol_type, '重构')
                    mlist = Protocol.objects.all().filter(protocol_device_key=list_key,
                                                          protocol_factory_type=protocol_type)
                elif str(protocol_type) == '1':
                    # 下行
                    print('1', mlist)
                    update_protocol(list_key, data_sql_update, protocol_type, '重构')
                    mlist = Protocol.objects.all().filter(protocol_device_key=list_key,
                                                          protocol_factory_type=protocol_type)
                else:
                    print('2', mlist)
                    data = {"code": 3, "data": "发送数据错误", "protocol_type": 0}
                    return HttpResponse(json.dumps(data))
                for ii in mlist:
                    res_list_data = ii.protocol_factory_content
                    protocol_type1 = ii.protocol_factory_type

                    res_list_data1 = json.loads(res_list_data)
                    res_list_data1['protocol_type'] = protocol_type1
                    return HttpResponse(json.dumps(res_list_data1))

        except Exception as e:
            print(e)
            logging.getLogger('').info("非保存操作", str(e))
            data = {"code": 3, "data": DefaultProtocol().DEFAULT_DATA_ZDY, "protocol_type": 0}
            return HttpResponse(json.dumps(data))
        return HttpResponse(json.dumps(r))



@csrf_exempt
def product_main(request):
    """
    应用详情
    :param request:
    :return:
    """

    def get():
        # 上传图片回调
        # print(request.user.developer,request.user)
        # res = request.GET.get("res", "")
        # data = request.GET.get("data", '')
        # if data:
        #     return JsonResponse({"xx": "xxx"})
        # if res:
        #     return HttpResponse(res)
        # if not request.user.developer:
        #     developer = ''
        # else:
        #     developer = request.user.developer
        # # 判断该产品ID是否是此用户所有或者是协同开发
        # # 只判断了该产品是否存在！
        #
        # try:
        #     print('111',developer)
        #     user_related_app = App.objects.filter(developer=developer)
        #     app_id = request.GET.get("ID", "")
        #     user_apps = App.objects.filter(app_id=int(app_id))
        #
        #     if not user_apps:
        #         user_apps = App.objects.filter(developer=DEFAULT_USER, app_id=int(app_id))
        # except Exception as e:
        #     print(e, '有问题')
        #     logging.getLogger('').info("应用出错", str(e))
        #     return HttpResponseRedirect(reverse("product/list"))
        # if not user_apps:
        #     return HttpResponseRedirect(reverse("product/list"))
        # # 判断该产品是否属于这个用户,该产品是否是分享过来的
        # try:
        #     user_login = request.COOKIES['COOKIE_USER_ACCOUNT']
        #     app_ids = request.GET.get("ID", "")
        #     user_appsd = App.objects.filter(developer__developer_account=user_login, app_id=app_ids)
        #     if '@' in user_login:
        #         user_appss = UserGroup.objects.filter(
        #             group_id=[i.group_id for i in App.objects.filter(app_id=app_ids)][0], user_account=user_login)
        #     else:
        #         user_appss = UserGroup.objects.filter(
        #             group_id=[i.group_id for i in App.objects.filter(app_id=app_ids)][0],
        #             user_account=[j.account_email for j in Account.objects.filter(account_id=user_login)][0])
        #     if not user_appsd:
        #         if not user_appss:
        #             return HttpResponseRedirect(reverse("product/list"))
        #         else:
        #             pass
        #     else:
        #         pass1
        # except Exception as e:
        #     print(e, '有问题')
        #     logging.getLogger('').info("应用出错", str(e))
        #     return HttpResponseRedirect(reverse("product/list"))
        app_id = request.GET.get("ID", "")
        user_apps = App.objects.filter(app_id=int(app_id))
        category = {'': ' ', '0': '', '1': '4.3寸屏', '2': '5寸屏', '3': '6.8寸长条屏'}
        categoryed = {'31': '洗碗机', '1': '油烟机', '2': '集成灶', '6': '冰箱', '11': '烤箱', '21': "蒸烤箱", '20': '蒸箱',
                      '25': ' 电压力锅',
                      '26': '电饭煲', '27': '台式小烤箱', '30': '微蒸烤', '0': '其他'}
        # 应用审核状态（0:未审核, 1:审核中, 2:审核通过, -1:审核未通过）
        check_statused = {"0": "未发布", "1": "审核中", "2": "以发布", "-1": "未通过"}
        teams = []
        app_infos = []
        ug = UserGroup.objects.filter(group=user_apps[0].group_id)
        for j in ug:
            teams.append({"email": j.user_account})
        for a in user_apps:
            app_infos = {
                "app_name": a.app_name,  # 产品名称
                "app_factory": a.app_factory_uid,  # 产品对应厂家信息 品牌
                "app_model": a.app_model,  # 产品型号
                "app_category": a.app_category,  # 产品类型
                "device_category": categoryed[str(a.app_device_type)],  # 产品分类
                "app_create_date": a.app_create_date.strftime("%Y-%m-%d"),  # 产品创建时间
                "app_update_date": a.app_update_date.strftime("%Y-%m-%d"),  # 更新时间
                "app_command": a.app_command,  # 指令类型 全指令：是 单指令：否
                "app_describe": a.app_describe,  # 产品描述
                "app_site": a.app_site,  # 产品网址
                "app_logo": a.app_logo  # 产品图片

            }
            tmp = {
                "app_id": a.app_id,
                "app_name": a.app_name,
                "app_update_date": a.app_update_date.strftime("%Y-%m-%d"),
                "is_share": 0,
                "check_status": check_statused[str(a.check_status)],
                "key": a.app_appid[-8:],  # app_screen_size
                "app_screen": category[str(a.app_screen_size)],
                "doc_ui": get_docui(a.app_appid[-8:]),
                "device_category": categoryed[str(a.app_device_type)],
                "teams": teams,
                "create_user": a.developer_id,
                "app_logo": a.app_logo,

            }
        tmp["app_infod"] = app_infos
        print(tmp)
        response = HttpResponse(json.dumps(tmp))
        response["Access-Control-Allow-Origin"] = "*"

        return response

    def find(id, opera_data):
        for i in range(len(opera_data)):
            if str(opera_data[i]['id']) == id:
                return [i, opera_data[i]]
        return []

    def findd(opera_data):
        if len(opera_data) > 1:
            for iosa in opera_data:

                if len(str(iosa)) < 20:
                    opera_data.remove(iosa)
            return opera_data
        else:
            return opera_data

    def findname(names, opera_data):
        names_list = eval(names)
        names = []
        for i in range(len(opera_data)):
            for j in names_list:
                if str(opera_data[i]['Stream_ID']) == j:
                    names.append(opera_data[i]['name'])
        return names

    def post():
        # data_protocol = json.loads(request.body.decode('utf-8')).get('key','')
        # data_protocol_list = json.loads(request.body.decode('utf-8'))
        app_id = request.GET.get("ID", "")
        # cook_ies = request.COOKIES['COOKIE_USER_ACCOUNT']
        post_data = request.POST.get("name")

        id = request.POST.get("id")
        r = Redis3_ClientDB6
        standa = request.POST.get("is_standa", None)  # 标准、自定义
        # 根据ID获取到数据库中的设备配置信息
        app = App.objects.get(app_id=app_id)
        device_conf = gen_app_default_conf(app.app_device_type)
        opera_data = []
        opera_data_new = []
        try:
            if app.device_conf:
                opera_data = json.loads(app.device_conf)
                opera_data_new = opera_data

                opera_data = findd(opera_data)

                if len(opera_data) < 2:
                    pass
                else:
                    opera_data.sort(key=lambda x: int(x.get("id")))
        except Exception as e:
            logging.info("读取数据库中设备配置信息失败", e)
            print(e)
        # 接收页面请求信
        if post_data == 'list':
            # 显示所有列表信息
            page = int(request.POST.get("page", 1))
            rows = int(request.POST.get("rows", 10))
            temp = []
            res_status = r.exists("product_funs" + app_id)
            if res_status:
                data = r.get("product_funs" + app_id)
                data = json.loads(data.decode())
                opera_data = data["rows"]

                opera_data = findd(opera_data)
                # 做判断 区分是否为老产品 根据是否有control来区分

            for line in opera_data:
                # if str(line.get("standa_or_define")) == str(standa):
                temp.append(line)
            data = {'rows': opera_data, 'check_state': app.check_status}
            r.set("product_funs" + app_id, json.dumps(data), 3600 * 24 * 3)
            data["rows"] = temp[(page - 1) * rows:page * rows]
            data["total"] = len(temp) // rows + 1
            data["records"] = len(temp)
            return JsonResponse(data)


        # 获取设备列表
        elif post_data == 'device_table':
            r5 = Redis3_ClientDB5
            key = app.app_appid
            key = key[-8:]
            device_content = DEVICE + "_" + key
            if r5.exists(device_content):
                device_list = r5.get(device_content)
                device_list = json.loads(device_list.decode())
            else:
                device_list = get_device_list(app.app_appid)
                r5.set(device_content, json.dumps(device_list), 1 * 60)
            for k in device_list:
                is_online = device_online(k['ebf_device_id'])
                k["is_online"] = is_online
            return JsonResponse({'data': device_list, 'key': key, 'check_state': app.check_status})
        # 获取工厂列表
        data = request.POST.get("data", "")
        if data == "factory_list":
            factory_list = get_factory_list()
            return JsonResponse({'data': factory_list})
        #  app操作
        res = dict(
            code=10000
        )
        action = request.POST.get("action", "")
        app_id = request.POST.get("app_id", "")
        app_name = request.POST.get("app_name", "")
        app_model = request.POST.get("app_model", "")
        app_describe = request.POST.get("app_describe", "")
        app_site = request.POST.get("app_site", "")
        app_logo = request.POST.get("app_logo", "")
        app_push_url = request.POST.get("app_config_push_url", "")
        app_push_token = request.POST.get("app_config_push_token", "")
        app_command = request.POST.get("app_command", "")
        app_group = request.POST.get("app_group", "")
        app_factory_uid = request.POST.get("app_factory_uid", "")
        if action in ("cancel_release_product", "off_product", "release_product",
                      "update_info", "update_config", "reset_app_secret"):
            if action == "release_product":
                # 发布应用
                ret = release_app(app_id)
                res["data"] = ret
                return HttpResponse(json.dumps(res, separators=(",", ":")))
            elif action == "cancel_release_product":
                # 取消发布
                ret = cancel_release_app(app_id)
                res["data"] = ret
                return HttpResponse(json.dumps(res, separators=(",", ":")))
            elif action == "off_product":
                # 下架
                ret = off_app(app_id)
                res["data"] = ret
                return HttpResponse(json.dumps(res, separators=(",", ":")))
            elif action == "update_info":
                # 更新基本信息
                ret = update_app_info(app_id, app_name, app_model, app_describe, app_site, app_logo,
                                      app_command, app_group, app_factory_uid)
                logging.getLogger('').info("ss_ret" + str(ret))
                if ret:
                    update_app_protocol(app)
                res["data"] = ret
                logging.getLogger('').info("data" + str(res))
                return HttpResponse(json.dumps(res, separators=(",", ":")))
            elif action == "update_config":
                # 更新配置信息
                # 先验证填写的url地址是否正确
                result = verify_push_url(app_push_url, app_push_token)
                if result:
                    ret = update_app_config(app_id, app_push_url, app_push_token)
                    res["data"] = ret
                    return HttpResponse(json.dumps(res, separators=(",", ":")))
                else:
                    return HttpResponse(json.dumps({'code': -2}))
            elif action == "reset_app_secret":
                # 重置密钥
                ret = reset_app_secret(app_id)
                res["data"] = ret
                return HttpResponse(json.dumps(res, separators=(",", ":")))
        return HttpResponse(json.dumps(res, separators=(",", ":")))

    if request.method == "GET":
        return get()

    elif request.method == "POST":
        return post()


@csrf_exempt
def device_list(request):
    app_id = request.GET.get("ID", "")
    # cook_ies = request.COOKIES['COOKIE_USER_ACCOUNT']
    post_data = request.POST.get("name")
    r5 = Redis3_ClientDB5
    app = App.objects.get(app_id=app_id)
    key = app.app_appid
    key = key[-8:]
    device_content = DEVICE + "_" + key
    if r5.exists(device_content):
        device_list = r5.get(device_content)
        device_list = json.loads(device_list.decode())
    else:
        device_list = get_device_list(app.app_appid)
        r5.set(device_content, json.dumps(device_list), 1 * 60)
    for k in device_list:
        is_online = device_online(k['ebf_device_id'])
        k["is_online"] = is_online
    return JsonResponse({'data': device_list, 'key': key, 'check_state': app.check_status})


@csrf_exempt
def upload_file(request):
    try:
        if len(request.FILES.dict()) >= 1:
            f = request.FILES["productImgFile"]
            store = EbStore(CLOUD_TOKEN)
            r = store.upload(f.read(), f.name, f.content_type)
            ret = json.loads(r)
            if ret["code"] == 0:
                print("上传成功")
            else:
                print(ret["msg"])
                logging.getLogger("").info(r["msg"])
            data = ret["data"]
            return HttpResponse(data)
    except Exception as e:
        print(e)
    if request.method == 'POST':

        file = request.FILES.get("file", '')
        post_data = request.POST.get('name', '')
        key = request.POST.get('key', '')
        id = request.POST.get('id', '')
        location = request.POST.get('location', '')
        # action 判断
        action = request.POST.get('action', '')
        app_ids = request.POST.get('app_id', '')
        app_version = request.POST.get('app_version', '')
        appversion_remark = request.POST.get('app_remark', '')
        if action == 'ui_upload':
            try:
                store = EbStore(CLOUD_TOKEN)
                rr = store.upload(file.read(), file.name, file.content_type)
                rr = json.loads(rr)
                r = rr['code']
                print(rr)
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({"code": 1}))
            mobj = App.objects.filter(app_id=int(app_ids))
            print(mobj)
            t = AppVersion.objects.filter(app_id_id=int(app_ids), version_code=app_version, version_name=app_version,
                                          upload_type=int(1))

            if t:
                return HttpResponse(json.dumps({"code": 2}))
            else:

                url_list = rr['data']
                AppVersion.objects.create(app_id=mobj[0], download_url=url_list, version_code=app_version,
                                          version_name=app_version, av_md5='1', create_date=datetime.datetime.utcnow(),
                                          update_date=datetime.datetime.utcnow(), remarks=appversion_remark)
                Message.objects.create(message_content='屏端固件已更新', message_type=int(5),
                                       message_handler_type=int(5),
                                       device_key=key, message_sender='11', message_target='11',
                                       create_date=datetime.datetime.utcnow(),
                                       update_date=datetime.datetime.utcnow())
                return HttpResponse(
                    json.dumps({"code": 0, "url": rr['data'], "filename": file.name, "version": app_version}))
        elif action == 'ui_upload_1':
            try:
                store = EbStore(CLOUD_TOKEN)
                rr = store.upload(file.read(), file.name, file.content_type)
                rr = json.loads(rr)
                r = rr['code']
                print(rr)
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({"code": 1}))
            mobj = App.objects.filter(app_id=int(app_ids))
            print(mobj)
            t = AppVersion.objects.filter(app_id_id=int(app_ids), version_code=app_version, version_name=app_version,
                                          upload_type=int(2))

            if t:
                return HttpResponse(json.dumps({"code": 2}))
            else:

                url_list = rr['data']
                AppVersion.objects.create(app_id=mobj[0], download_url=url_list, version_code=app_version,
                                          version_name=app_version, av_md5='1', create_date=datetime.datetime.utcnow(),
                                          update_date=datetime.datetime.utcnow(), remarks=appversion_remark,
                                          upload_type=int(2))
                Message.objects.create(message_content='屏端固件已更新', message_type=int(5),
                                       message_handler_type=int(5),
                                       device_key=key, message_sender='11', message_target='11',
                                       create_date=datetime.datetime.utcnow(),
                                       update_date=datetime.datetime.utcnow())
                return HttpResponse(
                    json.dumps({"code": 0, "url": rr['data'], "filename": file.name, "version": app_version}))
        elif action == 'firmware':
            files = request.FILES.get("files", '')
            print(file, files)
            try:
                # 处理上传的pkg文件
                store = EbStore(CLOUD_TOKEN)
                rr = store.upload(file.read(), file.name, file.content_type)
                rr = json.loads(rr)
                r = rr['code']
                print(rr)
                # 处理上传的图片
                stores = EbStore(CLOUD_TOKEN)
                rp = stores.upload(files.read(), files.name, files.content_type)
                rp = json.loads(rp)
                rpp = rp['code']
                print(rpp)
            except Exception as e:
                print(e)
                return HttpResponse(json.dumps({"code": 1}))
            sizes = request.POST.get('sizes', '')
            fobj = Firmware.objects.create(firmware_size=int(sizes), firmware_name=appversion_remark,
                                           firmware_image=rp['data'],
                                           firmware_version=app_version, firmware_url=rr['data'],
                                           firmware_create_date=datetime.datetime.utcnow(),
                                           firmware_update_date=datetime.datetime.utcnow())
            if fobj:
                return HttpResponse(json.dumps({"code": 0}))
            else:
                return HttpResponse(json.dumps({"code": 2}))
        else:
            t = int(id) + int(1)
            user1 = request.COOKIES['COOKIE_USER_ACCOUNT']
            b = UserGroup.objects.filter(group__create_user=user1)
            a = App.objects.filter(app_appid__endswith=key)
            email_list = []
            app_name = ''
            developer = ''
            group_id = ''
            for i in a:
                app_name = i.app_name
                group_id = i.group_id
                developer = i.developer_id
            try:
                b = UserGroup.objects.filter(group__group_id=group_id)
                for i in b:
                    email_list.append(i.user_account)
            except Exception as e:
                print(e)
            try:
                # 上传UI文件
                if post_data == 'upload':

                    try:
                        store = EbStore(CLOUD_TOKEN)
                        rr = store.upload(file.read(), file.name, file.content_type)
                        rr = json.loads(rr)
                        r = rr['code']
                        print(rr)
                    except Exception as e:
                        print(e)
                        return HttpResponse(json.dumps({"code": 1}))
                    list_url = rr['data']
                    datas = get_ui_static_conf(key, list_url, id, file.name, user1)
                    product_name = app_name + '上传更新提示'
                    # 需要修改
                    print('id', t)
                    if DocUi.objects.filter(ui_key=key, ui_upload_id=t):
                        next_stemp = [str(i.ui_plan) for i in
                                      DocUi.objects.filter(ui_key=key, ui_upload_id=t)][0]
                    else:
                        next_stemp = '该产品即将量化'
                    # 发送邮件通知send_product_process_email(title, product_name, process_name, next_process, handler, to_user, detail_url, action)
                    try:
                        send_product_process_email(product_name, app_name, file.name, next_stemp, user1, email_list,
                                                   location, "submit")
                        Message.objects.create(message_content=BOOK[id] + ':' + '已上传', message_type=int(4),
                                               message_handler_type=int(4),
                                               device_key=key, message_sender='11', message_target='11',
                                               create_date=datetime.datetime.utcnow(),
                                               update_date=datetime.datetime.utcnow())
                    except Exception as e:
                        print(e)
                    dd = ''
                    p = DocUi.objects.filter(ui_key=key, ui_upload_id=id)
                    for i in p:
                        dd = i.ui_content

                    return HttpResponse(json.dumps(datas))
                else:
                    r = 1
            except Exception as e:
                r = 1
                print(e)
        return HttpResponse(json.dumps({"code": 0}))
