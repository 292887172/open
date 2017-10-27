# !/bash/bin/env python
# -*- coding: utf-8 -*-
import json

import requests
import logging

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


def deal_wxlogin_data(unionid, did):

    url1 = "http://wechat.53iq.com/tmp/user/info"
    res = requests.post(url1, params={'unionid': unionid,
                                      'access_token': '38DZq4MHYCA7N6qIA7Ap0MvSv7etzkAA3BKbgCrMcP8X6C458pm'
                                                      'cM8Ae8FjqBUl4_e1c54d31720f1e35f7967d2d9b3e559183'
                                                      '875cb0',
                                      }).json()

    if res['code'] == 0:
        token = res['data']['token']
        topic = res['data']['mosquitto_topic']
        openid = str(topic).split("/")[-1]
        logging.getLogger('').info("微信登录token：" + str(token)+">>openid:"+openid)
        send_wxlogin_data(did, openid, unionid, token)
        return token, openid


if __name__ == '__main__':
    a = deal_wxlogin_data('oixkIuJaT3J3AgwVmJx2Y4D81CdM', '100000319')
    print(a)
