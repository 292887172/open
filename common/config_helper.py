# coding=utf-8
import django
import json
import pprint

django.setup()

from model.center.app import App
from model.center.protocol import Protocol


def get_device_function(key):
    try:
        app = App.objects.get(app_appid__contains=key)
    except Exception as e:
        pass
    configs = json.loads(app.device_conf)
    device_function = []
    for config in configs:
        item = {}
        item['length'] = int(config['mxsLength'])
        item['name'] = config['Stream_ID']
        item['title'] = config['name']

        if config['Stream_ID'] == 'Fan3':
            item['controls'] = {'Main': 113}

        device_function.append(item)
    return device_function


name_map = {
    'frame_head': 'head',
    'frame_type': 'type',
    'frame_length': 'length',
    'data_domain': 'data'
}


def get_data_length(key):
    try:
        app = App.objects.get(app_appid__contains=key)
    except Exception as e:
        pass
    configs = json.loads(app.device_conf)
    data_len = 0
    for config in configs:
        data_len += int(config['mxsLength'])
    return int(data_len / 8)


def get_device_protocol_config(key):
    """

    :param key:
    :return:  list  [0]
    """
    protocols = Protocol.objects.filter(protocol_device_key=key)

    items = []
    for protocol in protocols:
        protocol_type = protocol.protocol_factory_type
        protocol_content = protocol.protocol_factory_content
        config = json.loads(protocol_content)

        if protocol_type == 0:
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
                if _item['name'] in name_map.keys(): _item['name'] = name_map[_item['name']]
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
            _sum = 0
            for struct in structs:
                try:
                    _sum += struct['length']
                except KeyError:
                    pass
            item['length'] = _sum

            items.insert(0, item)
        else:
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
                if _item['name'] in name_map.keys(): _item['name'] = name_map[_item['name']]
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
            _sum = 0
            for struct in structs:
                try:
                    _sum += struct['length']
                except KeyError:
                    pass
            item['length'] = _sum

            items.append(item)
    return items


if __name__ == '__main__':
    device_function = get_device_function(key='vUN5MyX2')
    pprint.pprint(device_function)

    print('\n')

    device_protocol_config = get_device_protocol_config(key='vUN5MyX2')
    pprint.pprint(device_protocol_config[0], width=200)
    pprint.pprint(device_protocol_config[1], width=200)
