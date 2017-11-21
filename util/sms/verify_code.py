# !/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from base.connection import RedisBaseHandler
from conf.redisconf import SMS_CHECK_CODE_PREFIX

__author__ = 'rdy'


def verify_sms_code(user_id, code):
    """
    验证用户输入的短信验证码
    :param: request:
    :return:
    """
    r = RedisBaseHandler().client
    if code and user_id:
        save_code = r.get(SMS_CHECK_CODE_PREFIX + user_id)
        if save_code:
            save_code = save_code.decode()
            if save_code == code:
                # 注册成功跳转到注册成功页面
                url = reverse('center')
                return {'status': 1, 'url': url}
            else:
                return {'status': 2, 'error': '验证码错误'}
        else:
            return {'status': 3, 'error': '验证码过期'}
    else:
        return {'status': 0, 'error': '参数错误'}
