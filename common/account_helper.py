# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'achais'

from model.center.account import Account
from django.core.paginator import Paginator
from base.const import ConventionValue
from base.convert import utctime2localtime
from base.convert import date2ymdhms
from base.crypto import md5_en

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
                is_forbid=user.account_is_forbid,
                createtime=date2ymdhms(utctime2localtime(user.account_create_date))
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