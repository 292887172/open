# !/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from model.center.account import Account
from django.db import models
__author__ = 'rdy'


class AccountIfo(models.Model):
    """
    用户账户表
    """
    # 用户信息id
    ac_info_id = models.AutoField(primary_key=True, db_column='ebf_account_info_id')
    # 用户帐号
    account_id = models.ForeignKey(Account, null=True, db_column='ebf_account_id', related_name='info_related_account')
    # 联系人姓名
    contact_name = models.CharField(max_length=64, null=True, db_column='ebf_account_contact_name')
    # 联系人电话
    contact_phone = models.CharField(max_length=32, null=True, db_column='ebf_account_contact_phone')
    # 手机号
    contact_address = models.CharField(max_length=512, null=True, db_column='ebf_account_contact_address')
    # 帐号信息创建时间
    account_create_date = models.DateTimeField(default=datetime.datetime.utcnow, db_column='ebf_account_info_create_date')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_account_info'
        verbose_name = '用户账号信息'
