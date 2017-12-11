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
    userID = did
    print('用户:', userID)
    if did =='test15267183467-stove':
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
    if did == 'test15267183467-smoke':
        if status:
            name = status.get('name')
            value = status.get('value')

            if name == 'POWER':
                if value:
                    default[0] = 1
                    default[1] = 1
                else:
                    default[0] = 0
                    default[1] = 0
                    default[2] = 0
                    default[3] = 0
                if value == 0:
                    default = [str(0) for e in default]
            elif name == 'LIGHT':
                if value:
                    default[1] = 1
                else:
                    default[1] = 0
            elif name == 'BIG_WIND':
                if value:
                    default[2] = 1
                    default[3] = 0
                    default[7] = 0
                else:
                    default[2] =0
            elif name == 'SMALL_WIND':
                if value:
                    default[3] = 1
                    default[2] = 0
                    default[7] = 0
                else:
                    default[3] = 0
            elif name == 'MIDDLE_WIND':
                if value:
                    default[7] = 1
                    default[2] = 0
                    default[3] = 0
                else:
                    default[7] = 0
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

    # 油烟机发送数据
    # default = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    # ID | 模式 | 温度 | 时间 | 工作状态 | 操作 | 风扇 | 电灯 | -->
    #  tmp_status = {'did': userID, 'model': devices.oven_type, 'temp': Oven_temp, 'time': nowtime, 'status': status, 'wind': wind, 'light': light};

    if did =='test15267183467-smoke':
        if status:
            oven_model = status.get('model')
            oven_temp = status.get('temp')
            oven_time =status.get('time')
            oven_status =status.get('status')
            oven_wind =status.get('wind')
            oven_light =status.get('light')
            default[0] = oven_model
            default[1] =oven_temp
            default[2]=oven_time
            default[3]=oven_status
            default[4]=oven_wind
            default[5]=oven_light
        deal_test_device_status(did,default,'set')
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













