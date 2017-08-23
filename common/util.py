# !/bash/bin/env python
# -*- coding: utf-8 -*-

from common.code import ResponseCode
__author__ = 'rdy'
_code = ResponseCode()


def parse_response(code=0, msg="", data=""):
    """
    格式化输出返回消息
    :param code: 全局代码
    :param msg: 英文提示
    :param data: 数据
    :return:
    """
    return _code.load(code, msg, data).result
