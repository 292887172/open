# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'achais'
import datetime
from model.center.message import Message
import logging


def save_user_message(target, content, type, sender):
    """
    用户消息
    :param target:
    :param content:
    :param type:
    :param sender:
    :return:
    """
    try:
        if type == 'sys':
            # 系统消息
            m = Message(message_content=content, message_type=2, message_sender='53iqadmin', message_target='', is_read=0,
                        create_date=datetime.datetime.utcnow(), update_date=datetime.datetime.utcnow())
            m.save()
        elif type == 'user':
            # 用户消息
            m = Message(message_content=content, message_type=2, message_sender=sender, message_target=target, is_read=0,
                        create_date=datetime.datetime.utcnow(), update_date=datetime.datetime.utcnow())
            m.save()
    except Exception as e:
        print(e)
