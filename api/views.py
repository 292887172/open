# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse, JsonResponse
from common.mysql_helper import query_data, get_ui_base_conf, query_ui_conf
import json

# Create your views here.


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
                    new_functions.append({'name': i['name'], "id": i['id'], 'title': i['title']})

                json.loads(a['ebf_pc_conf'])['functions'] = new_functions

                new_list = {'name':  json.loads(a['ebf_pc_conf'])['name'], 'key': json.loads(a['ebf_pc_conf'])['key'],
                            "model":  json.loads(a['ebf_pc_conf'])['model'], "functions": new_functions}
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
        if device_id:
            if device_conf:
                back_data = get_ui_base_conf(device_id, device_conf)
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
            back_data = query_ui_conf(device_key)
            if back_data != 'error':
                return HttpResponse((back_data['ebf_page_conf']), content_type="application/json")
