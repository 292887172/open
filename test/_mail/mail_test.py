# coding=utf-8
import os
import logging
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import email
import time
import imaplib

MAIL_HOST = 'mail.56iq.com'
MAIL_USER = 'support@53iq.com'
MAIL_PWD = 'support@#abc'
MAIL_POSTFIX = '53iq.com'
FROM_ADDRESS = 'support@53iq.com'


def mail_info(info, to_address, type='', subject='', imgs=[]):
    # todo 使用公司邮箱发送给qq邮箱会出现乱码
    """
    :param info: 邮件文本内容，或html内容
    :param to_address: 接受者邮箱 eq:123@mail.com
    :param type: plain(文本) or html(html)
    :param subject: 邮件显示的主题
    :param img: 是否附带发送图片， [] 没有图片，list [{'name':'img name','path':'img path'}]
    """
    type = type if type != '' else 'plain'
    subject = subject if subject != '' else FROM_ADDRESS

    if len(imgs) == 0:
        message = MIMEText(info, type, 'utf-8')
    elif len(imgs) == 1:
        message = MIMEMultipart()
        mail_body = MIMEText(info, type, 'utf-8')
        message.attach(mail_body)
        img_item = MIMEApplication(open(imgs[0]['path'], 'rb').read())
        img_item.add_header('Content-Disposition', 'attachment', filename=imgs[0]['name'])
        message.attach(img_item)
    else:
        message = MIMEMultipart()
        mail_body = MIMEText(info, type, 'utf-8')
        message.attach(mail_body)
        for img in imgs:
            img_item = MIMEApplication(open(img['path'], 'rb').read())
            img_item.add_header('Content-Disposition', 'attachment', filename=img['name'])
            message.attach(img_item)
    message['Subject'] = Header(subject)
    message['From'] = Header(FROM_ADDRESS)
    message['To'] = Header(to_address)

    smtp = None
    try:
        smtp = smtplib.SMTP(MAIL_HOST)
        smtp.login(MAIL_USER, MAIL_PWD)
        smtp.sendmail(FROM_ADDRESS, to_address, message.as_string())
    except smtplib.SMTPException as e:
        logging.error("邮件发送失败" + str(to_address) + '错误' + str(e))
    finally:
        smtp.quit()
        logging.info("邮件发送成功" + str(to_address))


if __name__ == '__main__':
    my_email = 'fuxy@53iq.com'
    imgs = [{'path': '1.jpg', 'name': '图片1.jpg'}, {'path': '2.jpg', 'name': '图片2.jpg'}]
    mail_info('<h1>test - info</h1>', my_email, 'html', subject='测试邮件', imgs=imgs)
    my_email = '1247079575@qq.com'
    mail_info('<h1>test - info</h1>', my_email, 'html', subject='测试邮件', imgs=imgs)
