# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'achais'

from pymongo import MongoClient
import pymysql
import redis
from conf.redisconf import REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PWD
from conf.mysqlconf import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PWD, MYSQL_DB
from conf.mysqlconf import MYSQL_HOST_SYS, MYSQL_PORT_SYS, MYSQL_USER_SYS, MYSQL_PWD_SYS, MYSQL_DB_SYS
from conf.mongoconf import SANDBOX_API_MONGODB_HOST, SANDBOX_API_MONGODB_PORT, SANDBOX_API_MONGODB_DATABASE
from conf.mongoconf import SANDBOX_API_MONGODB_USER, SANDBOX_API_MONGODB_PWD
from conf.mongoconf import RELEASE_API_MONGODB_HOST, RELEASE_API_MONGODB_PORT, RELEASE_API_MONGODB_DATABASE
from conf.mongoconf import RELEASE_API_MONGODB_USER, RELEASE_API_MONGODB_PWD
from conf.redisconf import SANDBOX_API_REDIS_HOST, SANDBOX_API_REDIS_PORT, SANDBOX_API_REDIS_DB, SANDBOX_API_REDIS_PWD
from conf.redisconf import RELEASE_API_REDIS_HOST, RELEASE_API_REDIS_PORT, RELEASE_API_REDIS_DB, RELEASE_API_REDIS_PWD


class RedisBaseHandler(object):
    """
    例子:
    r = RedisBaseHandler().client
    r.get("name")
    """

    def __init__(self):
        max_connections = 512
        redis_connection_pool = redis.ConnectionPool(max_connections=max_connections,
                                                     host=REDIS_HOST,
                                                     port=REDIS_PORT,
                                                     db=REDIS_DB,
                                                     password=REDIS_PWD)
        redis_client = redis.Redis(connection_pool=redis_connection_pool)
        self.client = redis_client


class MysqlHandler(object):
    """
    例子:
    conn = MysqlHandler().conn
    cur = conn.cursor()
    """

    def __init__(self):
        self.conn = pymysql.connect(host=MYSQL_HOST,
                                    port=MYSQL_PORT,
                                    user=MYSQL_USER,
                                    passwd=MYSQL_PWD,
                                    db=MYSQL_DB,
                                    charset='UTF8',
                                    cursorclass=pymysql.cursors.DictCursor)


class SysMysqlHandler(object):
    """
    例子:
    conn = SysMysqlHandler().conn
    cur = conn.cursor()
    """

    def __init__(self):
        self.conn = pymysql.connect(host=MYSQL_HOST_SYS,
                                    port=MYSQL_PORT_SYS,
                                    user=MYSQL_USER_SYS,
                                    passwd=MYSQL_PWD_SYS,
                                    db=MYSQL_DB_SYS,
                                    charset='UTF8',
                                    cursorclass=pymysql.cursors.DictCursor)


class SandboxApiMongoDBHandler(object):
    def __init__(self):
        self.client = MongoClient(host=SANDBOX_API_MONGODB_HOST,
                                  port=SANDBOX_API_MONGODB_PORT)
        mongodb_database = self.client[SANDBOX_API_MONGODB_DATABASE]
        mongodb_database.authenticate(SANDBOX_API_MONGODB_USER, SANDBOX_API_MONGODB_PWD)
        self.db = mongodb_database


class ReleaseApiMongoDBHandler(object):
    def __init__(self):
        self.client = MongoClient(host=RELEASE_API_MONGODB_HOST,
                                  port=RELEASE_API_MONGODB_PORT)
        mongodb_database = self.client[RELEASE_API_MONGODB_DATABASE]
        mongodb_database.authenticate(RELEASE_API_MONGODB_USER, RELEASE_API_MONGODB_PWD)
        self.db = mongodb_database


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
