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
    :return: 成功 -> 用户定义的帧协议  ，  失败 -> false
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
            # 功能定义的必须字段
            item['name'] = config['Stream_ID']
            item['length'] = int(config['mxsLength'])
            item['title'] = config['name']
            # 功能定义中的UI关联与控制器
            item['triggers'], item['controls'] = {}, []
            for mxs in config['mxs']:
                if mxs.get('control'):
                    if '=' in mxs['control']:
                        _key, _value = mxs['control'].split('=')
                        item['controls'].append({_key: int(_value)})
                    else:
                        item['controls'].append(int(mxs['control']))
                data = "[%s]" % mxs['data']
                if mxs.get('trigger') and len(mxs.get('trigger')):
                    _item = {}
                    for trigger in mxs['trigger']:
                        _item[trigger['func']] = int(trigger['val'])
                    item['triggers'][data] = _item
            if not item['triggers']: del item['triggers']
            if not item['controls']:
                del item['controls']
            else:
                _control_dict, _controls_set = [], set()
                for control in item['controls']:
                    if isinstance(control, dict):
                        _control_dict.append(control)
                    if isinstance(control, int):
                        _controls_set.add(control)
                item['controls'] = _control_dict + list(_controls_set)
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


def change_value(value):
    if len(value) == 4:
        return [int(value[0:2], 16), int(value[2:4], 16)]
    elif len(value) == 2:
        return [int(value, 16)]
    else:
        return ['Get Value False']


def get_check_data_location(check_id, frame_contents, position):
    if isinstance(check_id, str):
        check_id = int(check_id)

    length_sum, length_position, length_check_id = 0, 0, 0

    for frame_content in frame_contents:
        length_sum += int(frame_content['length'])
        if int(frame_content['id']) == check_id:
            length_check_id = int(frame_content['length'])
        if int(frame_content['id']) <= check_id:
            length_position += int(frame_content['length'])

    if position == 'start':
        return length_position - length_check_id
    elif position == 'end':
        return length_position - length_sum


def get_device_protocol_config(key: str):
    """
    :param key: 用户的key
    :return: 成功 > 用户的自定义协议配置  ，  失败 > False
    """

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
        # print(protocol_content)
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
            item['check_data_start'] = get_check_data_location(config['start_check_number'],
                                                               config['frame_content'], 'start')
            item['check_data_end'] = get_check_data_location(config['end_check_number'],
                                                             config['frame_content'], 'end')
            structs = []
            for frame_content in config['frame_content']:
                _item = {}
                _item['name'] = frame_content['name']
                _item['length'] = int(frame_content['length'])
                # 通过功能定义获取data数据长度
                # if _item['name'] == 'data':
                #     _item['length'] = get_data_length(key)
                _item['value'] = []
                if isinstance(frame_content['value'], str):
                    _item['value'] += change_value(frame_content['value'])
                elif isinstance(frame_content['value'], list):
                    for value in frame_content['value']:
                        if value.get('value'):
                            _item['value'] += change_value(value['value'])
                elif isinstance(frame_content['value'], dict):
                    if frame_content['value'].get('value'):
                        _item['value'] += change_value(frame_content['value']['value'])
                if not _item['value']:
                    del _item['value']
                structs.append(_item)
            item['structs'] = structs
            item['length'] = sum([struct['length'] for struct in structs])
            if protocol_type == 0:
                configs.insert(0, item)
            else:
                configs.append(item)
        except Exception as e:
            logging.error(str(e))

    if len(configs) == 1:
        return configs * 2
    else:
        return configs


def test_get_device_function():
    # 5yUHe7fk test　success
    device_function = get_device_function(key='nzammHmF')
    pprint.pprint(device_function)


def test_get_device_protocol_config():
    device_protocol_config = get_device_protocol_config(key='nzammHmF')
    pprint.pprint(device_protocol_config, width=80, indent=4)


def test_get_check_data_location():
    protocols = Protocol.objects.filter(protocol_device_key='xN6C2bCr')
    for protocol in protocols:
        protocol_content = protocol.protocol_factory_content
        config = json.loads(protocol_content)
        frame_contents = config['frame_content']

        check_start = config['start_check_number']
        print('check_start_id = ', check_start)
        print('check_location = ', get_check_data_location(check_start, frame_contents, 'start'))

        check_end = config['end_check_number']
        print('check_end_id = ', check_end)
        print('check_location = ', get_check_data_location(check_end, frame_contents, 'end'))


if __name__ == '__main__':
    test_get_device_function()
    print('-' * 99)
    test_get_device_protocol_config()
    # print('-' * 99)
    # test_get_check_data_location()
