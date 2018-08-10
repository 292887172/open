# coding=utf-8
import django
import json
import pprint

django.setup()

from model.center.app import App
from model.center.protocol import Protocol


def get_device_function(key='53zzqa8Qq6HAXF6nMz'):
    app = App.objects.get(app_appid=key)
    configs = json.loads(app.device_conf)
    device_function = []
    for config in configs:
        item = {}
        item['length'] = config['mxsLength']
        item['name'] = config['Stream_ID']
        item['title'] = config['name']
        device_function.append(item)
    return device_function


def get_device_protocol_config(key='5yUHe7fk'):
    protocol = Protocol.objects.get(protocol_device_key=key)
    protocol_type = protocol.protocol_factory_type
    protocol_content = protocol.protocol_factory_content
    config = json.loads(protocol_content)
    item = {}
    if protocol_type == 1:
        pass
    else:
        item['endian_type'] = int(config['endian_type'])
        item['length_offset'] = 'None'
        item['check_type'] = config['checkout_algorithm']
        item['check_data_start'] = int(config['start_check_number'])
        item['check_data_end'] = int(config['end_check_number'])
        structs = []
        for frame_content in config['frame_content']:
            _item = {}
            _item['name'] = frame_content['name']
            _item['length'] = int(frame_content['length'])
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
        item['length'] = sum([item['length'] for item in structs])
    return item


if __name__ == '__main__':
    device_function = get_device_function()
    pprint.pprint(device_function)

    print('\n')

    device_protocol_config = get_device_protocol_config()
    pprint.pprint(device_protocol_config, width=200)
