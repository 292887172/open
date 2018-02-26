# !/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import os
import shutil

from base.connection import ReleaseApiMongoDBHandler
from util.email.send_email_code import send_mail


def test_name():

    root = "/Users/zhanlingjie/Documents/mypython/Git/open"

    for dirpath, dirnames, filenames in os.walk(root):
        for filepath in filenames:
            if '__' in dirpath:
                try:
                    shutil.rmtree(dirpath)
                    print(dirpath)
                except Exception as e:
                    pass


# def Square(num):
#     temp = str(num)
#     n = 0
#     for index,value in enumerate(temp):
#         if index == len(temp)-1:
#             print(value+'*'+value, end='')
#         else:
#             print(value+'*'+value+' + ', end='')
#         a= int(value)
#         n += a*a
#     print(' = ',n,)
#     if n == 1:
#         return 1
#     return Square(n)
# def countBits(self, num):
#         """
#         :type num: int
#         :rtype: List[int]
#         """
#         list = []
#         for i in range(0,num+1):
#             count = bin(i).count('1')
#             list.append(count)
#         return list


if __name__=="__main__":
    db = ReleaseApiMongoDBHandler().db
    # page = request.POST.get('page')
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
            'from': i.get('source'),
            'is_bind_device': '',
            'is_control': '',
            'date': updated
        }
        total_data.append(t)
    for j in wx_user:
        nickname = j['nickname']
        openid = j['openid']
        updated = j['_updated']
        t = {
            'nickname': nickname,
            'openid': openid,
            'from': j.get('source'),
            'is_bind_device': '',
            'is_control': '',
            'date': updated
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
    print(total_data)