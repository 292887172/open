# !/bash/bin/env python
# -*- coding: utf-8 -*-
import json

import requests
import logging,datetime
from base.connection import ReleaseApiMongoDBHandler
from common.app_api_helper import remove_control_id
__author__ = 'rdy'
MSG_NOTIFY_URL = "https://api.53iq.com/1/message/push?access_token=%s"


def send_wxlogin_data(did, openid, unionid, token):
    access_token = 'SvycTZu4hMo21A4Fo3KJ53NNwexy3fu8GNcS8J0kiqaQoi0XvgnvXvyv5UhW8nJj_551657047c2d5d0fd8a30e999b4f7b20f5ea568e'
    url = MSG_NOTIFY_URL % access_token

    data = dict(
        msg_type=str('wechat_login'),
        device_id=str(did),
        msg_data={
            'openid': openid,
            'unionid': unionid,
            'token': token
        },
        create_time=1,
        sender=''
    )
    touser = [did]
    message = [data]
    data = dict(
        touser=touser,
        message=message
    )
    r = requests.post(url, data=json.dumps(data).replace("'", '"'), timeout=8)
    logging.getLogger('').info("推送微信登录消息结果：" + r.text)
    print(r.text)


def deal_wxlogin_data(unionid, did):

    url1 = "http://wechat.53iq.com/tmp/user/info"
    res = requests.post(url1, params={'unionid': unionid,
                                      'access_token': '38DZq4MHYCA7N6qIA7Ap0MvSv7etzkAA3BKbgCrMcP8X6C458pm'
                                                      'cM8Ae8FjqBUl4_e1c54d31720f1e35f7967d2d9b3e559183'
                                                      '875cb0',
                                      }).json()
    db = ReleaseApiMongoDBHandler().db
    # 保存当前该中控屏登录者关系
    c = db.devices.find_one({'_id': did})
    if c:
        db.devices.update({'_id': did}, {'$set': {'device_type': -2, 'tags': ['中控'], 'login_user': unionid,
                                                         'login_date': datetime.datetime.utcnow()}})
    else:
        tmp = {
            '_id': did,
            'device_type': -2, '_updated': datetime.datetime.utcnow(),
            'tags': ['中控'], 'login_user':  unionid, 'master':  unionid,
            'login_date': datetime.datetime.utcnow(), 'danger': 0
        }
        db.devices.insert(tmp)

    # 移除中控原有绑定关系
    d = db.devices.find({'controller': {'$in': [did]}})
    for i in d:
        device_id = i['_id']
        c_id = i['controller']
        try:
            c_id.remove(did)
            c_id = list(set(c_id))
            if len(c_id) > 10:
                del c_id[0]
        except ValueError:
            pass

        db.devices.update({'_id': device_id}, {"$set": {'controller': c_id}})

    # 建立绑定关系
    u = db.users.find_one({"unionid": unionid})
    if u:
        t_openid = u['openid']
        d = db.devices_users.find({'openid': t_openid, 'active': 1})
        for i in d:
            device_id = i['did']
            d1 = db.devices.find_one({"_id": device_id})
            try:
                if d1:
                    c_id = d1['controller']
                    c_id.append(did)
                    c_id = list(set(c_id))
                    if len(c_id) > 10:
                        del c_id[0]
            except KeyError:
                c_id = [did]
                pass
            db.devices.update({'_id': device_id}, {"$set": {'controller': c_id}})
            remove_control_id(device_id)

    if res['code'] == 0:
        token = res['data']['token']
        topic = res['data']['mosquitto_topic']
        openid = str(topic).split("/")[-1]
        logging.getLogger('').info("微信登录token：" + str(token)+">>openid:"+openid)
        send_wxlogin_data(did, openid, unionid, token)
        return token, openid


if __name__ == '__main__':
    a = deal_wxlogin_data('oixkIuJaT3J3AgwVmJx2Y4D81CdM', '100023362')
    print(a)
    # db = ReleaseApiMongoDBHandler().db
    #
    # u = db.users.find_one({"unionid": "oixkIuJaT3J3AgwVmJx2Y4D81CdM"})
    #
    # print(u['openid'])
