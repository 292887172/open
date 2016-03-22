import hashlib


# md5加密
def md5(content):
    # md5加密
    # 创建md5对象
    m = hashlib.md5()
    # 生成加密串，其中 password 是要加密的字符串

    m.update(content.encode('utf-8'))
    m.digest()
    # 获取加密串
    psw = m.hexdigest()
    return psw
