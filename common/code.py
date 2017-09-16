# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re
__author__ = 'rdy'


class ResponseCode(object):
    def __init__(self, code=0, msg="", data=""):
        """
        传入code定义内容
        :param code:
        :return:
        """
        self._result = {}
        self._code = code
        self._msg = msg
        self._data = data
        self._result = dict(
                code=self._code,
                msg=self._msg,
                data=self._data
        )
        for k in self.__dir__():
            if code and not re.match(r"__\D+__", k) and re.match(r"\D+_CODE", k) and getattr(self, k, None) == code:
                _prefix = k[:-5]
                self._result["code"] = getattr(self, "%s_CODE" % _prefix, "")
                self._result["msg"] = getattr(self, "%s_MSG" % _prefix, "")
                break

    def load(self, code=0, msg="", data=""):
        self.__init__(code, msg, data)
        return self

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
    def result(self):
        """
        返回结果dict对象
        :return:
        """
        if self._result:
            if self._code == 0:
                if not self._result['data']:
                    self._result["data"] = "success"
                # del self._result["msg"]
            else:
                pass
                # del self._result["data"]
            return self._result
        else:
            return {"code": 0}

    # 系统出错
    SYSTEM_ERROR_CODE = -1
    SYSTEM_ERROR_MSG = "system error"
    # 执行成功
    SUCCESS_CODE = 0
    SUCCESS_MSG = "success"
    # ============================= 10xx ==================== 无效
    # did无效
    INVALID_DID_CODE = 1001
    INVALID_DID_MSG = "invalid did"
    # user无效
    INVALID_USER_CODE = 1002
    INVALID_USER_MSG = "invalid user"
    # token 无效
    INVALID_TOKEN_CODE = 1003
    INVALID_TOKEN_MSG = 'invalid token'
    INVALID_MSG_TYPE_CODE = 1004
    INVALID_MSG_TYPE_MSG = 'invalid msg type'
    INVALID_POST_DATA_CODE = 1005
    INVALID_POST_DATA_MSG = 'invalid post data'
    INVALID_ACTION_CODE = 1006
    INVALID_ACTION_MSG = 'invalid action'
    # ============================= 20xx ==================== 缺少
    MISSING_DEVICE_MAC_CODE = 2001
    MISSING_DEVICE_MAC_MSG = "missing device mac"
    MISSING_SCENE_STR_CODE = 2002
    MISSING_SCENE_STR_MSG = "missing scene_str"
    MISSING_OPENID_CODE = 2003
    MISSING_OPENID_MSG = "missing openid"
    MISSING_COMMAND_CODE = 2004
    MISSING_COMMAND_MSG = 'missing command'
    MISSING_VALUE_CODE = 2005
    MISSING_VALUE_MSG = 'missing value'
    MISSING_TOKEN_CODE = 2006
    MISSING_TOKEN_MSG = 'missing access_token'
    MISSING_MSG_TYPE_CODE = 2007
    MISSING_MSG_TYPE_MSG = 'missing message type'
    MISSING_ARTICLE_LINK_CODE = 2008
    MISSING_ARTICLE_LINK_MSG = 'missing article link'
    MISSING_DIARY_CODE = 2009
    MISSING_DIARY_MSG = 'missing diary content'
    MISSING_UNIONID_CODE = 2010
    MISSING_UNIONID_MSG = 'missing unionid'
    MISSING_SOURCE_CODE = 2011
    MISSING_SOURCE_MSG = 'missing source info'
    MISSING_DEVICE_NAME_CODE = 2012
    MISSING_DEVICE_NAME_MSG = 'missing device name'
    MISSING_OPENID_DID_CODE = 2013
    MISSING_OPENID_DID_MSG = 'missing openid or device id'
    MISSING_FACTORY_UID_CODE = 2014
    MISSING_FACTORY_UID_MSG = 'missing factory uid'
    MISSING_DEVICE_TYPE_CODE = 2015
    MISSING_DEVICE_TYPE_MSG = 'missing device type'
    # ============================= 30xx ==================== 提示
    # 设备不在线
    ALERT_DEVICE_OFFLINE_CODE = 3001
    ALERT_DEVICE_OFFLINE_MSG = "device offline"
    ALERT_DEVICE_ONLINE_CODE = 3002
    ALERT_DEVICE_ONLINE_MSG = " device online"
    ALERT_DEVICE_UNKNOWN_CODE = 3003
    ALERT_DEVICE_UNKNOWN_MSG = "device unknown"
    ALERT_DEVICE_BIND_CODE = 3004
    ALERT_DEVICE_BIND_MSG = "device already bind"
    ALERT_DEVICE_support_CODE = 3005
    ALERT_DEVICE_support_MSG = "device not support"
    # ============================= 40xx ==================== 错误
    ERROR_PUSH_INSTRUCTION_CODE = 4001
    ERROR_PUSH_INSTRUCTION_MSG = "push instruction error"
    ERROR_NOTICE_REPORT_STATUS_CODE = 4002
    ERROR_NOTICE_REPORT_STATUS_MSG = "notice report status error"
    ERROR_OPENID_DID_STATUS_CODE = 4003
    ERROR_OPENID_DID_STATUS_MSG = "device_id not match with openid"
    ERROR_WECHAT_SEND_ERROR_CODE = 4004
    ERROR_WECHAT_SEND_ERROR_MSG = 'wechat send msg error'
    ERROR_IMG_URL_TYPE_CODE = 4005
    ERROR_IMG_URL_TYPE_MSG = 'img_url is not a list'
    ERROR_TOKEN_CODE = 4006
    ERROR_TOKEN_CODE_MSG = 'TOKEN error'
    # command无效
    INVALID_COMMAND_CODE = 4007
    INVALID_COMMAND_MSG = "invalid command"
    # command value无效
    INVALID_COMMAND_VALUE_CODE = 4008
    INVALID_COMMAND_VALUE_MSG = "invalid command value"

    # ============================= redis cache key =============
    DEVICE_DANGER_CODE_PREFIX = "device_danger_code_prefix"
    DEVICE_CONTROL_PREFIX = 'device_control_prefix'
    TEST_DEVICE_STATUS_PREFIX = 'test_device_status_prefix'
