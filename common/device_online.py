from common.zookeeper import ZookeeperHandler
from conf.zkconf import *
from random import randint
from thriftpy.rpc import client_context
from open.settings import BASE_DIR
import thriftpy
import os
import logging


ZK_SMARTSYS_ONLINE = ZookeeperHandler(ZK_HOSTS, SMARTSYS_ONLINE)
SERVICES_ONLINE = ZK_SMARTSYS_ONLINE.discover()
THRIFT_ONLINE = thriftpy.load(os.path.join(BASE_DIR, "idl/online.thrift"), module_name="device_online_service_thrift")


def device_online(device_id):
    ret = SERVICES_ONLINE
    if len(ret) < 1:
        # pass
        raise Exception("没有可用的服务:%s" % SERVICES_ONLINE)
    # 随机方式实现负载均衡
    server = ret[randint(0, len(ret) - 1)].split(":")
    # server_addr = server[0]
    # server_port = int(server[1])
    server_addr = "s74.53iq.com"
    server_port = 48076
    try:
        with client_context(THRIFT_ONLINE.Device, server_addr, server_port, timeout=None,
                            socket_timeout=20000) as client:
            r = client.get_status(device_id)
        print('r',r)
        if r.get('data') == 'online':
            return 1
        else:
            return 0

    except Exception as e:
        logging.exception(e)
        return None


def set_device_online(device_id):
    ret = SERVICES_ONLINE
    if len(ret) < 1:
        # pass
        raise Exception("没有可用的服务:%s" % SERVICES_ONLINE)
    # 随机方式实现负载均衡
    server = ret[randint(0, len(ret) - 1)].split(":")
    # server_addr = "122.144.167.74"
    # server_port = 48076
    server_addr = server[0]
    server_port = int(server[1])

    try:
        with client_context(THRIFT_ONLINE.Device, server_addr, server_port, timeout=None,
                            socket_timeout=20000) as client:
            r = client.heartbeat(device_id, 300)
        return r
    except Exception as e:
        logging.exception(e)
        return None