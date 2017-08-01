# !/usr/bin/env python
# -*- coding: utf-8 -*-
from base.connection import MysqlHandler
import json

from base.util import gen_app_default_conf

__author__ = 'rdy'
conn = MysqlHandler().conn
cur = conn.cursor()
sql = 'SELECT * FROM ebt_app WHERE ebf_app_id=%s LIMIT 1'
cur.execute(sql, 78)
result = cur.fetchone()
c = result['ebf_device_conf']
print(json.loads(c))
a = gen_app_default_conf('2')
print(type(a), a)
