# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'rdy'
from model.center.account import Account
a = Account.objects.filter(account_id='admin')
print(a, type(a))