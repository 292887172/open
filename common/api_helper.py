# !/usr/bin/env python
# -*- coding: utf-8 -*-

from base.connection import SandboxApiMongoDBHandler
from base.connection import SandboxApiRedisHandler
from base.connection import ReleaseApiMongoDBHandler
from base.connection import ReleaseApiRedisHandler
from base.util import gen_app_access_token
from base.util import gen_cache_key
from base.const import ConventionValue
from base.const import CacheKeyPrefix

from enum import Enum
import json
import requests
import logging
import datetime

_convention = ConventionValue()
_cache_key = CacheKeyPrefix()


class RequestMethod(Enum):
    """
    请求方法枚举
    """
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4
    HEAD = 5
    OPTIONS = 6
    PATCH = 7


class XmppApiClient():
    """
    xmpp  api调用类
    """

    def __init__(self, uri):
        self.apiaddr = uri
        self.data = []
        self.payload = {}
        self.params = {}

    def addpara(self, key, value):
        self.payload[key] = value

    def addchildpara(self, key, value):
        self.params[key] = value

    def invoke(self, method="POST"):
        """
        发送xmpp指令（兼容老版本）
        """
        # 新通信服务器地址
        apiaddrnew = "http://61.129.70.109:8002/xmpp"
        # 新通信服务器发送数据
        payloadnew = {"appid": "smartsys", "appsecret": "smart.56iq.net"}
        if "ids" in self.payload.keys():
            payloadnew["id"] = self.payload["ids"]
        elif "player_ids" in self.payload.keys():
            payloadnew["id"] = self.payload["player_ids"]
        if "type" in self.payload.keys():
            payloadnew["type"] = self.payload["type"]
        payloadnew["value"] = json.dumps(self.params)
        if self.apiaddr.lower() == "http://61.129.70.111/webedit/api/player/players/list":
            # 　这个地址原来是获取终端列表信息的
            apiaddrnew = "http://61.129.70.109:8002/xmppinfo"
            if "id" in payloadnew.keys():
                return requests.get(apiaddrnew, params={"id": payloadnew["id"]}, auth=("smartsys", "smart.56iq.net"),
                                    timeout=3)
        self.payload["key"] = "4b99ec1244f5475ab781356aec822463"
        self.payload["username"] = "Ebanswers"
        self.payload["params"] = json.dumps(self.params)
        if method == "POST":
            try:
                # 请求老接口
                requests.post(self.apiaddr, data=self.payload, timeout=2)
            except:
                pass
            return requests.post(apiaddrnew, data=payloadnew, auth=("smartsys", "smart.56iq.net"), timeout=3)
        else:
            return requests.get(self.apiaddr, params=self.payload, timeout=2)


class RestApiClient(object):
    """
    RESTfull api调用类
    """

    def __init__(self, uri, method=RequestMethod.GET,
                 username="admin", password="admin"):
        self.apiaddr = uri
        self.method = method
        self.username = username
        self.password = password
        self.params = {}
        self.header = {}

    def addpara(self, paradict):
        if isinstance(paradict, dict):
            self.params = paradict
        else:
            raise Exception("The parameter is not dict")

    def addheader(self, headerdict):
        if isinstance(headerdict, dict):
            self.header = headerdict
        else:
            raise Exception("The header parameter is not dict")

    def invoke(self):
        if self.method == RequestMethod.GET:
            return requests.get(self.apiaddr, params=self.params,
                                auth=(self.username, self.password))
        elif self.method == RequestMethod.POST:
            return requests.post(self.apiaddr, data=self.params,
                                 auth=(self.username, self.password))
        elif self.method == RequestMethod.PUT:
            headerObj = self.header
            return requests.put(self.apiaddr, data=self.params,
                                auth=(self.username, self.password),
                                headers=headerObj)
        elif self.method == RequestMethod.PATCH:
            headerObj = self.header
            return requests.patch(self.apiaddr, data=self.params,
                                  auth=(self.username, self.password),
                                  headers=headerObj)
        elif self.method == RequestMethod.DELETE:
            headerObj = self.header
            return requests.delete(self.apiaddr, data=self.params,
                                   auth=(self.username, self.password),
                                   headers=headerObj)
        else:
            raise Exception("Not Implemented")


def create_sandbox_api_app(api_id, app_secret):
    """
    添加沙箱的API_APP
    :param api_id:
    :param app_secret:
    :return:
    """
    try:
        document = dict(
            app_id=api_id,
            app_secret=app_secret,
            access_token=gen_app_access_token(),
            max_fetch_number=_convention.ACCESS_TOKEN_MAX_UPDATE_NUMBER,
            power=1,
            status=1,
            _created=datetime.datetime.utcnow()
        )
        db = SandboxApiMongoDBHandler().db
        db.ebc_api_app.insert(document)
        return True
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def create_release_api_app(app_id):
    """
    添加正式的API_APP
    :param app_id:
    :return:
    """
    try:
        screen = dict(
            app_id=app_id
        )
        sandbox_db = SandboxApiMongoDBHandler().db
        document = sandbox_db.ebc_api_app.find_one(screen)
        del document["_id"]
        del document["app_id"]
        document["_created"] = datetime.datetime.utcnow()
        db = ReleaseApiMongoDBHandler().db
        db.ebc_api_app.update({"app_id": app_id}, {"$set": document}, upsert=True)
        return True
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def delete_sandbox_api_app(app_id):
    """
    删除沙箱中的API
    :param app_id:
    :return:
    """
    try:
        screen = dict(
            app_id=app_id
        )
        # 获取旧的access_token ======================
        db = SandboxApiMongoDBHandler().db
        sandbox_old_access_token = ""
        document = db.ebc_api_app.find_one(screen, {"access_token": 1})
        if document:
            sandbox_old_access_token = document.get("access_token", "")
        # 获得旧的secret
        app_secret = ""
        document = db.ebc_api_app.find_one(screen, {"app_secret": 1})
        if document:
            app_secret = document.get("app_secret", "")

        # 删除沙箱的API_APP字段 ======================
        db.ebc_api_app.remove(screen)
        # 删除沙箱的缓存 ======================
        r = SandboxApiRedisHandler().client
        # k:ap
        if r.exists(gen_cache_key(_cache_key.AUTH_APP_ID, app_id)):
            r.delete(gen_cache_key(_cache_key.AUTH_APP_ID, app_id))
        # k.as
        if r.exists(gen_cache_key(_cache_key.AUTH_APP_SECRET, app_id, app_secret)):
            r.delete(gen_cache_key(_cache_key.AUTH_APP_SECRET, app_id, app_secret))
        # k:ak
        if r.exists(gen_cache_key(_cache_key.AUTH_ACCESS_TOKEN, sandbox_old_access_token)):
            r.delete(gen_cache_key(_cache_key.AUTH_ACCESS_TOKEN, sandbox_old_access_token))
        return True
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def delete_release_api_app(app_id):
    """
    删除正式的API
    :param app_id:
    :return:
    """
    try:
        screen = dict(
            app_id=app_id
        )
        # 获取旧的access_token ======================
        db = ReleaseApiMongoDBHandler().db
        release_old_access_token = ""
        document = db.ebc_api_app.find_one(screen, {"access_token": 1})
        if document:
            release_old_access_token = document.get("access_token", "")
        # 获得旧的secret
        app_secret = ""
        document = db.ebc_api_app.find_one(screen, {"app_secret": 1})
        if document:
            app_secret = document.get("app_secret", "")

        # 删除正式的API_APP字段 ======================
        db.ebc_api_app.remove(screen)
        # 删除正式的缓存 ======================
        r = ReleaseApiRedisHandler().client
        # k:ap
        if r.exists(gen_cache_key(_cache_key.AUTH_APP_ID, app_id)):
            r.delete(gen_cache_key(_cache_key.AUTH_APP_ID, app_id))
        # k.as
        if r.exists(gen_cache_key(_cache_key.AUTH_APP_SECRET, app_id, app_secret)):
            r.delete(gen_cache_key(_cache_key.AUTH_APP_SECRET, app_id, app_secret))
        # k:ak
        if r.exists(gen_cache_key(_cache_key.AUTH_ACCESS_TOKEN, release_old_access_token)):
            r.delete(gen_cache_key(_cache_key.AUTH_ACCESS_TOKEN, release_old_access_token))
        return True
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def delete_api_app(app_id):
    """
    删除沙箱和正式中的API
    :param app_id:
    :return:
    """
    try:
        if delete_sandbox_api_app(app_id) and delete_release_api_app(app_id):
            return True
    except Exception as e:
        logging.getLogger("").error(e)
        return False


def reset_api_app_secret(app_id, new_app_secret,):
    """
    重置app_secret
    :param app_id:
    :param old_app_secret:
    :return:
    """
    try:
        screen = dict(
            app_id=app_id
        )
        new_access_token = gen_app_access_token()
        # 获取沙箱旧的 access_token
        db = SandboxApiMongoDBHandler().db
        old_access_token = ""
        document = db.ebc_api_app.find_one(screen, {"access_token": 1})
        if document:
            old_access_token = document.get("access_token", "")
        # 获得旧的secret
        old_app_secret = ""
        document = db.ebc_api_app.find_one(screen, {"app_secret": 1})
        if document:
            old_app_secret = document.get("app_secret", "")

        # 更新沙箱的API_APP字段 Secret =====================
        db.ebc_api_app.update(screen, {"$set": {"app_secret": new_app_secret, "access_token": new_access_token}})
        # 更新沙箱的缓存 =====================
        r = SandboxApiRedisHandler().client
        # k:ap
        if r.exists(gen_cache_key(_cache_key.AUTH_APP_ID, app_id)):
            r.hset(gen_cache_key(_cache_key.AUTH_APP_ID, app_id), "access_token", new_access_token)
        # k.as
        if r.exists(gen_cache_key(_cache_key.AUTH_APP_SECRET, app_id, old_app_secret)):
            r.rename(gen_cache_key(_cache_key.AUTH_APP_SECRET, app_id, old_app_secret),
                     gen_cache_key(_cache_key.AUTH_APP_SECRET, app_id, new_app_secret))
        # k:ak
        if r.exists(gen_cache_key(_cache_key.AUTH_ACCESS_TOKEN, old_access_token)):
            r.rename(gen_cache_key(_cache_key.AUTH_ACCESS_TOKEN, old_access_token),
                     gen_cache_key(_cache_key.AUTH_ACCESS_TOKEN, new_access_token))
            r.hset(gen_cache_key(_cache_key.AUTH_ACCESS_TOKEN, new_access_token), "access_token", new_access_token)
        # 获取正式旧的 access_token
        db = ReleaseApiMongoDBHandler().db
        old_access_token = ""
        document = db.ebc_api_app.find_one(screen, {"access_token": 1})
        if document:
            old_access_token = document.get("access_token", "")
        # 获得正式旧的 secret
        old_app_secret = ""
        document = db.ebc_api_app.find_one(screen, {"app_secret": 1})
        if document:
            old_app_secret = document.get("app_secret", "")
        # 更新正式的API_APP字段 Secret =====================
        db.ebc_api_app.update(screen, {"$set": {"app_secret": new_app_secret, "access_token": new_access_token}})
        # 更新正式的缓存 =====================
        r = ReleaseApiRedisHandler().client
        # k:ap
        if r.exists(gen_cache_key(_cache_key.AUTH_APP_ID, app_id)):
            r.hset(gen_cache_key(_cache_key.AUTH_APP_ID, app_id), "access_token", new_access_token)
        # k.as
        if r.exists(gen_cache_key(_cache_key.AUTH_APP_SECRET, app_id, old_app_secret)):
            r.rename(gen_cache_key(_cache_key.AUTH_APP_SECRET, app_id, old_app_secret),
                     gen_cache_key(_cache_key.AUTH_APP_SECRET, app_id, new_app_secret))
        # k:ak
        if r.exists(gen_cache_key(_cache_key.AUTH_ACCESS_TOKEN, old_access_token)):
            r.rename(gen_cache_key(_cache_key.AUTH_ACCESS_TOKEN, old_access_token),
                     gen_cache_key(_cache_key.AUTH_ACCESS_TOKEN, new_access_token))
            r.hset(gen_cache_key(_cache_key.AUTH_ACCESS_TOKEN, new_access_token), "access_token", new_access_token)
        return True
    except Exception as e:
        logging.getLogger("").error(e)


def delete_app_access_token(app_id):
    r = ReleaseApiRedisHandler().client
    # k:ap
    if r.exists(gen_cache_key(_cache_key.AUTH_APP_ID, app_id)):
        d = r.hget(gen_cache_key(_cache_key.AUTH_APP_ID, app_id), "access_token")
        if d:
            d = d.decode('utf-8')
            r.delete(gen_cache_key(_cache_key.AUTH_ACCESS_TOKEN, d))
            return True

if __name__ == "__main__":
    delete_app_access_token("532NOuoHWy56Ot19Uc11")