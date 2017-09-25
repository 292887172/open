from django.db import models
import datetime
__author__ = 'rdy'


class AutoLogin(models.Model):
    """
    ebt_auto_login表
    """
    # api编号
    al_id = models.AutoField(primary_key=True, db_column='ebf_al_id')
    # 用户帐号
    al_account_id = models.CharField(max_length=64, db_column='ebf_al_account_id')
    # 用户密码
    al_account_pwd = models.CharField(max_length=512, db_column='ebf_al_account_password')
    # 登录token
    al_token = models.CharField(max_length=63, db_column='ebf_al_token')
    # 登录ip
    al_login_ip = models.CharField(max_length=32, db_column='ebf_al_login_ip')
    # 创建时间
    al_create_date = models.DateTimeField(default=datetime.datetime.utcnow(), db_column='ebf_al_create_date')
    # 更新时间
    al_update_date = models.DateTimeField(default=datetime.datetime.utcnow(), db_column='ebf_al_update_date')

    class Meta:
        app_label = 'center'
        db_table = 'ebt_auto_login'
        verbose_name = '自动登录记录'
