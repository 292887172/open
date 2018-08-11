# coding=utf-8

import zipfile
import os
import re
from pathlib import Path
import shutil
import logging
import pprint
from collections import OrderedDict
import re
import json


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

    if test_change(data):
        return data
    else:
        return False


def test_change(config):
    with open('test.lua', 'w+') as file:
        file.write("local item=" + config + '\nprint(type(item))')
    if os.popen('lua test.lua').read() == 'table\n':
        return True
    else:
        return False


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
