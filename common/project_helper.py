# coding=utf-8
import zipfile
import os
import re
from pathlib import Path
import shutil
import logging
import pprint

logging.basicConfig(level=logging.INFO)


def del_output(project_path):
    output_path = os.path.join(os.path.splitext(project_path)[0], 'output')
    if os.path.isdir(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)


def unzip_project(project_path):
    if os.path.isdir(os.path.splitext(project_path)[0]):
        return
    else:
        extract_path = os.path.splitext(project_path)[0]
        extract_path = os.path.split(extract_path)[0]
        with zipfile.ZipFile(project_path, 'r') as file:
            for item in file.namelist():
                file.extract(item, extract_path)
                old_name = os.path.join(extract_path, item)
                new_name = old_name.encode('cp437').decode('gbk')
                os.rename(old_name, new_name)
        del_output(project_path)


def zip_project(folder_path, new_name):
    base_path = os.path.split(folder_path)[0]
    zip_file = zipfile.ZipFile(os.path.join(base_path, new_name), 'w', zipfile.ZIP_DEFLATED)
    for folder, subfolder, file in os.walk(folder_path):
        for item in file:
            file_path = os.path.join(folder, item)
            file_name = file_path.replace(base_path, '')
            zip_file.write(file_path, file_name)
        if len(file) == 0:
            file_path = folder.replace(base_path, '')
            zip_file.write(folder, file_path)
    zip_file.close()


def replace_config(data: str, config_name: str, new_config: str) -> 'str or false':
    rule = "(-- start {0} config)([\s\S]+)(-- end {0} config)".format(config_name)
    logging.info('匹配规则 ' + rule)
    # logging.info('匹配到的数据 ', end='')
    # logging.info(re.search(rule, data, re.M).groups())
    try:
        data = re.sub(rule, new_config, data, re.M)
        return data
    except Exception as e:
        logging.error('格式转换出现错误 ' + str(e))
        return False


def get_personal_project(project_path, key, device_function, device_protocol_config):
    project_name = os.path.splitext(os.path.basename(project_path))[0]
    try:
        unzip_project(project_path)
    except Exception as e:
        logging.error('解压失败 返回原始文件 错误内容 ' + str(e))
        return project_path

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

    try:
        for config in configs:
            data = replace_config(data, config, configs[config])
        with open(main_lua, 'w+', encoding='utf-8') as file:
            file.write(data)
    except Exception as e:
        logging.error('替换失败 ' + str(e))

    try:
        zip_project(project_folder, personal_name)
    except Exception as e:
        logging.error('压缩失败 ' + str(e))
        return project_path

    personal_file_path = os.path.split(project_path)[0]
    personal_file_path = os.path.join(personal_file_path, personal_name)

    if os.path.exists(personal_file_path):
        logging.info('最终返回的下载文件路径1 ' + personal_file_path)
        return personal_file_path
    else:
        logging.info('最终返回的下载文件路径2 ' + project_path)
        return project_path


def config_change(config):
    with open('test.txt', 'w+') as file:
        pprint.pprint(config, width=200, stream=file)

    with open('test.txt', 'r') as file:
        data = "".join(file.readlines())

    data = data.replace("'", '"') \
        .replace(':', '=') \
        .replace('[', '{') \
        .replace(']', '}') \
        .replace('"None"', 'nil')

    data = re.sub(r'(")([\w]+)("=)', r'\2=', data)

    data = re.sub(r'("{)(\d)(}")', r'[\2]', data)

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
    
    - 初始准备，在此方法的同目录下放置项目文件其中
        - 格式 zip
        - main.lua 中需要替换的项使用   -- start xxx config    -- end xxx config 包裹，
    - 解压生成
        - 项目默认解压在同目录下
        - 解压后 拷贝 main.lua 为 main.origin.lua
        - 生成的文件 main.lua 中的配置会替换，main.origin.lua 也会打包进项目中
    - 打包
        - 打包后文件名 prject_name + '_' + new_key.zip 
        
    - 调用
        project_path = get_personal_project(project_name, key, device_function, device_protocol_config)
        
        project_name: 项目名  (例如 WiFiIot 代表同目录下 WiFiIot.zip)
        ket: 新的key  (str) 
        device_function:    dict
        device_protocol_config  dict    
    - 其他
        - main.lua 使用utf-8编码进行存储
        - 更新项目时 删除 WiFiIot.zip 以及 WiFiIot文件夹 
        - 以 项目名_key 形式存放的文件属于临时文件可以进行删除
            - ls WiFiIot_*zip
            - rm WiFiIot_*zip
        - 格式转换基于文本的替换，并且转换后的数据会使用 lua5.1 模拟运行
    """

    # print(os.path.join(os.getcwd(), 'WiFiIot.zip'))  # /home/am/deployment/open/static/sdk/WiFiIot.zip
    # print(os.path.split(project_path))  # ('/home/am/deployment/open/static/sdk', 'WiFiIot.zip')
    # print(os.path.splitext(project_path))  # ('/home/am/deployment/open/static/sdk/WiFiIot', '.zip')
    # print(os.path.splitext('WiFiIot.zip'))  # ('WiFiIot', '.zip')
    # print(os.path.basename(project_path))  # WiFiIot.zip
    # print(os.path.split('/home/am/deployment/open/static/sdk'))  # ('/home/am/deployment/open/static', 'sdk')

    # test config
    # device_function = [{'length': 1, 'name': 'fan1', 'title': '大风'},
    #                    {'length': 2, 'name': 'fan2', 'title': '大风'},
    #                    {'length': 3, 'name': 'fan3', 'title': '大风'}]
    #
    # device_protocol_config = {
    #     'endian_type': 0,
    #     'length': 9,
    #     'length_offset': "None",
    #     'check_type': 'crc16',
    #     'check_data_start': 0,
    #     'check_data_end': -2,
    #     'structs': [
    #         {'name': 'head', 'length': 1, 'value': [0x11, 0xA5, 0x5A, 0x01]},
    #         {'name': "version", 'length': 1, 'value': [0x01]},
    #         {'name': "category", 'length': 1, 'value': [0x01]},
    #         {'name': 'data', 'length': 4, 'value': [
    #             {'length': 1, 'name': 'fan1', 'title': '大风'},
    #             {'length': 2, 'name': 'test_fan', 'title': '大风风'},
    #             {'length': 3, 'name': 'test_fan', 'title': '大风风'},
    #             {'length': 4, 'name': 'test_fan', 'title': '大风风'},
    #             {'length': 5, 'name': 'test_fan', 'title': '大风风'}
    #         ]},
    #         {'name': 'check', 'length': 2, 'value': [{'length': 1, 'name': 'fan2', 'title': '小风'}]}
    #     ]
    # }

    # actual config
    device_function = [
        {'length': 1, 'name': 'Fan3', 'title': '大风',
         'controls': {'Main': 113}, 'triggers': {'[1]': {'Power': 1, 'Fan1': 0, 'Fan2': 0}}},
        {'length': 1, 'name': 'Fan2', 'title': '中风'},
        {'length': 1, 'name': 'Fan1', 'title': '小风'},
        {'length': 1, 'name': 'Wash', 'title': '清洗'},
        {'length': 1, 'name': 'Light', 'title': '清洗'},
        {'length': 1, 'name': 'Down', 'title': '降'},
        {'length': 1, 'name': 'Up', 'title': '升'},
        {'length': 1, 'name': 'Lamp', 'title': 'Lamp'},
        {'length': 1, 'name': 'Power', 'title': '电源',
         'value': 1, 'controls': {'Main': 101}},
        # 'value': 1, 'controls': {'Main': 101}, 'triggers': {'[0]': {'All': 0}, '[1]': {'Fan2': 1}}},
        {'length': 1, 'name': 'Fire', 'title': '火焰型号'},
        {'length': 1, 'name': 'LeftGas', 'title': '左灶'},
        {'length': 2, 'name': 'Beep', 'title': '蜂鸣'},
        {'length': 1, 'name': 'Dry', 'title': '烘干'},
        {'length': 1, 'name': 'Disinfectants', 'title': '消毒'},
        {'length': 1, 'name': 'Aux', 'title': 'Aux'},
        {'length': 8, 'name': 'Temp', 'title': '烟道温度'},
        {'length': 8, 'name': 'Fault', 'title': '故障报警'}
    ]

    device_protocol_config = {
        'endian_type': 0,
        'length': 9,
        'length_offset': "None",
        'check_type': 'crc16',
        'check_data_start': 0,
        'check_data_end': -2,
        'structs': [
            {'name': 'head', 'length': 1, 'value': [0xA5]},
            {'name': "version", 'length': 1, 'value': [0x01]},
            {'name': "category", 'length': 1, 'value': [0x01]},
            {'name': 'data', 'length': 4},
            {'name': 'check', 'length': 2}
        ]
    }

    logging.info(config_change(device_function))
    logging.info(config_change(device_protocol_config))

    key = 'AABBCCDD'
    project_path = '/home/am/deployment/open/static/sdk/WiFiIot.zip'
    logging.info('传入项目的路径 ' + project_path)
    logging.info(get_personal_project(project_path, key, device_function, device_protocol_config))
