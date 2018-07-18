# -*- coding: utf-8 -*-
import codecs
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from base.connection import ReleaseApiMongoDBHandler
from base.const import ConventionValue
from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
#import markdownfrom model.center.doc_menu import DocMenu
from common.message_helper import *
from conf.message import *
from model.center.doc_menu import DocMenu

from open import settings
_convention = ConventionValue()


def is_mobile(request):
    """
    判断浏览器是否为移动设备浏览器
    :param request:
    :return:
    """
    if "HTTP_USER_AGENT" in request.META.keys():
        agent = request.META["HTTP_USER_AGENT"].lower()
        view = request.REQUEST.get("view", "")
        if "android" in agent or "mobile" in agent or "iemobile" in agent:
            if view != "pc":
                return True
    return False


def home(request):
    template = "home/home.html"
    if is_mobile(request):
        template = "home/home-mobile.html"
    try:
        account = request.user.account_id
        if account == "admin":
            uri = "/center"
        else:
            uri = "/product/console"
        return HttpResponseRedirect(uri)
    except Exception as e:
        print(e)
    return render(request, template, locals())


def smart_menu(request):

    return render(request, "home/smart-menu.html", locals())


def guide(request):
    try:
        if request.user.account_type == _convention.USER_IS_ADMIN:
            return HttpResponseRedirect(reverse("admin_center"))
    except AttributeError:
        pass
    return render(request, "home/guide.html", locals())


def test(request):
    # code = codecs.open(settings.BASE_DIR + "/static/file/BUILD.md", "r", "utf-8").read()
    # ret = markdown.markdown(code, ['codehilite'])
    return render(request, "home/test.html", locals())


@csrf_exempt
def status(request):
    """
    :param request: 获取厨房用户状态
    :return:
    """
    import pymongo
    from django.http.response import JsonResponse
    client = pymongo.MongoClient('s72.53iq.com', 27017)
    db = client.ebdb_smartsys
    collection = db.ebc_kitchen_user_stats
    date = request.GET.get("date")
    try:
        temp = date.split("-")
        temp[1] = str(int(temp[1]))
        temp[2] = str(int(temp[2]))
        date1 = ''.join(temp)
        temp = datetime.datetime.strptime(date, '%Y-%m-%d')
        date3 = temp - datetime.timedelta(hours=8)
        date4 = temp + datetime.timedelta(hours=16)
        req_code = collection.find({"action": "get_wechat_code", "day_time": date1}).count()
        scan_code = collection.find({"action": "scan_qr", "date": {"$gte": date3, "$lt": date4}}).count()
        down_code = collection.find({"action": "download_app", "date": {"$gte": date3, "$lt": date4}}).count()
        ret = {
            "req_code": req_code,
            "scan_code": scan_code,
            "down_code": down_code
            }
        return JsonResponse(ret)
    except Exception as e:
        print("获取秦秋次数出错:", e)
    return render(request, "home/kitchen_status.html", locals())


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


@csrf_exempt
def app_user(request):
    if request.method == 'POST':
        db = ReleaseApiMongoDBHandler().db
        # page = request.POST.get('page')
        from_dict = {'ios': 'ios日记', 'zncf': '通用App', 'md':'美大厨房', 'arda': '安德厨房', 'kinde': '金帝厨房', 'app': '厨房日记'}
        phone_user = db.ebc_app_users.find({}).sort([('_updated', -1)]).skip(0).limit(30)
        wx_user = db.users.find({}).sort([('_updated', -1)]).skip(0).limit(30)
        total_data = []
        for i in phone_user:
            nickname = i['phone']
            account_id = i['account_id']
            updated = i['_updated']

            t = {
                'nickname': nickname,
                'openid': account_id,
                'from': from_dict.get(i.get('source'), ''),
                'is_bind_device': '',
                'is_control': '',
                'date': (updated+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%I:%S")
            }
            total_data.append(t)
        for j in wx_user:
            nickname = j['nickname']
            openid = j['openid']
            updated = j['_updated']
            t = {
                'nickname': nickname,
                'openid': openid,
                'from': from_dict.get(j.get('source'), ''),
                'is_bind_device': '',
                'is_control': '',
                'date': (updated+datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%I:%S")
            }
            total_data.append(t)
        for z in total_data:
            du = db.devices_users.find({"openid": z.get("openid")})
            if du.count() > 0:
                is_bind_device = True
            else:
                is_bind_device = False
            if is_bind_device:
                rd = db.record.find({"user": z.get("openid")})
                if rd.count() > 0:
                    is_control = True
                else:
                    is_control = False
            else:
                is_control = False
            z['is_bind_device'] = is_bind_device
            z['is_control'] = is_control

        return JsonResponse({'code': 0, 'data': total_data})
    else:
        return render(request, "home/app-user.html", locals())