__author__ = 'rdy'
from django.db import models

from model.center.app import App
from model.center.api import Api


class ApiAuth(models.Model):
    """
    api权限表
    """
    # api权限编号
    aa_id = models.AutoField(primary_key=True, db_column='ebf_aa_id')
    # 应用编号
    app_id = models.ForeignKey(App, null=True, db_column='ebf_app_id')
    # 接口编号
    api_id = models.ForeignKey(Api, null=True, db_column='ebf_api_id')
    # 每天调用次数
    invoke_total = models.BigIntegerField(max_length=20, db_column='ebf_aa_invoke_total')
    # 是否禁用 （0：未禁用，1：禁用）
    aa_is_forbid = models.IntegerField(max_length=2, default=0, db_column='ebf_aa_is_forbid')
    # api授权时间,auto_now_add,为添加时的时间，更新对象时不会有变动,auto_now无论是你添加还是修改对象，时间为你添加或者修改的时间
    aa_create_date = models.DateTimeField(auto_now_add=True, db_column='ebf_aa_create_date')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_api_auth'
        verbose_name = 'api接口权限'