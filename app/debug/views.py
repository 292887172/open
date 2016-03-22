import json
import re
from urllib.parse import urlparse
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import requests
from common.debug_helper import get_debug_api
from common.protocol import send_cmd
from util.logutil import print_log

__author__ = 'sunshine'


@csrf_exempt
def debug_interface(request):
    """
    调试接口
    :param request:
    :return:
    """
    if request.method == 'GET':
        api = get_debug_api()
        return render(request, 'debug/debug_interface.html', locals())
    if request.method == 'POST':
        method = request.POST.get('method', None)
        api_url = request.POST.get('api_url', None)

        if method is None:
            return HttpResponse(json.dumps({'code': 41002, 'msg': "missing request method param!"}))
        if api_url is None:
            return HttpResponse(json.dumps({'code': 41003, 'msg': "missing request url param!"}))

        args = dict()
        for key in request.POST:
            if key != 'method' and key != 'api_url':
                args[key] = request.POST[key]
        args['version'] = '1'
        try:
            url = urlparse(api_url)
            if url.scheme is None:
                api_url = 'http://'+api_url
            # 解析url中的{arg}参数
            pattern = re.compile(r"\{(.*?)\}")
            params = re.findall(pattern, api_url)
            if params:
                try:
                    params = tuple([args[key] for key in params])
                except KeyError as e:
                    return HttpResponse(json.dumps({'code': 46004, 'msg': "缺少参数%s" % str(e)}))
                api_url = re.sub(pattern, '%s', api_url)
                api_url = api_url % params
            if method == 'POST':
                resp = requests.post(api_url, data=args, timeout=10)
            elif method == 'GET':
                resp = requests.get(api_url, params=args, timeout=10)
            elif method == 'PUT':
                resp = requests.put(api_url, data=args, timeout=10)
            elif method == 'DELETE':
                resp = requests.delete(api_url, timeout=10)
            else:
                return HttpResponse(json.dumps({'code': 46001, 'msg': "请求方式错误"}))
            return HttpResponse(resp.text)
        except ValueError as e:
            print_log(e)
            return HttpResponse(json.dumps({'code': 46002, 'msg': "请求错误"}))
        except Exception as e:
            print_log(e)
            return HttpResponse(json.dumps({'code': 46001, 'msg': str(e)}))


@csrf_exempt
def debug_device(request):
    """
    调试设备
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'debug/debug_device.html', locals())
    elif request.method == 'POST':
        token = request.POST.get('token', None)
        cmd = request.POST.get('cmd', None)
        if token and cmd:
            result = send_cmd(cmd)
            if isinstance(result, str):
                result = json.loads(result)
            return HttpResponse(json.dumps(result))
        else:
            return HttpResponse(json.dumps({"value": "", "status": -1, "msg": "参数错误"}))
