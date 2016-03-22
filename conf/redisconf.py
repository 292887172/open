# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'rdy'

# sandbox_api_redis_config
SANDBOX_API_REDIS_HOST = "192.168.0.62"
SANDBOX_API_REDIS_PORT = 6379
SANDBOX_API_REDIS_DB = 4
SANDBOX_API_REDIS_PWD = "smart.53iq.com@56iq"

# release_api_redis_config
RELEASE_API_REDIS_HOST = "192.168.0.62"
RELEASE_API_REDIS_PORT = 6379
RELEASE_API_REDIS_DB = 4
RELEASE_API_REDIS_PWD = "smart.53iq.com@56iq"

REDIS_HOST = '192.168.0.62'
REDIS_PORT = 6379
REDIS_PWD = 'smart.53iq.com@56iq'
REDIS_DB = 2

# 短信验证码前缀
SMS_CHECK_CODE_PREFIX = 'sms_check_code_prefix_'
# 短信验证码过期时间单位（10分钟）：秒
SMS_CHECK_CODE_EXPIRE = 10*60

# 邮箱验证码前缀
EMAIL_CHECK_CODE_PREFIX = 'email_check_code_prefix_'
# 邮箱验证码过期时间单位（10分钟）：秒
EMAIL_CHECK_CODE_EXPIRE = 10*60


# 邮箱注册激活前缀
EMAIL_ACTIVE_PREFIX = 'email_active_prefix_'
# 邮箱注册激活过期时间单位（30分钟）：秒
EMAIL_ACTIVE_EXPIRE = 30*60