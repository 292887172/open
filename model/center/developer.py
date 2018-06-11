import datetime


from django.db import models

__author__ = 'rdy'


class Developer(models.Model):
    """
    开发者表
    """
    # 开发者帐号（开发者来源+下划线+账号拼接起来）
    developer_id = models.CharField(primary_key=True, max_length=128, db_column='ebf_developer_id')
    # 用户帐号
    developer_account = models.CharField(max_length=1024, db_column='ebf_developer_account')
    # 厂商名称
    developer_factory = models.CharField(max_length=128, null=True, db_column='ebf_developer_factory')
    # 厂商标识（一定不能为空）
    developer_symbol = models.CharField(max_length=1024, db_column='ebf_developer_symbol')
    # 开发者来源 （1：平台用户，2：设备管理系统厂商，3：微信）
    developer_from = models.IntegerField(max_length=2, default=1, db_column='ebf_developer_from')
    # 开发者公司/团队名称
    developer_inc = models.CharField(max_length=64, db_column='ebf_developer_inc')
    # 开发者公司/团队网址
    developer_site = models.CharField(max_length=2048, null=True, db_column='ebf_developer_site')
    # 开发者公司/团队所在地
    developer_address = models.CharField(max_length=2048, null=True, db_column='ebf_developer_address')
    # 开发者团队人数
    developer_person = models.IntegerField(null=True, db_column='ebf_developer_person')
    # 联系人姓名
    developer_realname = models.CharField(max_length=32, db_column='ebf_developer_realname')
    # 联系人职务
    developer_job = models.CharField(max_length=64, null=True, db_column='ebf_developer_job')
    # 用户邮箱
    developer_email = models.CharField(max_length=1282, null=True, db_column='ebf_developer_email')
    # 用户手机号
    developer_mobile = models.CharField(max_length=32, null=True, db_column='ebf_developer_mobile')
    # 操作类型（1：添加，2：修改，3：删除）
    developer_action = models.IntegerField(max_length=2, null=True, db_column='ebf_developer_action')
    # 审核状态（0：审核中，1：审核通过，-1：审核未通过）
    developer_check_status = models.IntegerField(max_length=2, default=1, db_column='ebf_developer_check_status')
    # 审核备注
    developer_check_remarks = models.CharField(max_length=1024, null=True, db_column='ebf_developer_check_remarks')
    # 是否禁用（0：启用，1：禁用）
    developer_is_forbid = models.IntegerField(max_length=2, default=0, db_column='ebf_developer_is_forbid')
    # 更新时间，auto_now_add,为添加时的时间，更新对象时不会有变动,auto_now无论是你添加还是修改对象，时间为你添加或者修改的时间
    developer_update_date = models.DateTimeField(auto_now=True, default=datetime.datetime.utcnow(), db_column='ebf_developer_update_date')
    # 创建时间
    developer_create_date = models.DateTimeField(auto_now_add=True, default=datetime.datetime.utcnow(), db_column='ebf_developer_create_date')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_developer'
        verbose_name = '开发者'
