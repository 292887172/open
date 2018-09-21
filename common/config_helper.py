 # coding=utf-8
import django
import json
import pprint
import logging
import re

from package.slpp_23.slpp import slpp as lua

logging.basicConfig(level=logging.INFO)

django.setup()

from model.center.app import App
from model.center.protocol import Protocol

"""
默认使用Django的ORM进行数据查询，单独运行此py文件时，在pycharm中配置
PYTHONUNBUFFERED=1;
DJANGO_SETTINGS_MODULE=open.settings
"""


def get_all_device_function(key: str):
    device_function = {}
    try:
        app = App.objects.get(app_appid__contains=key)
        configs = json.loads(app.device_conf)
        device_function = []
        for config in configs:
            item = {}
            # 功能定义的必须字段
            item['name'] = config['Stream_ID']
            item['length'] = int(config['mxsLength'])
            item['title'] = config['name']
            item['values'] = []
            for mxs in config['mxs']:
                item['values'].append({'data': mxs['data'], 'desc': mxs['desc']})
            device_function.append(item)
        device_function = ('{"function":' + str(device_function).replace("'", '"') + "}")

    except Exception as e:
        print(str(e))
    finally:
        print(pprint.pformat(json.loads(device_function), width=200).replace("'", '"'))
        # print(json.dumps(json.loads(device_function), indent=4, ensure_ascii=False))


def get_device_function(key: str) -> list or 'false':
    """ 获取用户定义的帧协议

    :param key: 用户的key
    :return: 成功 -> 用户定义的帧协议  ，  失败 -> false
    """

    def get_ids(ids):
        new_ids = []
        for item in ids:
            if item.isdigit():
                new_ids.append(int(item))
            elif ':' in item:
                key, value = item.split(':')
                if value.isdigit():
                    new_ids.append({key: int(value)})
                else:
                    new_ids.append({key: value})
        return new_ids

    def get_params(params):
        new_params = []
        for item in params:
            _new_params = []
            if item.isdigit():
                _new_params.append(int(item))
            elif ':' in item:
                values = item.split(':')
                for value in values:
                    if value.isdigit():
                        _new_params.append(int(value))
                    else:
                        _new_params.append(value)
            new_params.append(_new_params)
        return new_params

    def get_control_items(ids, wedgit, params):
        if not ids:
            return []
        if ids and not wedgit:
            return get_ids(ids)
        if ids and wedgit:
            controls = []
            params = get_params(params)
            for item in get_ids(ids):
                if isinstance(item, int):
                    if not params:
                        controls.append({'id': item, 'wedgit': wedgit})
                    else:
                        controls.append({'id': item, 'wedgit': wedgit, 'params': params})

                elif isinstance(item, dict):
                    for k, v in item.items():
                        if not params:
                            controls.append(k + '=')
                            controls.append({'id': v, 'wedgit': wedgit})
                        else:
                            controls.append(k + '=')
                            controls.append({'id': v, 'wedgit': wedgit, 'params': params})
            return controls

    def get_triggers(triggers):
        new_triggers = {}
        for key, value in triggers.items():
            if value == {}:
                continue
            print(key, value)
            _item = {}
            for k, v in value.items():
                if v.isdigit():
                    _item[k] = int(v)
            new_triggers[key] = _item
        return new_triggers

    try:
        app = App.objects.get(app_appid__contains=key)
    except Exception as e:
        logging.error('查询数据失败 key={} \n {}'.format(key, str(e)))
        return False

    configs = json.loads(app.device_conf)

    ## 输出原始的配置信息
    # try:
    #     _configs = ('{"function":' + str(configs) + "}").replace("'", '"')
    #     _configs = json.loads(_configs)
    #     print(pprint.pformat(_configs))
    # except:
    #     print(configs, end='\n\n')

    device_functions = []
    for config in configs:
        function = {}
        function['name'] = config['Stream_ID']
        function['length'] = int(config['mxsLength'])
        function['title'] = config['name']
        function['triggers'], function['controls'] = {}, {}

        # 功能定义中的UI关联与控制器
        if config.get('control'):
            ids = config['control']['uid']
            wedgit = config['control']['wedgit']
            params = config['control']['params']

            function['controls'] = get_control_items(ids, wedgit, params)

        # 获取前的触发器示例 'triggers': {'[1]': {'Fast': 0, 'Slow': 0}}
        for mxs in config['mxs']:
            data = "[{0}]".format(mxs['data'])
            value = {}
            if mxs.get('trigger'):
                for trigger in mxs['trigger']:
                    value[trigger['func']] = trigger['val']
            function['triggers'][data] = value

        function['triggers'] = get_triggers(function['triggers'])
        device_functions.append(function)

        if not function['triggers']:
            del function['triggers']
        if not function['controls']:
            del function['controls']

    return device_functions


def get_device_protocol_config(key: str) -> list or 'false':
    """
    获取自定义协议解析的规则 \n
    解析成功返回 [上行规则，下行规则] \n
    如果只有上行规则或下行规则返回 [规则]*2 \n

    :param key: 用户的key
    :return: 成功 > 用户的自定义协议配置  ，  失败 > False
    """

    def get_data_length(key: str) -> int or 'false':
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

    def get_check_data_location(check_id, frame_contents, position):
        """ 解析帧，获取帧的起始校验码位置和结束校验码位置，

        校验位置计算是计算需要校验的数据在数据中的位置，并根据位置计算偏移量

        :param check_id: 需要校验数据的ID
        :param frame_contents: 所有的帧协议数据
        :param position: 获取校验起始位，或结束位
        :return: 校验数据的位置
        """

        if isinstance(check_id, str):
            check_id = int(check_id)

        length_sum = sum([int(frame_content['length']) for frame_content in frame_contents])

        length_position, length_check_id = 0, 0
        for frame_content in frame_contents:
            length_position += int(frame_content['length'])
            if int(frame_content['id']) == check_id:
                length_check_id = int(frame_content['length'])
                break

        if position == 'start':
            return length_position - length_check_id
        elif position == 'end':
            return length_position - length_sum

    def change_value(value: hex) -> list or 'false':
        """ 数据之间的转换

        '0011' (hex) -> [0,17]

        '01' -> [1]

        :param value: 需要转换的十六进制数
        :return: 十进制数组成的数组
        """
        if len(value) == 4:
            return [int(value[0:2], 16), int(value[2:4], 16)]
        elif len(value) == 2:
            return [int(value, 16)]
        else:
            logging.error(['Get Value False'])
            return False

    try:
        protocols = Protocol.objects.filter(protocol_device_key=key)
    except Exception as e:
        protocols = []
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
    # 标准集成灶 BTO9ciBr
    device_function = get_device_function(key='BTO9ciBr')

    # js = json.dumps(device_function, indent=4, ensure_ascii=False)
    # print(js)

    pprint.pprint(device_function, width=100, indent=4)
    print('\n' + '-' * 40 + '   test_get_device_function   ' + '-' * 40, end='\n\n')


def test_get_device_protocol_config():
    device_protocol_config = get_device_protocol_config(key='BTO9ciBr')
    pprint.pprint(device_protocol_config, width=80, indent=4)
    print('\n' + '-' * 40 + '   test_get_device_protocol_config   ' + '-' * 40, end='\n\n')


def test_config_change():
    data = '{id=103,weight="time_button",params={value={1,2,3},progress=104}}'
    data = lua.decode(data)
    print(data, type(data))
    print('\n' + '-' * 40 + '   test_config_change   ' + '-' * 40, end='\n\n')


def test_change_device_function(device_function):
    from common.project_helper import config_change
    print(config_change(device_function))


if __name__ == '__main__':
    # test_get_device_function()

    # test_get_device_protocol_config()

    # test_config_change()

    device_function = get_device_function("MCKjIJWI")

    if device_function:
        pprint.pprint(device_function)
        print('-' * 100)
        test_change_device_function(device_function)
