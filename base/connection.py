# !/usr/bin/env python
# -*- coding: utf-8 -*-
import ssl

import pymysql
import redis
from DBUtils.PooledDB import PooledDB
from pymongo import MongoClient
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

from conf.mongoconf import RELEASE_API_MONGODB_DATABASE, \
    SANDBOX_API_MONGODB_STR, RELEASE_API_MONGODB_STR
from conf.mongoconf import SANDBOX_API_MONGODB_DATABASE
from conf.mysqlconf import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PWD, MYSQL_DB
from conf.mysqlconf import MYSQL_HOST_SYS, MYSQL_PORT_SYS, MYSQL_USER_SYS, MYSQL_PWD_SYS, MYSQL_DB_SYS
from conf.redisconf import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PWD, REDIS_HOST3
from conf.redisconf import RELEASE_API_REDIS_HOST, RELEASE_API_REDIS_PORT, RELEASE_API_REDIS_DB, RELEASE_API_REDIS_PWD
from conf.redisconf import SANDBOX_API_REDIS_HOST, SANDBOX_API_REDIS_PORT, SANDBOX_API_REDIS_DB, SANDBOX_API_REDIS_PWD

__author__ = 'achais'


class RedisBaseHandler(object):
    """
    例子:
    r = RedisBaseHandler().client
    r.get("name")
    """

    def __init__(self):
        redis_connection_pool = redis.ConnectionPool(max_connections=512,
                                                     host=REDIS_HOST,
                                                     port=REDIS_PORT,
                                                     db=REDIS_DB,
                                                     password=REDIS_PWD)
        redis_client = redis.Redis(connection_pool=redis_connection_pool)
        self.client = redis_client


Redis_Clent = RedisBaseHandler().client


class Redis3(object):
    def __init__(self, rdb=REDIS_DB):
        redis_connection_pool = redis.ConnectionPool(max_connections=512,
                                                     host=REDIS_HOST3,
                                                     port=REDIS_PORT,
                                                     db=rdb,
                                                     password=REDIS_PWD)
        redis_client = redis.Redis(connection_pool=redis_connection_pool)
        self.client = redis_client


Redis3_Client = Redis3().client
Redis3_ClientDB5 = Redis3(rdb=5).client
Redis3_ClientDB6 = Redis3(rdb=6).client


class MySqlConnPoll(object):
    def __init__(self, min_cached=2, max_cached=5, max_shared=0, max_connections=10, blocking=False,
                 max_usage=None, set_session=None, reset=True, failures=None, ping=1, *args, **kwargs):
        """

        :param min_cached: 最少的空闲连接数，如果空闲连接数小于这个数，pool会创建一个新的连接
        :param max_cached: 最大的空闲连接数，如果空闲连接数大于这个数，pool会关闭空闲连接
        :param max_shared: 当连接数达到这个数，新请求的连接会分享已经分配出去的连接
        :param max_connections: 最大的连接数
        :param blocking: 当连接数达到最大的连接数时，在请求连接的时候，如果这个值是True，请求连接的程序会一直等待，直到当前连接数小于最大连接数，如果这个值是False，会报错
        :param max_usage:
        :param set_session:
        :param reset:
        :param failures:
        :param ping:
        :param args:
        :param kwargs:
        """
        self.pool = PooledDB(pymysql, mincached=min_cached, maxcached=max_cached,
                             maxshared=max_shared, maxconnections=max_connections, blocking=blocking,
                             maxusage=max_usage, setsession=set_session, reset=reset,
                             failures=failures, ping=ping, *args, **kwargs)

    @property
    def conn(self):
        return self.pool.connection()


# mysql连接池
mysql_conn_poll = MySqlConnPoll(
    host=MYSQL_HOST,
    port=MYSQL_PORT,
    user=MYSQL_USER,
    passwd=MYSQL_PWD,
    db=MYSQL_DB,
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)

sys_mysql_conn_pool = MySqlConnPoll(
    host=MYSQL_HOST_SYS,
    port=MYSQL_PORT_SYS,
    user=MYSQL_USER_SYS,
    passwd=MYSQL_PWD_SYS,
    db=MYSQL_DB_SYS,
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)


class SandboxApiMongoDBHandler(object):
    def __init__(self):
        self.client = MongoClient(SANDBOX_API_MONGODB_STR)
        mongodb_database = self.client[SANDBOX_API_MONGODB_DATABASE]
        self.db = mongodb_database


SandboxApiMongoDBClient = SandboxApiMongoDBHandler().db


class ReleaseApiMongoDBHandler(object):
    def __init__(self):
        self.client = MongoClient(RELEASE_API_MONGODB_STR)
        mongodb_database = self.client[RELEASE_API_MONGODB_DATABASE]
        self.db = mongodb_database


ReleaseApiMongoDBClient = ReleaseApiMongoDBHandler().db


class SandboxApiRedisHandler(object):
    def __init__(self):
        max_connections = 512
        redis_connection_pool = redis.ConnectionPool(max_connections=max_connections,
                                                     host=SANDBOX_API_REDIS_HOST,
                                                     port=SANDBOX_API_REDIS_PORT,
                                                     db=SANDBOX_API_REDIS_DB,
                                                     password=SANDBOX_API_REDIS_PWD)
        redis_client = redis.Redis(connection_pool=redis_connection_pool)
        self.client = redis_client


SandboxApiRedisClient = SandboxApiRedisHandler().client


class ReleaseApiRedisHandler(object):
    def __init__(self):
        max_connections = 512
        redis_connection_pool = redis.ConnectionPool(max_connections=max_connections,
                                                     host=RELEASE_API_REDIS_HOST,
                                                     port=RELEASE_API_REDIS_PORT,
                                                     db=RELEASE_API_REDIS_DB,
                                                     password=RELEASE_API_REDIS_PWD)
        redis_client = redis.Redis(connection_pool=redis_connection_pool)
        self.client = redis_client


ReleaseApiRedisClient = ReleaseApiRedisHandler().client


class MyAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(num_pools=connections,
                                       maxsize=maxsize,
                                       block=block,
                                       ssl_version=ssl.PROTOCOL_TLSv1)
