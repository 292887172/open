# !/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from conf.emailconf import *
import logging

__author__ = 'rdy'


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
    # me = "53iqCloudDev" + "<" + MAIL_USER + "@" + MAIL_POSTFIX + ">"
    msg = MIMEText(text, _subtype='html', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = MAIL_USER
    msg['To'] = to_user
    try:
        server = smtplib.SMTP()
        server.connect(MAIL_HOST)
        # server.debuglevel(1)
        server.login(MAIL_USER, MAIL_PWD)
        server.sendmail(MAIL_USER, to_user, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(e)
        logging.getLogger('').info("发送邮件出错"+str(e))
        return False


def send_product_process_email(title, product_name, process_name, next_process, handler, to_user, detail_url, action):
    if action == 'submit':
        # 文件提交发送邮件
        text = '<html><head lang="en"><style>' \
               '.content{width: 100%;height: 450px;}.header{width: 100%;border-bottom: 1px solid #333;}' \
               '.ui-body{width: 100%;height: 260px;border-bottom: 1px dashed #333;padding-left: 10px;padding-top: 6px;}' \
               '.foot{padding-left: 12px;}.foot p{font-size: 12px;color: #909090;}p{padding-left:2em}' \
               '.strong-text{font-weight:bolder}' \
               '</style></head><body><div class ="content"><div class ="header">' \
               '<img src = "http://storage.56iq.net/group1/M00/00/52/CgoKRFZFVM2AFzQRAAA4t_Adb_k940.png">' \
               '</div><div class ="ui-body"> <h3> 尊敬的开发者，您好！ </h3> <label style="padding-left: 2em"> ' \
               '您的'+product_name+'文件已更新，请尽快确认并进行下一步操作：<span class="strong-text">'+next_process+'。' \
                '</span></label><p>产品名称: <span class="strong-text">' + \
               product_name+'</span></p><p>文件:<span class="strong-text"> '+process_name+'</span></p><p>发布者: '\
               + handler+'</p><p>详情请查看: <a href="' + \
               detail_url + '">' + detail_url + '</a></p></div>' \
               '<div class ="foot"><p> 53iq厨电开发平台项目组 </p> <p> 本邮件由系统自动发送，请勿直接回复！ </p> ' \
                '<p> 如果您有任何疑问或建议，请联系我们：support@53iq.com </p></div></div></body></html>'
        pass
    elif action == 'confirm':
        # 进度确认邮件
        text = '<html><head lang="en"><style>' \
               '.content{width: 100%;height: 450px;}.header{width: 100%;border-bottom: 1px solid #333;}' \
               '.ui-body{width: 100%;height: 210px;border-bottom: 1px dashed #333;padding-left: 10px;padding-top: 6px;}' \
               '.foot{padding-left: 12px;}.foot p{font-size: 12px;color: #909090;}p{padding-left:2em}' \
               '.strong-text{font-weight:bolder}' \
               '</style></head><body><div class ="content"><div class ="header">' \
               '<img src = "http://storage.56iq.net/group1/M00/00/52/CgoKRFZFVM2AFzQRAAA4t_Adb_k940.png">' \
               '</div><div class ="ui-body"> <h3> 尊敬的开发者，您好！ </h3> <label style="padding-left: 2em"> ' \
               '您的<span class="strong-text">'+product_name+process_name+'</span>已由 <span class="strong-text">' + handler +'</span> 确认。请尽快进行下一步操作：<span class="strong-text">'+next_process+'</span>' \
                '。</label><p>详情请查看: <a href="' + \
               detail_url + '">' + detail_url + '</a></p></div>' \
               '<div class ="foot"><p> 53iq厨电开发平台项目组 </p> <p> 本邮件由系统自动发送，请勿直接回复！ </p> ' \
               '<p> 如果您有任何疑问或建议，请联系我们：support@53iq.com </p></div></div></body></html>'
        pass
    msg = MIMEText(text, _subtype='html', _charset='utf-8')
    msg['Subject'] = title
    msg['From'] = MAIL_USER

    try:
        server = smtplib.SMTP()
        server.connect(MAIL_HOST)
        # server.debuglevel(1)
        server.login(MAIL_USER, MAIL_PWD)
        if isinstance(to_user, list):
            for i in to_user:
                msg['To'] = i
                server.sendmail(MAIL_USER, i, msg.as_string())
        else:
            msg['To'] = to_user
            server.sendmail(MAIL_USER, to_user, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(e)
        logging.getLogger('').info("发送邮件出错" + str(e))
        return False

if __name__ == "__main__":
    r = send_product_process_email("油烟机已提交正式UI和UE v1.0", '油烟机', '提交正式UI和UE v1.0', '提交蒸烤箱详细技术功能规格书', '15256734655', ['rendy@53iq.com', 'liuwu@53iq.com'], 'http://www.553iq.com', 'submit')
    print(r)