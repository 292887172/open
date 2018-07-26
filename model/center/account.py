# !/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import hashlib
import datetime
from django.db import models
from app.center.models import AbstractBaseUser
# from app.center.models import BaseUserManager
from django.contrib.auth.models import BaseUserManager
from model.center.developer import Developer

__author__ = 'rdy'


def md5(x):
    return hashlib.md5(x.lower()).hexdigest()


class MyUserManager(BaseUserManager):
    def create_wx_user(self, account, password, stat, nickname):
        user = self.model(
            account_id=MyUserManager.normalize_email(account),
            account_from_id=stat,
            account_type=3,
            account_nickname=nickname,
            last_login=datetime.datetime.now(),
            account_create_date=datetime.datetime.now()
        )

        user.set_password(password)

        user.save()
        return user

    def create_user(self, account, password, stat, dproducts='', team_persons=1, expertise="", sproducts="", intent="",
                    tel='no', email=''):
        # 最后一个参数为了区分设备管理系统厂商注册过来的电话号码，其他注册没有这个参数
        if not account:
            raise ValueError('Users must have an account id')
        from_id = stat
        phone = ''
        if str(account).find('@') > 1:
            email = account
        elif str(account).isdigit():
            phone = account
        else:
            if str(tel).isdigit():
                phone = tel
        user = self.model(
                account_id=MyUserManager.normalize_email(account),
                account_from_id=from_id,
                account_email=email,
                account_phone=phone,
                last_login=datetime.datetime.now(),
                account_create_date=datetime.datetime.now(),
                account_dproducts=dproducts,
                account_team_persons=team_persons,
                account_expertise=expertise,
                account_sproducts=sproducts,
                account_intent=intent
        )

        user.set_password(password)

        user.save()
        return user

    def create_superuser(self, account, password, stat='ok'):
        if not account:
            raise ValueError('Users must have an account id')

        user = self.create_user(account, password=password, stat=stat, dproducts="", team_persons=1, sproducts="",
                                expertise="", intent="")
        user.is_admin = True

        user.save()
        return user

    def change_password(self, account, password):

        if not account:
            raise ValueError('Users must have an account id')

        user = self.model(
            account_id=MyUserManager.normalize_email(account),
            last_login=datetime.datetime.utcnow(),
        )
        user.set_password(password)
        user.save()
        return user

    def admin_change_password(self, account, password, account_type):

        if not account:
            raise ValueError('Users must have an account id')

        user = self.model(
            account_id=MyUserManager.normalize_email(account),
            account_type=account_type,
            last_login=datetime.datetime.utcnow(),
        )
        user.set_password(password)
        user.save()
        return user


class Account(AbstractBaseUser):
    """
    用户账户表
    """
    # 用户帐号
    account_id = models.CharField(primary_key=True, max_length=64, db_column='ebf_account_id')
    # 用户来源帐号
    account_from_id = models.CharField(max_length=64, null=True, db_column='ebf_account_from_id')
    # 帐号密码
    # account_pwd = models.CharField(max_length=512, db_column='ebf_account_password')
    # 帐号类型（0：普通账号 ，1：运营账号，2：厂商帐号, 3:微信账号）
    account_type = models.IntegerField(max_length=3, default=0, db_column='ebf_account_type')
    # 帐号邮箱
    account_email = models.CharField(max_length=64, null=True, db_column='ebf_account_email')
    # 账号昵称
    account_nickname = models.CharField(max_length=128, null=True, db_column='ebf_account_nickname')
    # 手机号
    account_phone = models.CharField(max_length=32, null=True, db_column='ebf_account_phone')
    # 帐号是否禁用 （0：启用，1：禁用）
    account_is_forbid = models.IntegerField(max_length=2, default=0, db_column='ebf_account_is_forbid')
    # 上次登录时间
    # account_last_login = models.DateTimeField(default=datetime.datetime.utcnow(), db_column='ebf_account_last_login')
    # 帐号创建时间
    account_create_date = models.DateTimeField(default=datetime.datetime.utcnow(), db_column='ebf_account_create_date')

    # 参与开发的产品
    account_dproducts = models.CharField(max_length=128, db_column='ebf_account_dproducts')
    # 团队人数
    account_team_persons = models.IntegerField(max_length=4, db_column='ebf_account_team_persons')
    # 专长
    account_expertise = models.CharField(max_length=128, db_column='ebf_account_expertise')
    # 已出货的产品(列举)
    account_sproducts = models.CharField(max_length=128, db_column='ebf_account_sproducts')
    # 合作意向
    account_intent = models.CharField(max_length=128, db_column='ebf_account_intent')
    # 关联账户
    relate_account = models.TextField(null=True, db_column='ebf_account_relate_account')
    USERNAME_FIELD = 'account_id'
    # REQUIRED_FIELDS = ['stat', ]
    objects = MyUserManager()

    def __unicode__(self):
        return self.account_id

    # 判断用户使用已禁用
    @property
    def is_forbid(self):
        return self.account_is_forbid

    @property
    def is_developer(self):
        try:

            return self.developer.developer_check_status == 1 and self.developer.developer_is_forbid == 0
        except Exception as e:
            print(e)
            return False

    @property
    def is_staff(self):
        return self.account_type

    def get_full_name(self):
        return self.account_id

    def get_short_name(self):
        return self.account_id

    @property
    def developer(self):
        account_id = self.account_id
        try:
            developer = Developer.objects.get(developer_account=account_id)
        except Exception as e:
            print(e)
            developer = None
        return developer

    class Meta:
        app_label = 'center'
        db_table = 'ebt_account'
        verbose_name = '用户帐号'
