import os
import sys
import django

sys.path.append(os.path.join(os.path.dirname('.'), '..'))
os.environ['DJANGO_SETTINGS_MODULE'] = 'open.settings'
django.setup()

from model.center.app import App
from celery import Celery, platforms
import requests
from conf.commonconf import IS_DEBUG, KEY_URL


if IS_DEBUG:
    celery = Celery('celerytask', broker='redis://:smart.53iq.com@56iq@192.168.0.62:6379/7')
else:
    celery = Celery('celerytask', broker='redis://:smart.53iq.com@56iq@127.0.0.1:6379/10')
# celery = Celery('celerytask', broker='redis://:smart.53iq.com@56iq@192.168.0.62:6379/8')
# 让其支持使用root
platforms.C_FORCE_ROOT = True


@celery.task
def add(app_id):
    app = App.objects.get(app_id=app_id)
    print(app)
    from common.smart_helper import update_app_protocol
    update_app_protocol(app)
    app_key = app.app_appid
    key = app_key[-8:]
    # requests.get(KEY_URL, params={'key': key})

@celery.task
def get_device():
    pass

if __name__ == "__main__":
    print("开始调用...")
