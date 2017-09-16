# !/bash/bin/env python
# -*- coding: utf-8 -*-
from base.connection import Redis3
from common.code import ResponseCode
import json
import stomp

from conf.stompconf import STOMP_ADDR, STOMP_PORT, STOMP_ADDR2

__author__ = 'rdy'
_code = ResponseCode()


def gen_group_key(*args):
    return ":".join(str(_) for _ in args)


def parse_response(code=0, msg="", data=""):
    """
    格式化输出返回消息
    :param code: 全局代码
    :param msg: 英文提示
    :param data: 数据
    :return:
    """
    return _code.load(code, msg, data).result


def deal_test_device_status(device_id, val, action):
    r = Redis3(6).client
    default = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    try:
        if action == 'get':
            res = r.get(gen_group_key(_code.TEST_DEVICE_STATUS_PREFIX, device_id))
            if res:
                return json.loads(res.decode('utf-8'))
            else:
                return default
        elif action == 'set':
            r.setex(gen_group_key(_code.TEST_DEVICE_STATUS_PREFIX, device_id), val, 20 * 60)
            return val
    except Exception as e:
        return default


def send_test_device_status(did, status):
    """
    发送测试设备的状态，实现多屏互动
    :param did:
    :param status:
    :return:
    """
    # 电源|照明|大风|小风|消毒|烘干|延时|中风|故障|火(| 运行时间|风险指数)”
    # default = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]    # '0|0|0|0|0|0|0|0|0|0|0|0'
    default = deal_test_device_status(did, '', 'get')
    if status:
        name = status.get('name')
        value = status.get('value')
        if name == 'POWER':
            default[0] = value
            default[-1] = 10
            if value == 0:
                default = [str(0) for e in default]

        elif name == 'LIGHT':
            default[1] = value
        elif name == 'WIND':
            if value == 1:
                default[2] = 0
                default[3] = 1
                default[7] = 0
            elif value == 2:
                default[2] = 0
                default[3] = 0
                default[7] = 1
            elif value == 3:
                default[2] = 1
                default[3] = 0
                default[7] = 0
            else:
                default[2] = 0
                default[3] = 0
                default[7] = 0
        elif name == 'DISINFECT':
            default[4] = value
        elif name == 'DRY':
            default[5] = value
    deal_test_device_status(did, default, 'set')
    default = [str(e) for e in default]
    default = "|".join(default)
    try:
        conn = stomp.Connection10(host_and_ports=[(STOMP_ADDR, STOMP_PORT)])
        conn.start()
        conn.connect()
        conn2 = stomp.Connection10(host_and_ports=[(STOMP_ADDR2, STOMP_PORT)])
        conn2.start()
        conn2.connect()
        obj = {"id": did, "type": int(2500), "value": default}
        print('发送内容', obj)
        # 往支持stomp协议的消息队列中添加数据
        conn.send(body=json.dumps({"msg": obj}), destination="/" + did)
        conn.disconnect()
        conn2.send(body=json.dumps({"msg": obj}), destination="/" + did)
        conn2.disconnect()
        obj_res = "OK"
    except Exception as e:
        print('往消息队列中发送消息出错:' + str(e))
        # 请求格式错误
        obj_res = "ERR"
        pass
    return obj_res
