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
    import requests
    r = requests.get("http://storage.56iq.net/group1/M00/47/4E/CgoKQ1thb1uASfKjACuT7CTcmIc555.pkg")
    print(r.headers['content-length'])
    # print(r.content)
    import os

    url = 'http://storage.56iq.net/group1/M00/47/4E/CgoKQ1thb1uASfKjACuT7CTcmIc555.pkg'
    filename = os.path.basename(url)
    print(filename)