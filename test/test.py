# !/usr/bin/env python
# -*- coding: utf-8 -*-
import base64
import os
import shutil

from base.connection import ReleaseApiMongoDBHandler
from util.email.send_email_code import send_mail


def test_name():

    root = "/Users/zhanlingjie/Documents/mypython/Git/open"

    for dirpath, dirnames, filenames in os.walk(root):
        for filepath in filenames:
            if '__' in dirpath:
                try:
                    shutil.rmtree(dirpath)
                    print(dirpath)
                except Exception as e:
                    pass


# def Square(num):
#     temp = str(num)
#     n = 0
#     for index,value in enumerate(temp):
#         if index == len(temp)-1:
#             print(value+'*'+value, end='')
#         else:
#             print(value+'*'+value+' + ', end='')
#         a= int(value)
#         n += a*a
#     print(' = ',n,)
#     if n == 1:
#         return 1
#     return Square(n)
# def countBits(self, num):
#         """
#         :type num: int
#         :rtype: List[int]
#         """
#         list = []
#         for i in range(0,num+1):
#             count = bin(i).count('1')
#             list.append(count)
#         return list


if __name__=="__main__":
    from email import encoders
    from email.header import Header
    from email.mime.text import MIMEText
    from email.utils import parseaddr, formataddr

    import smtplib





    from_addr = 'support@53iq.com'
    password = 'support@#abc'
    to_addr = 'rendy@53iq.com'
    smtp_server = 'mail.53iq.com'
    msg = MIMEText('<html><body><h1>Hello</h1>' +
                   '<p>send by <a href="http://www.python.org">Python</a>...</p>' +
                   '</body></html>', 'html', 'utf-8')
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = Header(u'来自SMTP的问候……', 'utf-8')

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()
    print('ok')