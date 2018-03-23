# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'achais'

import re


class CacheKeyPrefix(object):
    # auth app_id
    AUTH_APP_ID = "auth_app_id"
    # auth app_secret
    AUTH_APP_SECRET = "auth_app_secret"
    # 值:json字符串:auth access_token
    AUTH_ACCESS_TOKEN = "auth_access_token"
    # 值:normal字符串:access_token, 键:update_access_token_number:{app_id}:{app_secret}
    ACCESS_TOKEN_CURRENT_FETCH_NUMBER = "access_token_update_number"


class ConventionValue(object):
    """
    约定:
    数据库中定义的一些有含义的值,例如(应用check_status:0代表未审核, 1代表审核, 2代表审核通过, -1代表审核未通过)
    """

    def __init__(self):
        pass

    # ACCESS_TOKEN_MAX_UPDATE_NUMBER
    ACCESS_TOKEN_MAX_UPDATE_NUMBER = 2000
    # 应用,0:未审核,1:审核中,2:审核通过,-1:审核失败
    APP_UN_CHECK = 0
    APP_CHECKING = 1
    APP_CHECKED = 2
    APP_CHECK_FAILED = -1
    APP_DEFAULT = 3
    # 功能审核 1：待审核，2：审核通过，-1审核失败
    FUN_CHECKING = 1
    FUN_CHECK_FAILED = -1
    FUN_CHECKED = 2
    # 用户的权限,0:普通用户,1:运营人员,2:厂商账号
    USER_IS_ACCOUNT = 0
    USER_IS_ADMIN = 1
    USER_IS_FRIEND = 2
    # 开发者审核状态
    DEVELOPER_CHECKING = 0
    DEVELOPER_CHECKED = 1
    DEVELOPER_CHECK_FAILED = -1
    # 开发者禁用状态
    DEVELOPER_IS_FORBID = 1
    DEVELOPER_UN_FORBID = 0
    # 用户禁用状态
    ACCOUNT_IS_FORBID = 1
    ACCOUNT_UN_FORBID = 0


class StatusCode(object):
    # ============================= 返回格式规范 ====================
    # Response
    # 绝大部分接口的响应类型为 application/json。此时，响应的JSON对象中都包含一个 code 字段，这用于标识请求成功与否：
    #
    # code 为 0，此时成功执行了请求。 对应的数据位于data字段。 它的具体类型跟接口有关。
    # 如：
    # {"code": 0, "data": {}}
    #
    # code 不为 0，此时请求未能正常完成。 对应的错误信息位于msg字段。 它的类型为string。
    # 如：
    # {"code": 40003, "msg": "invalid access_token"}
    # ============================= 系统状态 ====================
    # 系统繁忙(一般是系统出错)
    SYSTEM_TIMEOUT_CODE = -1
    # 英文提示,主要用在接口
    SYSTEM_TIMEOUT_MSG = "The system is busy, please try again later"
    # 中文提示,主要用在HTTP请求Response
    SYSTEM_TIMEOUT_MESSAGE = "系统繁忙,请稍后再试"
    # 执行成功
    SUCCESS_CODE = 0
    SUCCESS_MSG = "success"
    SUCCESS_MESSAGE = "成功"
    # ============================= 40xxx ==================== 40xxx 是某某东西无效(例如:应用编号无效)
    # appid无效
    INVALID_APP_ID_CODE = 40001
    INVALID_APP_ID_MSG = "invalid appid"
    INVALID_APP_ID_MESSAGE = "appid无效"
    # secret无效
    INVALID_APP_SECRET_CODE = 40002
    INVALID_APP_SECRET_MSG = "invalid secret"
    INVALID_APP_SECRET_MESSAGE = ""
    # access_token无效
    INVALID_ACCESS_TOKEN_CODE = 40003
    INVALID_ACCESS_TOKEN_MSG = "invalid access_token"
    INVALID_ACCESS_TOKEN_MESSAGE = ""
    # access_token无效
    INVALID_APP_KEY_CODE = 40004
    INVALID_APP_KEY_MSG = "invalid app_key"
    INVALID_APP_KEY_MESSAGE = "app_key无效"
    # application_id无效
    INVALID_APPLICATION_ID_CODE = 40009
    INVALID_APPLICATION_ID_MSG = "invalid application_id"
    INVALID_APPLICATION_ID_MESSAGE = ""
    # ============================= 41xxx ==================== 41xxx 是缺少某某东西(例如:缺少用户名参数)
    # 缺少application_id参数
    MISSING_APPLICATION_ID_CODE = 41001
    MISSING_APPLICATION_ID_MSG = "missing application_id"
    MISSING_APPLICATION_ID_MESSAGE = "缺少应用编号"
    # 缺少application_id参数
    MISSING_APP_KEY_CODE = 41001
    MISSING_APP_KEY_MSG = "missing app_key"
    MISSING_APP_KEY_MESSAGE = "缺少设备授权key"
    # ============================= 45xxx ==================== 45xxx 是某某东西超出了限制(例如:API调用次数超出限制)
    OVER_FETCH_ACCESS_TOKEN_NUMBER_CODE = 45001
    OVER_FETCH_ACCESS_TOKEN_NUMBER_MSG = "api freq out of limit"

    # ============================= 46xxx ==================== 46xxx 请求错误，服务器出现错误异常
    # 46001 请求异常（例如请求超时等）
    # 46002 返回结果不是json格式的数据

    def __init__(self, code=None, msg=None, message=None):
        """
        传入code定义内容
        :param code:
        :return:
        """
        self._result = {}
        self._code = code
        self._msg = msg
        self._message = message
        self._result = dict(
            code=self._code,
            msg=self._msg,
            message=self._message
        )
        for k in self.__dir__():
            if code and not re.match(r"__\D+__", k) and re.match(r"\D+_CODE", k) and self.__getattribute__(k) == code:
                _prefix = k[:-5]
                self._result["code"] = self.__getattribute__("%s_CODE" % _prefix)
                self._result["msg"] = self.__getattribute__("%s_MSG" % _prefix)
                self._result["message"] = self.__getattribute__("%s_MESSAGE" % _prefix)
                break

    @property
    def code(self):
        """
        全局状态码
        :return:
        """
        return self._result.get("code", 0)

    @property
    def msg(self):
        """
        返回英文信息
        :return:
        """
        return self._result.get("msg", "")

    @property
    def message(self):
        """
        返回中文信息
        :return:
        """
        return self._result.get("message", "")

    @property
    def result(self):
        """
        返回结果dict对象
        :return:
        """
        if self._result:
            return self._result
        else:
            return {"code": 0}
