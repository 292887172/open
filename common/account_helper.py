# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'achais'
import datetime
from model.center.account import Account
from model.center.auto_login import AutoLogin
from django.core.paginator import Paginator
from base.const import ConventionValue
from base.convert import utctime2localtime
from base.convert import date2ymdhms
from base.crypto import md5_en
import base64
import logging

_convention = ConventionValue()


def toggle_forbid_user(account_id):
    """
    切换用户禁用状态
    :param account_id:
    :return:
    """
    try:
        user = Account.objects.get(account_id=account_id)
        update_line = Account.objects.filter(account_id=account_id) \
            .update(
            account_is_forbid=_convention.ACCOUNT_UN_FORBID if user.account_is_forbid
            else _convention.ACCOUNT_IS_FORBID)
        if update_line > 0:
            return True
        else:
            return False
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def fetch_user_list_data(page, limit, order_by_names):
    """
    获取所有用户列表
    :param page:
    :param limit:
    :param order_by_names:
    :return:
    """
    try:
        pager = Paginator(Account.objects.all().order_by(order_by_names), int(limit))
        users = pager.page(int(page))
        total_count = pager.count
        data = []
        for user in users:
            d = dict(
                id=user.account_id,
                f=user.account_from_id,
                t=user.account_type,
                email=user.account_email,
                phone=user.account_phone,
                nickname=user.account_nickname,
                is_forbid=user.account_is_forbid,
                createtime=date2ymdhms(user.account_create_date)
            )
            data.append(d)
        result = dict(
            totalCount=total_count,
            items=data
        )
        return result
    except Exception as e:
        logging.getLogger("").error(e)
        return ""


def change_user_pwd(user_id, new_pwd):
    """
    修改用户密码
    :param user_id:
    :param new_pwd:
    :return:
    """
    try:
        user = Account.objects.get(account_id=user_id)
        user.password = md5_en(new_pwd)
        user.save()
    except Exception as e:
        print(e)


def update_user_login_data(user_id, pwd, token, ip, action):
    """
    更新用户的登录信息
    :param user_id:
    :param pwd:
    :param token:
    :param ip:
    :param action
    :return:
    """

    if action == 'save':
        pwd = base64.b64encode(pwd)
        try:
            al = AutoLogin.objects.get(al_account_id=user_id)
            al.al_account_pwd = pwd
            al.al_token = token
            al.al_login_ip = ip
            al.al_update_date = datetime.datetime.utcnow()
            al.save()
        except Exception as e:
            print(e)
            al = AutoLogin(al_account_id=user_id, al_account_pwd=pwd, al_token=token, al_login_ip=ip,
                           al_create_date=datetime.datetime.utcnow(), al_update_date=datetime.datetime.utcnow())
            al.save()
    elif action == 'delete':
        try:
            AutoLogin.objects.filter(al_account_id=user_id).delete()
        except Exception as e:
            print(e)
