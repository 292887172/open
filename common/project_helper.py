# coding=utf-8
import zipfile
import os
import re
import shutil
import logging
import pprint

logging.basicConfig(level=logging.INFO)


def del_output(project_path):
    """
    在解压后的项目中删除output文件夹下所有文件
    :param project_path: 项目绝对路径
    """
    output_path = os.path.join(os.path.splitext(project_path)[0], 'output')
    if os.path.isdir(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)


def unzip_project(project_path):
    """ 解压项目文件，并删除解压后文件夹下 output 文件夹

    存在解压文件夹后直接返回，项目在更新时，在替换项目原始文件后，也要删除对应的解压后的文件夹

    :param project_path: 压缩文件的绝对路径
    """

    if os.path.isdir(os.path.splitext(project_path)[0]):
        return
    else:
        extract_path = os.path.splitext(project_path)[0]
        extract_path = os.path.split(extract_path)[0]
        with zipfile.ZipFile(project_path, 'r') as file:
            for item in file.namelist():
                file.extract(item, extract_path)
                old_name = os.path.join(extract_path, item)
                # 中文字符编码转换
                new_name = old_name.encode('cp437').decode('gbk')
                os.rename(old_name, new_name)
        del_output(project_path)


def zip_project(folder_path, new_name):
    """ 压缩文件夹成 zip压缩包

    :param folder_path: 待压缩的文件夹
    :param new_name: 文件夹压缩后的名字
    """
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


def replace_config(data: str, config_name: str, new_config: str) -> str or 'false':
    """
    基于指定格式的进行正则表达式替换，

    替换 [-- start xxx config] [...old...] [--end xxx config] 成 [...new...]

    :param data: 需要替换的字符串
    :param config_name: 需要替换的配置名
    :param new_config: 新的配置
    :return: 成功-> 替换皮质后的data ，  失败 -> 原始的data
    """
    rule = "(-- start {0} config)([\s\S]+)(-- end {0} config)".format(config_name)
    logging.info('匹配规则 ' + rule)
    # logging.info(re.search(rule, data, re.M).groups())
    try:
        data = re.sub(rule, new_config, data, re.M)
    except Exception as e:
        logging.error('替换出现错误 ' + str(e))
    finally:
        return data


def config_change(config: dict):
    """ 将 python 的 dict 转换成 lua 的 table
    替换规则
        :           =       \n
        [           {       \n
        ]           }       \n
        "None"      nil     \n
        "item"=     item    \n
        "{1}"       [1]     \n

    :param config: 需要转换的数据
    :return: 转换成功 -> 转换后的数据，转换失败 -> false
    """
    with open('tmp_change.txt', 'w+') as file:
        pprint.pprint(config, indent=4, width=200, stream=file)

    with open('tmp_change.txt', 'r') as file:
        data = "".join(file.readlines())

    data = data.replace("'", '"') \
        .replace(':', '=') \
        .replace('[', '{') \
        .replace(']', '}') \
        .replace('"None"', 'nil')
    data = re.sub(r'(")([\w]+)("=)', r'\2=', data)
    data = re.sub(r'("{)(\d)(}")', r'[\2]', data)

    data = re.sub(r"^{", "{\n ", data)
    data = re.sub(r"}$", "\n}", data)

    if change_validation(data):
        return data
    else:
        return False


def change_validation(config: str) -> bool:
    """ 验证dict->lua table转换后数据的正确性

    使用转换后的的内容生成 一个 test.lua 内容为  local item=config
    在lua5.1环境中进行测试，能返回指定结果代表转换后正确

    :param config:转换后的配置文件
    :return: true 转换成功，false 转换失败
    """
    with open('test.lua', 'w+') as file:
        file.write("local item=" + config + '\nprint(type(item))')
    if os.popen('lua test.lua').read() == 'table\n':
        return True
    else:
        return False


def get_personal_project(project_path: str,
                         key: str,
                         device_function: dict,
                         device_protocol_config: dict or 'false' = False,
                         device_protocol_response_config: dict or 'false' = False,
                         return_type: 'zip or lua' = 'zip'):
    """
    根据自定义配置生成自定义的项目包

    :param project_path: 项目原始文件的路径 必须
    :param key: 自定义的key 必须
    :param device_function: 自定义的设备功能列表 必须
    :param device_protocol_config: 自定义的上行帧格式 可选
    :param device_protocol_response_config: 自定义的应答帧格式  可选
    :param return_type: 最终获取的 文件类型  'zip'->project.zip  'lua'->main.lua 默认 'zip'
    :return: 自定义转换成功 -> 返回绝对路径下载地址  ， 自定义转换失败 -> 原始绝对路径下载地址
    """

    def _replace(main_key_lua):
        with open(main_key_lua, encoding='utf-8') as file:
            data = "".join(file.readlines())

        configs = {
            "product_key": 'local product_key="{0}"'.format(key),
            "device_function": 'local device_function={0}'.format(config_change(device_function)),
        }

        if device_protocol_config:
            configs["device_protocol_config"] = 'local device_protocol_config={0}'.format(
                config_change(device_protocol_config))
        else:
            configs["device_protocol_config"] = 'local device_protocol_config'

        if device_protocol_response_config:
            configs["device_protocol_response_config"] = 'local device_protocol_response_config={0}'.format(
                config_change(device_protocol_response_config))
        else:
            configs["device_protocol_response_config"] = 'local device_protocol_response_config'

        try:
            for config in configs:
                data = replace_config(data, config, configs[config])
        except Exception as e:
            logging.error('替换失败 ' + str(e))

        with open(main_key_lua, 'w+', encoding='utf-8') as file:
            file.write(data)

    # project_path '/home/am/deployment/open/static/sdk/WiFiIot.zip'
    project_name = os.path.splitext(os.path.basename(project_path))[0]  # 'WiFiIot'
    project_location = os.path.split(project_path)[0]  # '/home/am/deployment/open/static/sdk'
    project_folder = os.path.splitext(project_path)[0]  # '/home/am/deployment/open/static/sdk/WiFiIot'
    main_lua = os.path.join(project_folder, 'main.lua')  # '/home/am/deployment/open/static/sdk/WiFiIot/main.lua'
    main_origin_lua = os.path.join(project_folder, 'main.origin.lua')
    # '/home/am/deployment/open/static/sdk/WiFiIot/main.origin.lua'

    personal_zip_name = project_name + '_' + key + '.zip'  # 'WiFiIot_dnZj13MV.zip'
    personal_main_name = 'main_' + key + '.lua'  # 'main_dnZj13MV.lua'

    if not project_path:
        logging.error('没有 project_path')
        return False
    if not key:
        logging.error('没有 key')
        return False
    if not device_function:
        logging.error('没有 device_function')
        return False
    if not return_type:
        logging.error('没有 return_type')
        return False

    try:
        unzip_project(project_path)
    except Exception as e:
        logging.error('解压失败 错误内容 ' + str(e))

    if not os.path.isfile(main_origin_lua):
        shutil.copy(main_lua, main_origin_lua)

    project_key_zip = os.path.join(project_location, personal_zip_name)
    main_key_lua = os.path.join(project_location, personal_main_name)

    shutil.copy(main_origin_lua, main_key_lua)

    _replace(main_key_lua)

    if return_type == 'zip':
        try:
            shutil.copy(main_key_lua, main_lua)
            zip_project(project_folder, personal_zip_name)
            logging.info('最终返回的自定义项目下载文件路径 ' + project_key_zip)
            return project_key_zip
        except Exception as e:
            logging.error('压缩失败 ' + str(e))
            logging.info('最终返回的下载文件路径 ' + project_path)
            return project_path

    elif return_type == 'lua':
        if os.path.exists(main_key_lua):
            logging.info('最终返回的自定义文件下载文件路径 ' + main_key_lua)
        else:
            shutil.copy(main_origin_lua, main_key_lua)
            logging.info('最终返回的下载文件路径 ' + main_key_lua)
        return main_key_lua


def test_os():
    project_path = os.path.join(os.getcwd(), 'WiFiIot.zip')  # /home/am/deployment/open/static/sdk/WiFiIot.zip
    print(project_path)
    print(os.path.split(project_path))  # ('/home/am/deployment/open/static/sdk', 'WiFiIot.zip')
    print(os.path.splitext(project_path))  # ('/home/am/deployment/open/static/sdk/WiFiIot', '.zip')
    print(os.path.splitext('WiFiIot.zip'))  # ('WiFiIot', '.zip')
    print(os.path.basename(project_path))  # WiFiIot.zip
    print(os.path.split('/home/am/deployment/open/static/sdk'))  # ('/home/am/deployment/open/static', 'sdk')


def test_config_change(device_function, device_protocol_config):
    pprint.pprint(config_change(device_function))
    pprint.pprint(config_change(device_protocol_config))


def test_get_personal_project(device_function, device_protocol_config):
    key = 'AABBCCDD'
    project_path = '/home/am/deployment/open/static/sdk/WiFiIot.zip'
    device_protocol_response_config = False

    logging.info(get_personal_project(project_path, key, device_function,
                                      device_protocol_config, device_protocol_response_config, 'lua'))


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

    device_function = [
        {'length': 8, 'name': 'BaoLiu1', 'title': '保留1'},
        {'length': 8, 'name': 'BaoLiu2', 'title': '保留2'},
        {'length': 4, 'name': 'BaoLiu3', 'title': '保留3'},
        {'length': 1, 'name': 'FengMing', 'title': '蜂鸣'},
        {'length': 1, 'name': 'XiaoDu', 'title': '消毒'},
        {'length': 1, 'name': 'HongGan', 'title': '烘干'},
        {'length': 1, 'name': 'AUX', 'title': 'AUX'},
        {'length': 1, 'name': 'Fan3', 'title': '快档'},
        {'length': 1, 'name': 'Fan2', 'title': '中档'},
        {'length': 1, 'name': 'Fan1', 'title': '慢档'},
        {'length': 1, 'name': 'Wash', 'title': '清洗'},
        {'controls': [101, 102], 'length': 1, 'name': 'lamp', 'title': '照明',
         'triggers': {
             '[0]': {'jiang': 0, 'shen': 1},
             '[1]': {'jiang': 1, 'shen': 0}}},
        {'length': 1, 'name': 'jiang', 'title': '降'},
        {'length': 1, 'name': 'shen', 'title': '升'},
        {'length': 1, 'name': 'LAMP1', 'title': 'LAMP'}
    ]

    device_protocol_config = {
        'check_data_end': -2,
        'check_data_start': 1,
        'check_type': 'crc16',
        'endian_type': 1,
        'length': 9,
        'length_offset': 'None',
        'structs': [
            {'length': 1, 'name': 'head', 'value': [165]},
            {'length': 2, 'name': 'category', 'value': [0, 1]},
            {'length': 4, 'name': 'data'},
            {'length': 2, 'name': 'check'}
        ]}

    test_get_personal_project()
