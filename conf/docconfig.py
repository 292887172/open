# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from open import settings


DOC_TPL_PATH = os.path.join(settings.BASE_DIR, "static/file/tpl")

# 文档部分返回消息模板
DOC_RET_MSG = {
    "status": 1,
    "msg": "",
    "data": None
}




