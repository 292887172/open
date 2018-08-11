# coding=utf-8
import re
import pprint


""" 
基于数据识别转换进行数据转换 

"""


def configs_code(config, key_rule=[], line=False, except_key=[]):
    if line:
        code = '{\n'
    else:
        code = '{'

    def get_item(code, value):
        if key in except_key:
            return code
        if line:
            code += ('\t' + key + '=')
        else:
            code += (key + '=')
        if value == "None":
            code += 'nil'
        elif isinstance(value, str):
            code += ('"' + value + '"')
        elif isinstance(value, int):
            code += str(value)
        elif isinstance(value, list):
            if isinstance(value[0], int):
                code += '{'
                for item in value:
                    item = '0x' + hex(item).lstrip('0x').zfill(2).upper()
                    code += item + ', '
                code = code.rstrip(', ') + '}'
        if line:
            code += ',\n'
        else:
            code += ', '

        return code

    if key_rule:
        for key in key_rule:
            if key in config.keys():
                code = get_item(code, config[key])
    else:
        for key in config.keys():
            if key in config.keys() and key not in key_rule:
                code = get_item(code, config[key])

    code = code.rstrip(', ') + '}'
    return code


def get_device_function(configs):
    key_rule = ['name', 'length', 'title']
    code = '{\n'
    for config in configs:
        code += ('\t' + configs_code(config, key_rule) + ',\n')
    code = code.rstrip(',\n')
    code += '\n}'
    return code

def get_device_protocol_config(config):
    key_rule = ['endian_type', 'length', 'length_offset', 'check_type',
                'check_data_start', 'check_data_end', 'structs']

    code = (configs_code(config, key_rule, True, except_key=['structs']))
    code = code.rstrip('\n}')

    structs_keys = ['name', 'length', 'value']
    structs_value_keys = ['name', 'length', 'title']

    if 'structs' in config.keys():
        code += '\n\tstructs={\n'
        for config in config['structs']:
            if isinstance(config['value'][0], int):
                _code = (configs_code(config, structs_keys, False))
            else:
                _code = (configs_code(config, structs_keys, False))
                _code = _code.rstrip('}') + '{\n'

                for item in config['value']:
                    _code += '\t\t\t' + (configs_code(item, structs_value_keys, False)) + ', \n'
                _code = _code.rstrip(', \n') + '}'
            code += '\t\t' + _code + ',\n'
    code = code.rstrip(',\n') + '\n\t}'
    code += '\n}'
    return code



def config_change(config):
    with open('test.txt', 'w+') as file:
        pprint.pprint(config, width=200, stream=file)

    with open('test.txt', 'r') as file:
        data = "".join(file.readlines())

    data = data.replace("'", '"') \
        .replace(':', '=') \
        .replace('[', '{') \
        .replace(']', '}') \
        .replace('None', 'nil')

    data = re.sub(r'(")([\w]+)("=)', r'\2=', data)

    return data

if __name__ == '__main__':
    configs = [{'length': 1, 'name': 'fan1', 'title': '大风'},
               {'length': 2, 'name': 'fan2', 'title': '大风'},
               {'length': 3, 'name': 'fan3', 'title': '大风'}]

    config = {
        'endian_type': 0,
        'length': 9,
        'length_offset': None,
        'check_type': 'crc16',
        'check_data_start': 0,
        'check_data_end': -2,
        'structs': [
            {'name': 'head', 'length': 1, 'value': [0x11, 0xA5, 0x5A, 0x01]},
            {'name': "version", 'length': 1, 'value': [0x01]},
            {'name': "category", 'length': 1, 'value': [0x01]},
            {'name': 'data', 'length': 4, 'value': [
                {'length': 1, 'name': 'fan1', 'title': '大风'},
                {'length': 12, 'name': 'test_fan', 'title': '大风风'},
                {'length': 12, 'name': 'test_fan', 'title': '大风风'},
                {'length': 12, 'name': 'test_fan', 'title': '大风风'},
                {'length': 12, 'name': 'test_fan', 'title': '大风风'}
            ]},
            {'name': 'check', 'length': 2, 'value': [{'length': 1, 'name': 'fan2', 'title': '小风'}]}
        ]
    }

    data = config_change(configs)
    # result = test_change(data)
    print(data)
