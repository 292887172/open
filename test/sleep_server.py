from common.zookeeper import ZookeeperHandler
from conf.zkconf import *
from random import  randint
from thriftpy.rpc import client_context
from open.settings import BASE_DIR
import thriftpy
from thriftpy.rpc import make_server
import os
import logging


ZK_SMARTSYS_ONLINE = ZookeeperHandler(ZK_HOSTS, SMARTSYS_ONLINE)
SERVICES_ONLINE = ZK_SMARTSYS_ONLINE.discover()
THRIFT_ONLINE = thriftpy.load(os.path.join(BASE_DIR, "idl/online.thrift"), module_name="device_online_service_thrift")


class Online(object):
    def ping(self):
        return "pong"
    def get_status(self,device_id):
        ret = {'msg': '请求成功', 'data': 'online', 'code': '0'}
        return ret

ret = SERVICES_ONLINE
if len(ret) < 1:
    # pass
    raise Exception("没有可用的服务:%s" % SERVICES_ONLINE)
# 随机方式实现负载均衡
s = ret[randint(0, len(ret) - 1)].split(":")
# server_addr = s[0]
# server_port = int(s[1])
server_addr = "127.0.0.1"
server_port = 6000
server = make_server(THRIFT_ONLINE.Device, Online(), server_addr, server_port)
server.serve()