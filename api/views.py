# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, JsonResponse
from common.mysql_helper import query_data, get_ui_base_conf, query_ui_conf
import json
import logging
import datetime
# Create your views here.
from model.center.account import Account
from model.center.account_info import AccountIfo


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

                        new_functions.append({'name': i['name'], "id": i['id'], 'title': i['title'],'values':i['values'],'type':i['type'],'permission':i['permission']})
                json.loads(a['ebf_pc_conf'])['functions'] = new_functions

                new_list = {'name':  json.loads(a['ebf_pc_conf'])['name'], 'key': json.loads(a['ebf_pc_conf'])['key'],
                            "model":  json.loads(a['ebf_pc_conf'])['model'], "functions": new_functions,
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
                back_data = get_ui_base_conf(device_id, device_conf,cook_ies)
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
                back_data = query_ui_conf(device_key)
                if back_data and back_data != 'error':
                    return HttpResponse((back_data['ebf_page_conf']), content_type="application/json")
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
                logging.getLogger('').info(' 创建用户邮寄地址信息失败'+str(e))
            return JsonResponse({'code': -2, 'msg': 'account save error'})
        else:
            return JsonResponse({'code': -3, 'msg': 'miss parameters'})
    else:
        return JsonResponse({'code': -1, 'msg': 'error request method'})
