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
            m = Message(message_content=content, message_type=2, message_sender=sender, message_target='', is_read=0,
                        create_date=datetime.datetime.utcnow(), update_date=datetime.datetime.utcnow())
            m.save()
        elif type == 'user':
            # 用户消息
            m = Message(message_content=content, message_type=1, message_sender=sender, message_target=target, is_read=0,
                        create_date=datetime.datetime.utcnow(), update_date=datetime.datetime.utcnow())
            m.save()
    except Exception as e:
        print(e)


def read_user_message(target,type):
    """
    读取用户消息
    :param target:
    :param type:
    :param sender:
    :return:
    """
    try:
        m = []
        if type == 'sys':
            m = Message.objects.filter(message_sender=target).order_by('-update_date')[0]
        elif type == 'user':
            m = Message.objects.filter(message_target=target).order_by('-update_date')[0:3]
        if m:
            return m
        else:
            return ''
    except Exception as e:
        print(e)



def get_sys_message(sender):
    try :
        m = Message.objects.get(message_sender=sender)
        if m:
            return m
        else:
            return ''
    except Exception as e:
        print(e)

