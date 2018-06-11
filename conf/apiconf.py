# !/bash/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'rdy'

wx_oauth = "https://api.weixin.qq.com/sns/oauth2/access_token?appid={0}&secret={1}&code={2}&grant_type=authorization_code"
wx_userinfo = "https://api.weixin.qq.com/sns/userinfo?access_token={0}&openid={1}"

wx_ticket = "http://wechat.53iq.com/partner/ddb4c038579a11e59e8800a0d1eb6068/jsapi_ticket?token=hi"
INSIDE_MESSAGE_PUSH="https://api.53iq.com/1/message/push?access_token={0}"
DOWNLOAD_ZIP = "http://oven.53iq.com/static/file/{0}.zip"