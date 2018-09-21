# -*- coding: utf-8 -*-
import time

# 全局变量
from conf.commonconf import IS_DEBUG


def set_version(request):
    """
    设置版本号
    :param request:
    :return:
    """
    if IS_DEBUG:
        is_debug = "true"
    else:
        is_debug = "false"
    return {'version_code': "563846523444", "is_debug": is_debug}


if __name__ == "__main__":
    print(time.time())
