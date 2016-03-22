# !/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'rdy'
import smtplib
from email.mime.text import MIMEText
from conf.emailconf import *


def send_mail(to_user, sub, code):
    if len(code) > 7:
        # 邮箱注册验证地址
        text = '<html><head lang="en"><style>' \
               '.content{width: 100%;height: 450px;}.header{width: 100%;border-bottom: 1px solid #333;}' \
               '.ui-body{width: 100%;height: 150px;border-bottom: 1px dashed #333;padding-left: 10px;padding-top: 6px;}' \
               '.foot{padding-left: 12px;}.foot p{font-size: 12px;color: #909090;}' \
               '</style></head><body><div class ="content"><div class ="header"><img src = "http://storage.56iq.net/group1/M00/00/52/CgoKRFZFVM2AFzQRAAA4t_Adb_k940.png">' \
               '</div><div class ="ui-body"> <h3> 亲爱的53iq用户，您好！ </h3> <label style="padding-left: 2em"> 感谢您注册53iq智能云开发者，请点击链接完成注册： ' \
               '<a href="' + code + '">' + code + '</a>(30分钟内有效,如非本人操作请忽略) </label> </div><div class ="foot"> <p> 本邮件由系统自动发送，请勿直接回复！ </p> <p> 如果您有任何疑问或建议，请联系我们：support@53iq.com </p> ' \
                                                  '</div></div></body></html>'
    else:
        # 邮箱发送验证码
        text = '<html><head lang="en"><style>' \
               '.content{width: 100%;height: 450px;}.header{width: 100%;border-bottom: 1px solid #333;}' \
               '.ui-body{width: 100%;height: 150px;border-bottom: 1px dashed #333;padding-left: 10px;padding-top: 6px;}' \
               '.foot{padding-left: 12px;}.foot p{font-size: 12px;color: #909090;}' \
               '</style></head><body><div class ="content"><div class ="header"><img src = "http://storage.56iq.net/group1/M00/00/52/CgoKRFZFVM2AFzQRAAA4t_Adb_k940.png">' \
               '</div><div class ="ui-body"> <h3> 亲爱的53iq用户，您好！ </h3> <label style="padding-left: 2em"> 感谢您使用53iq厨房智能云，本次申请验证码为： ' \
               '<strong>' + code + '</strong> 不区分大小写(10分钟内有效,如非本人操作请忽略) </label> </div><div class ="foot"> <p> 本邮件由系统自动发送，请勿直接回复！ </p> <p> 如果您有任何疑问或建议，请联系我们：support@53iq.com </p> ' \
                                   '</div></div></body></html>'
    me = "53iqCloudDev" + "<" + MAIL_USER + "@" + MAIL_POSTFIX + ">"
    msg = MIMEText(text, _subtype='html', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = to_user
    try:
        server = smtplib.SMTP()
        server.connect(MAIL_HOST)
        # server.debuglevel(1)
        server.login(MAIL_USER, MAIL_PWD)
        server.sendmail(me, to_user, msg.as_string())
        server.close()
        return True
    except Exception as e:
        del e
        return False
