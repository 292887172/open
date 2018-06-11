# !/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib

__author__ = 'achais'


def md5_16(value):
    """
    MD5加密 16位
    :param value:
    :return: 生成16位加密数据
    """
    return md5_en(value)[8:-8]


def md5_en(value):
    """
    MD5加密
    :param value:
    :return:
    """
    md5 = hashlib.md5()
    md5.update(str(value).encode('utf-8'))
    return md5.hexdigest()


def sha1_en(value):
    """
    SHA1加密
    :param value:
    :return:
    """
    sha = hashlib.sha1()
    sha.update(str(value).encode('utf-8'))
    return sha.hexdigest()


def sha256_en(value):
    """
    SHA256加密
    :param value:
    :return:
    """
    sha256 = hashlib.sha256()
    sha256.update(str(value).encode('utf-8'))
    return sha256.hexdigest()


if __name__ == '__main__':
    a = md5_en('wudt@#abc')
    print(a)
    # pbkdf2_sha256$12000$VbOA0Yl0RKXF$V69hbz7+e6gVAwtnG0Kjj3glupbiWNPKbnuTquSWorE=