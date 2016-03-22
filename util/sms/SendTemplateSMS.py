# -*- coding: UTF-8 -*-
from conf.smsconf import ACCOUNTSID, ACCOUNTTOKEN, APPID
from util.sms.CCPRestSDK import REST

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = 8883

# REST版本号
softVersion = '2013-12-26'


def sendTemplateSMS(to, datas, tempId=34882):
    """
    发送模板短信
    您的验证码是：{1}，有效期{2}分钟，请勿泄漏给他人。如非本人操作，可不用理会。
    :param to:手机号码
    :param datas: 内容数据 格式为数组 例如：['12','34']，如不需替换请填 ''
    :param tempId:模板Id
    :return:
    """
    # 初始化REST SDK
    rest = REST(serverIP, serverPort, softVersion)
    rest.setAccount(ACCOUNTSID, ACCOUNTTOKEN)
    rest.setAppId(APPID)

    result = rest.sendTemplateSMS(to, datas, tempId)
    for k, v in result.items():
        if k == 'templateSMS':
            for k, s in v.items():
                print('%s:%s' % (k, s))
        else:
            print('%s:%s' % (k, v))


if __name__ == "__main__":
    sendTemplateSMS("15553483801", ['8888', '10'], 34882)