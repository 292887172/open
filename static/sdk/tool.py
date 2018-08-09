# coding=utf-8

import zipfile
import os
import re
from pathlib import Path
import shutil
import logging
import pprint
from collections import OrderedDict


def del_output(project_path):
    output_path = os.path.join(os.path.splitext(project_path)[0], 'output')
    if os.path.isdir(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)


def unzip_project(project_path):
    # project_path = os.path.join(os.getcwd(), project_name)
    if os.path.isdir(os.path.splitext(project_path)[0]):
        return
    else:
        with zipfile.ZipFile(project_path, 'r') as file:
            for item in file.namelist():
                extracted_path = Path(file.extract(item))
                extracted_path.rename(item.encode('cp437').decode('gbk'))
        del_output(project_path)


def zip_project(folder_path, new_name):
    base_path = os.path.split(folder_path)[0]
    zip_file = zipfile.ZipFile(os.path.join(base_path, new_name) + '.zip', 'w', zipfile.ZIP_DEFLATED)
    for folder, subfolder, file in os.walk(folder_path):
        for item in file:
            file_path = os.path.join(folder, item)
            file_name = file_path.replace(base_path, '')
            zip_file.write(file_path, file_name)
        if len(file) == 0:
            file_path = folder.replace(base_path, '')
            zip_file.write(folder, file_path)
    zip_file.close()


def replace_config(data: str, config_name: str, new_config: str) -> str:
    rule = "(-- start {0} config)([\s\S]+)(-- end {0} config)".format(config_name)
    # print(re.search(rule, data, re.M).groups())  # test 输出匹配到的数据
    try:
        data = re.sub(rule, new_config, data, re.M)
        return data
    except Exception as e:
        logging.error(str(e))
        return '替换错误'


def get_personal_project(project_name, key, device_function, device_protocol_config):
    """根据原始的项目文件生成自定义用户key的用户项目，生成过程中
    在解压后的项目文件夹中替换main.lua中的key，替换后删除output文件夹下所有文件，并压缩成zip文件

    :param project_name: 项目文件夹压缩包的名字（WiFiIot）
    :param new_key: 用户的 key （keyqwerty）
    :return: 以 (项目名_用户的key.zip) 形式的压缩包名 （WiFiIot_keyqwerty.zip）
    """

    project_path = os.path.join(os.getcwd(), project_name) + '.zip'

    unzip_project(project_path)

    personal_name = project_name + '_' + key + '.zip'
    project_folder = os.path.splitext(project_path)[0]
    main_lua = os.path.join(project_folder, 'main.lua')
    main_origin_lua = os.path.join(project_folder, 'main.origin.lua')

    if not os.path.isfile(main_origin_lua):
        shutil.copy(main_lua, main_origin_lua)

    with open(main_origin_lua, encoding='utf-8') as file:
        data = "".join(file.readlines())

    configs = {
        "product_key": 'local product_key="{0}"'.format(key),
        "device_function": 'local device_function={0}'.format(config_change(device_function)),
        "device_protocol_config": 'local device_protocol_config={0}'.format(config_change(device_protocol_config))
    }

    for config in configs:
        data = replace_config(data, config, configs[config])

    with open(main_lua, 'w+', encoding='utf-8') as file:
        file.write(data)

    zip_project(project_folder, personal_name)

    return os.path.join(os.getcwd(), personal_name)


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

    if change_test(data):
        return data
    else:
        return False


def change_test(config):
    with open('test.lua', 'w+') as file:
        file.write("local item=" + config + '\nprint(type(item))')
    if os.popen('lua test.lua').read() == 'table\n':
        return True
    else:
        return False


if __name__ == '__main__':
    """使用说明
    main.lua 使用utf-8编码进行存储
    更新项目时 删除 WiFiIot.zip 以及 WiFiIot文件夹 
    以 项目名_key 形式存放的文件属于临时文件可以进行删除
    ls WiFiIot_*zip
    rm WiFiIot_*zip
    """

    # print(os.path.join(os.getcwd(), 'WiFiIot.zip'))  # /home/am/deployment/open/static/sdk/WiFiIot.zip
    # print(os.path.split(project_path))  # ('/home/am/deployment/open/static/sdk', 'WiFiIot.zip')
    # print(os.path.splitext(project_path))  # ('/home/am/deployment/open/static/sdk/WiFiIot', '.zip')
    # print(os.path.basename(project_path))  # WiFiIot.zip
    # print(os.path.split('/home/am/deployment/open/static/sdk'))  # ('/home/am/deployment/open/static', 'sdk')

    device_function = [{'length': 1, 'name': 'fan1', 'title': '大风'},
                       {'length': 2, 'name': 'fan2', 'title': '大风'},
                       {'length': 3, 'name': 'fan3', 'title': '大风'}]

    device_protocol_config = {
        'endian_type': 0,
        'length': 9,
        'length_offset': "None",
        'check_type': 'crc16',
        'check_data_start': 0,
        'check_data_end': -2,
        'structs': [
            {'name': 'head', 'length': 1, 'value': [0x11, 0xA5, 0x5A, 0x01]},
            {'name': "version", 'length': 1, 'value': [0x01]},
            {'name': "category", 'length': 1, 'value': [0x01]},
            {'name': 'data', 'length': 4, 'value': [
                {'length': 1, 'name': 'fan1', 'title': '大风'},
                {'length': 2, 'name': 'test_fan', 'title': '大风风'},
                {'length': 3, 'name': 'test_fan', 'title': '大风风'},
                {'length': 4, 'name': 'test_fan', 'title': '大风风'},
                {'length': 5, 'name': 'test_fan', 'title': '大风风'}
            ]},
            {'name': 'check', 'length': 2, 'value': [{'length': 1, 'name': 'fan2', 'title': '小风'}]}
        ]
    }

    # print(config_change(device_function))
    # print(config_change(device_protocol_config))

    result = get_personal_project('WiFiIot', 'new_key_123', device_function, device_protocol_config)
    print(result)
