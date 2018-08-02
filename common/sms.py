import logging

import requests


def verify_code(action, phone, code=''):
    """
    验证码相关方法
    :param action: get or verify
    :param phone: phone number
    :param code: code to be verified
    :return:
    """
    url = "https://iot.53iq.com/1/telephone/code"
    access_token = '38DZq4MHYCA7N6qIA7Ap0MvSv7etzkAA3BKbgCrMcP8X6C458pmcM8Ae8FjqBUl4_e1c54d31720f1e35f7967d2d9b3e559183875cb0'
    try:
        if action == "get":
            res = requests.get(url, params={
                "phone": phone,
                "access_token": access_token,
            }, timeout=10)
            return res.json()
        elif action == "verify":
            res = requests.post(url, params={
                "phone": phone,
                "access_token": access_token,
                "code": code,
            }, timeout=10)
            return res.json()
    except Exception as e:
        logging.getLogger("").exception(e)
        return {"code": -1, "msg": "error"}
