# !/bash/bin/env python
# -*- coding: utf-8 -*-

from kazoo.client import KazooClient
from kazoo.protocol.states import KazooState, KeeperState

__author__ = 'rdy'


class ZookeeperHandler:
    def __init__(self, zk_hosts, prefix, host=None, port=None):
        self.zk = KazooClient(hosts=zk_hosts)
        self.prefix = prefix
        self.is_service = host
        self.children = None
        self.root_path = self.prefix + "/{0}:{1}".format(host, port)

        @self.zk.add_listener
        def zk_listener(state):
            # 这个方法也要放在start前面
            if state == KazooState.LOST:
                print("lost", state)
            elif state == KazooState.CONNECTED:
                # 检查是否是只读的客户端
                if self.zk.client_state == KeeperState.CONNECTED_RO:
                    print("Read only mode!")
                else:
                    print("Read/Write mode!")
            elif state == KazooState.SUSPENDED:
                print("SUSPENDED", state)
            else:
                print("other", state)

        self.zk.start()

    def register(self):
        """
        服务注册
        :return:
        """
        if not self.is_service:
            return
        if not self.zk.exists(self.prefix):
            # 注册这个目录，如果不存在的话就创建，可以连着创建几个目录（但是不能存储数据）
            print("创建节点了", self.prefix)
            self.zk.ensure_path(self.prefix)
        if self.zk.exists(self.root_path):
            self.zk.delete(self.root_path, recursive=True)
        self.zk.create(self.root_path, b'{"weight":1}', ephemeral=True, sequence=False)

        # 监视子节点变化
        @self.zk.ChildrenWatch(self.prefix)
        def watch_children(children):
            self.children = children
            print("子节点变化了（需要更新服务列表了）: %s" % children)

        # 实时监视数据的变化(可以做动态配置)
        @self.zk.DataWatch(self.root_path)
        def watch_node(data, stat):
            print("节点下的数据变化了(这边可以写些处理逻辑)：", data, stat)
            if stat:
                print("Version: %s, data: %s" % (stat.version, data.decode("utf-8")))

    def discover(self):
        """
        服务发现
        :return:
        """
        # 获取子节点
        ret = self.zk.get_children(self.prefix)
        return ret
