# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'rdy'

from model.center.developer import Developer
from django.core.paginator import Paginator
from base.convert import utctime2localtime
from base.convert import date2ymdhms
from base.const import ConventionValue

import datetime
import logging

_convention = ConventionValue()


def create_developer(company, company_url, company_address, company_scale, contact_name, contact_role, contact_mobile,
                     contact_phone, contact_qq, contact_email, factory_name, factory_uuid, user, user_from):
    """
    注册开发者帐号
    :param company:
    :param company_url:
    :param company_address:
    :param company_scale:
    :param contact_name:
    :param contact_role:
    :param contact_mobile:
    :param contact_phone:
    :param contact_qq:
    :param contact_email:
    :param factory_name:
    :param factory_uuid:
    :return:
    """

    try:
        # 开发者帐号：  由开发者来源+下划线+账号拼接起来
        # 开发者来源： （1：平台用户，2：设备管理系统厂商，3：qq）
        if user_from == '53iq':
            dev_from = 1
            dev_id = '1_' + user
        else:
            dev_from = 2
            dev_id = '2_' + user
        dev = Developer(
            developer_id=dev_id,
            developer_account=user,
            developer_factory=factory_name,
            developer_symbol=factory_uuid,
            developer_from=dev_from,
            developer_inc=company,
            developer_site=company_url,
            developer_address=company_address,
            developer_person=company_scale,
            developer_realname=contact_name,
            developer_job=contact_role,
            developer_email=contact_email,
            developer_mobile=contact_mobile)
        dev.save()
        return dev_id
    except Exception as e:
        logging.getLogger('').info(str(e))

    return ""


def denied_developer(developer_id, remark):
    """
    开发者审核不通过
    :param developer_id:
    :param remark:
    :return:
    """
    try:
        if not remark:
            return False
        update_line = Developer.objects.filter(developer_id=developer_id) \
            .update(developer_check_status=_convention.DEVELOPER_CHECK_FAILED, developer_check_remarks=remark,
                    developer_update_date=datetime.datetime.utcnow())
        if update_line > 0:
            return True
        else:
            return False
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def pass_developer(developer_id):
    """
    开发者审核通过
    :param developer_id:
    :return:
    """
    try:
        update_line = Developer.objects.filter(developer_id=developer_id) \
            .update(developer_check_status=_convention.DEVELOPER_CHECKED,
                    developer_update_date=datetime.datetime.utcnow())
        if update_line > 0:
            return True
        else:
            return False
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def toggle_forbid_developer(developer_id):
    """
    切换开发者禁用状态
    :param developer_id:
    :return:
    """
    try:
        developer = Developer.objects.get(developer_id=developer_id)
        update_line = Developer.objects.filter(developer_id=developer_id) \
            .update(
            developer_is_forbid=_convention.DEVELOPER_UN_FORBID if developer.developer_is_forbid
            else _convention.DEVELOPER_IS_FORBID,
            developer_update_date=datetime.datetime.utcnow())
        if update_line > 0:
            return True
        else:
            return False
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def fetch_checking_developer_data(page, limit, order_by_names):
    """
    获取审核状态中的开发者
    :param page:
    :param limit:
    :param order_by_names:
    :return:
    """
    try:
        pager = Paginator(Developer.objects.filter(developer_check_status=_convention.DEVELOPER_CHECKING)
                          .order_by(order_by_names), int(limit))
        developers = pager.page(int(page))
        total_count = pager.count
        data = []
        for developer in developers:
            d = dict(
                id=developer.developer_id,
                factory=developer.developer_factory,
                inc=developer.developer_inc,
                site=developer.developer_site,
                job=developer.developer_job,
                person=developer.developer_person,
                createtime=date2ymdhms(utctime2localtime(developer.developer_update_date))
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


def fetch_developer_list_data(page, limit, order_by_names):
    """
    获取所有开发者列表
    :param page:
    :param limit:
    :param order_by_names:
    :return:
    """
    try:
        pager = Paginator(Developer.objects.filter(developer_check_status=_convention.DEVELOPER_CHECKED)
                          .order_by(order_by_names), int(limit))
        developers = pager.page(int(page))
        total_count = pager.count
        data = []
        for developer in developers:
            d = dict(
                id=developer.developer_id,
                is_forbid=developer.developer_is_forbid,
                factory=developer.developer_factory,
                inc=developer.developer_inc,
                site=developer.developer_site,
                job=developer.developer_job,
                person=developer.developer_person,
                createtime=date2ymdhms(utctime2localtime(developer.developer_update_date))
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


def fetch_developer_data(developer_id):
    """
    获取开发者信息
    :param developer_id:
    :return:
    """
    try:
        developer = Developer.objects.get(developer_id=developer_id)
        if developer:
            return developer
        else:
            return None
    except Exception as e:
        logging.getLogger("").error(e)
        return None
