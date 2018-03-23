# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'gmy'

import datetime

from django.db import models

class Device_Fun(models.Model):
    """
    ebt_device_function 功能审核状态表
    """

    # ebf_df_id 编号
    df_id = models.AutoField(primary_key=True, db_column='ebf_df_id')
    # ebf_device_key 该功能对应App的key
    device_key = models.CharField(max_length=64, db_column='ebf_device_key')
    # ebf_device_function 该功能对应的值
    device_function = models.CharField(max_length=64, db_column='ebf_device_function')
    # ebf_df_check_status 该功能审核状态（1:审核中, 2:审核通过, -1:审核未通过）
    df_check_status = models.IntegerField(max_length=2, default=0, db_column='ebf_df_check_status')
    # ebf_df_update_date 该功能更新时间
    df_update_date = models.DateTimeField(default=datetime.datetime.utcnow(), db_column='ebf_df_update_date')
    # ebf_df_create_date 该功能创建时间
    df_create_date = models.DateTimeField(default=datetime.datetime.utcnow(), db_column='ebf_df_create_date')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_device_function'
        verbose_name = '功能审核'
