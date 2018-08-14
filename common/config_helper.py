# coding=utf-8
import django
import json
import pprint
import logging

logging.basicConfig(level=logging.INFO)

django.setup()

from model.center.app import App
from model.center.protocol import Protocol

"""
默认使用Django的ORM进行数据查询，单独运行此py文件时，在pycharm中配置
PYTHONUNBUFFERED=1;DJANGO_SETTINGS_MODULE=open.settings
"""


def get_device_function(key: str) -> list:
    """获取用户定义的帧协议
    :param key: 用户的key
    :return: 成功 -》 用户定义的帧协议  ，  失败 -》 false
    """
    try:
        app = App.objects.get(app_appid__contains=key)
    except Exception as e:
        logging.error('查询数据失败 key=%s' % key)
        logging.error(str(e))
        return False
    try:
        configs = json.loads(app.device_conf)
        device_function = []
        for config in configs:
            item = {}
            item['length'] = int(config['mxsLength'])
            item['name'] = config['Stream_ID']
            item['title'] = config['name']
            # TODO 测试时默认绑定一个UI ID ，后续需要删除
            if config['Stream_ID'] == 'Fan3':
                item['controls'] = {'Main': 113}
            device_function.append(item)
        return device_function
    except Exception as e:
        logging.error(str(e))
        return False


def get_data_length(key: str) -> int:
    """
    根据用户定义的功能列表，计算自定义帧协议中 data_domain 的数据长度
    :param key: 用户的Key
    :return: 成功 数据域长度  失败 false
    """
    try:
        app = App.objects.get(app_appid__contains=key)
        configs = json.loads(app.device_conf)
        data_len = 0
        for config in configs:
            data_len += int(config['mxsLength'])
        return int(data_len / 8)
    except Exception as e:
        logging.error(str(e))
        return False


def get_device_protocol_config(key: str):
    """
    :param key: 用户的key
    :return: 成功 》 用户的自定义协议配置  ，  失败 》 False
    """

    # 命名转换。数据库与帧代码中保持一致
    name_map = {
        'frame_head': 'head',
        'frame_type': 'type',
        'frame_length': 'length',
        'data_domain': 'data'
    }
    try:
        protocols = Protocol.objects.filter(protocol_device_key=key)
    except Exception as e:
        logging.error('key=' + key + ' ' + str(e))

    if not protocols:
        logging.error('protocols ' + str(protocols))
        return False

    configs = []
    for protocol in protocols:
        protocol_type = protocol.protocol_factory_type
        protocol_content = protocol.protocol_factory_content
        try:
            config = json.loads(protocol_content)
        except Exception as e:
            logging.error('转换失败 ' + str(protocol_content))
            logging.error(str(e))

        try:
            item = {}
            item['endian_type'] = int(config['endian_type'])
            item['length_offset'] = 'None'
            item['check_type'] = config['checkout_algorithm']
            item['check_data_start'] = int(config['start_check_number'])
            item['check_data_end'] = int(config['end_check_number'])

            structs = []
            for frame_content in config['frame_content']:
                _item = {}
                _item['name'] = frame_content['name']
                if _item['name'] in name_map.keys():
                    _item['name'] = name_map[_item['name']]
                try:
                    if frame_content['name'] == 'data_domain':
                        _item['length'] = get_data_length(key)
                    else:
                        _item['length'] = int(frame_content['length'])
                except KeyError:
                    pass

                _item['value'] = []
                if len(frame_content['code']) > 0:
                    for code in frame_content['code']:
                        if len(code['value']) == 4:
                            _item['value'].append(int(code['value'][0:2], 16))
                            _item['value'].append(int(code['value'][2:4], 16))
                        else:
                            _item['value'].append(int(code['value'], 16))
                if not _item['value']: del _item['value']
                structs.append(_item)
            item['structs'] = structs
            item['length'] = sum([struct['length'] for struct in structs])

            if protocol_type == 0:
                configs.insert(0, item)
            else:
                configs.append(item)
        except Exception as e:
            logging.error(str(e))
    if configs:
        return configs
    else:
        return False


def test_get_device_function():
    device_function = get_device_function(key='q8qG3tq7')
    pprint.pprint(device_function)


def test_get_device_protocol_config():
    device_protocol_config = get_device_protocol_config(key='q8qG3tq7')
    pprint.pprint(device_protocol_config, width=200, indent=4)


if __name__ == '__main__':
    test_get_device_function()

    test_get_device_protocol_config()
