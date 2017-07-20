# !/usr/bin/env python
# -*- coding: utf-8 -*-
from base.util import gen_app_access_token

__author__ = 'achais'

from bson.objectid import ObjectId

if __name__ == '__main__':
    r = gen_app_access_token()
    print(r)
