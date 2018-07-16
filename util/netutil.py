import json
import random
import requests
import time
from conf.commonconf import VALIDATE_URL

__author__ = 'sunshine'


def verify_push_url(url, token):
    data = {
        'token': token,
        'timestamp': str(time.time()),
        'nonce': random.randint(10000, 100000),
        'url': url
    }
    try:
        response = requests.post(VALIDATE_URL, data=data, timeout=10)
        if response:
            result = json.loads(response.text)
            print(result)
            if result['code'] == 0:
                return True
    except Exception as e:
        print(e)
    return False

