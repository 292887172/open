# !/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from model.center.app import App
from django.db import models
__author__ = 'rdy'


class AppVersion(models.Model):
    """
    ebt_app_version应用版本表
    """
    # 版本编号
    av_id = models.AutoField(primary_key=True, db_column='ebf_av_id')
    # 应用编号
    app_id = models.ForeignKey(App, null=True, db_column='ebf_app_id', related_name='app_version_related_app')
    # 版本号
    version_code = models.CharField(max_length=64, db_column='ebf_av_version_code')
    # 版本名称
    version_name = models.CharField(max_length=128, db_column='ebf_av_version_name')
    # 下载地址
    download_url = models.TextField(null=True, db_column='ebf_av_download_url')
    # 是否提示
    is_notify = models.CharField(max_length=16, default='yes', db_column="ebf_av_is_notify")
    # 是否强制升级
    is_force = models.CharField(max_length=16, default='no', db_column="ebf_av_is_force")
    # 版本文件大小
    av_size = models.CharField(max_length=32, null=True, db_column="ebf_av_size")
    # 版本备注
    remarks = models.TextField(null=True, db_column='ebf_av_remarks')
    # 版本签名
    av_md5 = models.CharField(max_length=128, default='', db_column="ebf_av_md5")
    # 文件md5值
    file_md5 = models.CharField(max_length=128, default='', db_column="ebf_file_md5")
    # 版本类型
    av_type = models.IntegerField(max_length=3, default=0, db_column='ebf_av_type')
    # 最小版本
    min_version = models.IntegerField(max_length=11, default=0, db_column='ebf_min_version')
    # 更新时间，auto_now_add,为添加时的时间，更新对象时不会有变动,auto_now无论是你添加还是修改对象，时间为你添加或者修改的时间
    update_date = models.DateTimeField(auto_now=True, default=datetime.datetime.utcnow, db_column='ebf_av_updatedate')
    # 创建时间
    create_date = models.DateTimeField(auto_now_add=True, default=datetime.datetime.utcnow,
                                       db_column='ebf_av_createdate')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_app_version'
        verbose_name = 'app版本信息表'
