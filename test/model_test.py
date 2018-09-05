# !/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

__author__ = 'rdy'
url2 = 'https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}'.format(
    '2DSQlZFAy9prnRjSGiC6OpQxcga10VSjQxM_nBmO-WL9GAECHX0nIn7u64tdUFoun4-AcKeljkiLlK7JLABgdA',
    'oVJQIxEBwnRxsYB0zvEcGZvYnKXE')
ret2 = requests.get(url2)
ret2.encoding = 'utf8'
ret2 = ret2.json()
print(ret2)
