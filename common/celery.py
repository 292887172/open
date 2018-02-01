from celery import Celery, platforms

from conf.commonconf import IS_DEBUG,KEY_URL

import requests


if IS_DEBUG:
    celery = Celery('celerytask', broker='redis://:smart.53iq.com@56iq@192.168.0.62:6379/7')
else:
    celery = Celery('celerytask', broker='redis://:smart.53iq.com@56iq@127.0.0.1:6379/10')
# celery = Celery('celerytask', broker='redis://:smart.53iq.com@56iq@192.168.0.62:6379/8')
# 让其支持使用root
platforms.C_FORCE_ROOT = True


@celery.task
def add(developer_id, app_name, app_model, app_category, app_category_detail, app_command,
        device_conf, app_factory_id, app_group, app_logo):

    from common.app_helper import create_app
    from common.smart_helper import update_app_protocol
    result = create_app(developer_id, app_name, app_model, app_category, app_category_detail, app_command,
                        device_conf, app_factory_id, app_group, app_logo)
    update_app_protocol(result)
    app_key = result.app_appid
    key = app_key[-8:]
    requests.get(KEY_URL, params={'key': key})


if __name__ == "__main__":
    print("开始调用...")
