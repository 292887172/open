# coding=utf-8
import zipfile
import os
import re
import shutil
import logging
import pprint

from common.config_helper import get_device_function
from common.config_helper import get_device_protocol_config
from common.config_helper import get_init_config_code
from common.config_helper import get_device_config_virsion

from common.config_helper_old import get_device_function as get_device_function_old
from common.config_helper_old import get_device_protocol_config as get_device_protocol_config_old
from common.project_help_old import get_personal_project as get_personal_project_old

logging.basicConfig(level=logging.INFO)


def del_output_and_dciot_build(project_path: str):
    """ 大彩IDE在编译打包时生成的文件\n
    在解压后的项目中删除output,dciot_build文件夹下所有文件\n
    :param project_path: 项目绝对路径 /home/am/deployment/open/static/sdk/WiFiIot.zip
    """
    output_path = os.path.join(os.path.splitext(project_path)[0], 'output')
    dciot_build_path = os.path.join(os.path.splitext(project_path)[0], 'dciot_build')

    if os.path.isdir(output_path):
        shutil.rmtree(output_path)
        os.makedirs(output_path)
    if os.path.isdir(dciot_build_path):
        shutil.rmtree(dciot_build_path)
        os.makedirs(dciot_build_path)


def unzip_project(project_path: str) -> None:
    """ 解压项目文件\n
    存在解压文件夹后直接返回\n
    项目在更新时，在替换项目原始文件后，也要删除对应的解压后的文件夹\n
    :param project_path: 压缩文件的绝对路径 /home/am/deployment/open/static/sdk/WiFiIot.zip
    """
    if os.path.isdir(os.path.splitext(project_path)[0]):
        return
    else:
        extract_path = os.path.split(project_path)[0]
        with zipfile.ZipFile(project_path, 'r') as file:
            for item in file.namelist():
                file.extract(item, extract_path)
                old_name = os.path.join(extract_path, item)
                new_name = old_name.encode('cp437').decode('gbk')  # 中文字符编码转换
                os.rename(old_name, new_name)
        del_output_and_dciot_build(project_path)


def zip_project(folder_path: str, new_name: str, main_key_lua: str) -> None:
    """ 压缩文件夹成 project_{key}.zip 形式的压缩包\n
    :param folder_path: 待压缩的文件夹  /home/am/deployment/open/static/sdk/WiFiIot
    :param new_name: 文件夹压缩后的名字  WiFiIot_dnZj13MV.zip
    :param main_key_lua: 替换配置之后的main.lua文件绝对路径 /home/am/deployment/open/static/sdk/main_dnZj13MV.lua
    """
    base_path = os.path.split(folder_path)[0]  # /home/am/deployment/open/static/sdk
    zip_file = zipfile.ZipFile(os.path.join(base_path, new_name), 'w', zipfile.ZIP_DEFLATED)
    for folder, subfolder, file in os.walk(folder_path):
        for item in file:
            file_path = os.path.join(folder, item)  # /home/am/deployment/open/static/sdk/WiFiIot/main.lua
            file_name = file_path.replace(base_path, '')  # /WiFiIot/main.lua
            if os.path.basename(file_name) == 'main.lua':
                zip_file.write(main_key_lua, file_name)
            else:
                zip_file.write(file_path, file_name)
        if len(file) == 0:  # 文件夹下没有文件情况下将文件夹添加进压缩包
            file_path = folder.replace(base_path, '')  # /WiFiIot/Waves
            zip_file.write(folder, file_path)
    zip_file.close()


def replace_config(data: str, config_name: str, new_config: str) -> str or bool(False):
    """ 基于指定格式的进行正则表达式替换\n
    替换 [-- start xxx config] [...old...] [--end xxx config] 成 [...new...]\n
    :param data: 需要替换的字符串
    :param config_name: 需要替换的配置名
    :param new_config: 新的配置
    :return: True:替换皮质后的data ，  False:原始的data
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


def change_config(config: list) -> str or bool(False):
    """ 将 python 的 dict 转换成 lua 的 table\n
    :param config: 需要转换的数据
    :return: True:转换后的数据，False:转换失败
    """
    data = pprint.pformat(config, indent=4, width=150)

    data = data.replace("'", '"')  # '  "
    data = data.replace(':', '=')  # :  =
    data = data.replace('[', '{')  # [  {
    data = data.replace(']', '}')  # ]  }
    data = data.replace('"None"', 'nil')  # "None"  nil
    data = re.sub(r'(\")(\w+=)(\",)', r'\2', data)  # "main="  main=
    data = re.sub(r'(")([\w]+)("=)', r'\2=', data)  # "item"=  item
    data = re.sub(r'(\")(\w+=\d+)(\")', r'\2', data)  # "main=51"  main=51
    data = re.sub(r'("{)(\d)(}")', r'[\2]', data)  # "{1}"  [1]
    data = re.sub(r"^{", "{\n ", data)  # 第一个{替换成{\n
    data = re.sub(r"}$", "\n}", data)  # 最后一个{替换成\n}

    # 代码部分美化
    data = data.replace('    ', '\t')
    data = data.replace(' ', '')
    data = data.replace('\t', '    ')
    data = re.sub(r'(=)(\n\s+)', r'=', data)

    if validation_config(data):
        return data
    else:
        return False


def validation_config(config: str) -> bool:
    """ 验证python dict->lua table转换后数据的正确性\n
    使用转换后的的内容生成 一个 test.lua 内容为  local item=config\n
    在lua5.1环境中进行测试，能返回指定结果代表转换后正确\n
    :param config:转换后的配置文件
    :return: True:转换成功，False:转换失败
    """
    with open('test.lua', 'w+') as file:
        file.write("local item=" + config + '\nprint(type(item))')
    return os.popen('lua test.lua').read() == 'table\n'


def get_personal_project(project_path: str,
                         key: str,
                         device_function: dict,
                         device_protocol_config: dict or bool(False),
                         device_protocol_response_config: dict or bool(False),
                         return_type: 'zip or lua' = 'zip') -> str:
    """
    根据自定义配置生成自定义的项目包

    :param project_path: 项目原始文件的路径 必须
    :param key: 自定义的key 必须
    :param device_function: 自定义的设备功能列表 必须
    :param device_protocol_config: 自定义的上行帧格式 可选
    :param device_protocol_response_config: 自定义的应答帧格式  可选
    :param return_type: 最终获取的 文件类型  'zip'->project.zip  'lua'->main.lua 默认 'zip'
    :return: 自定义转换成功:返回绝对路径下载地址  ， 自定义转换失败:原始绝对路径下载地址
    """

    def _replace_config(main_key_lua):
        with open(main_key_lua, encoding='utf-8') as file:
            data = "".join(file.readlines())

        configs = {
            "product_key": 'local product_key="{0}"'.format(key),
            "device_function": 'local device_function={0}'.format(change_config(device_function))
        }

        init_code = get_init_config_code(device_function)

        if init_code:
            configs['init'] = init_code

        if device_protocol_config:
            configs["device_protocol_config"] = 'local device_protocol_config={0}'.format(
                change_config(device_protocol_config))
        else:
            configs["device_protocol_config"] = 'local device_protocol_config'

        if device_protocol_response_config:
            configs["device_protocol_response_config"] = 'local device_protocol_response_config={0}'.format(
                change_config(device_protocol_response_config))
        else:
            configs["device_protocol_response_config"] = 'local device_protocol_response_config'

        for config in configs:
            data = replace_config(data, config, configs[config])

        with open(main_key_lua, 'w+', encoding='utf-8') as file:
            file.write(data)

    # project_path '/home/am/deployment/open/static/sdk/WiFiIot.zip'
    project_name = os.path.splitext(os.path.basename(project_path))[0]  # 'WiFiIot'
    project_location = os.path.split(project_path)[0]  # '/home/am/deployment/open/static/sdk'
    project_folder = os.path.splitext(project_path)[0]  # '/home/am/deployment/open/static/sdk/WiFiIot'
    main_lua = os.path.join(project_folder, 'main.lua')  # '/home/am/deployment/open/static/sdk/WiFiIot/main.lua'
    main_origin_lua = os.path.join(project_folder, 'main.origin.lua')
    # '/home/am/deployment/open/static/sdk/WiFiIot/main.origin.lua'

    personal_zip_name = '{project_name}_{key}.zip'.format(project_name=project_name, key=key)  # 'WiFiIot_dnZj13MV.zip'
    personal_main_name = 'main_{key}.lua'.format(key=key)  # 'main_dnZj13MV.lua'

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
    # '/home/am/deployment/open/static/sdk/WiFiIot_dnZj13MV.zip'

    main_key_lua = os.path.join(project_location, personal_main_name)
    # '/home/am/deployment/open/static/sdk/main_dnZj13MV.lua'

    shutil.copy(main_origin_lua, main_key_lua)

    _replace_config(main_key_lua)

    if return_type == 'zip':
        try:
            zip_project(project_folder, personal_zip_name, main_key_lua)
            logging.info('最终返回的自定义项目下载文件路径 ' + project_key_zip)
            return project_key_zip
        except Exception as e:
            logging.error('压缩失败 ' + str(e))
            logging.info('最终返回的下载文件路径 ' + project_path)
            return project_path

    elif return_type == 'lua':
        if os.path.exists(main_key_lua):
            logging.info('最终返回的自定义文件下载文件路径 ' + main_key_lua)
            return main_key_lua
        else:
            logging.info('最终返回的下载文件路径 ' + main_lua)
            return main_lua


def get_personal_project_by_key(project_path, key, return_type):
    """ 通过 项目绝对路径, key, 返回类型 生成自定义项目\n
    兼容旧版功能定义，

    :param project_path: 使用项目的绝对路径  /home/am/deployment/open/static/sdk/WiFiIot.zip
    :param key: 用户的 key  MCKjIJWI
    :param return_type: 需要生成的类型  zip
    :return: 生成后的文件的绝对路径
    """

    version = get_device_config_virsion(key)
    if version == 0:
        device_function = get_device_function_old(key)
        device_protocol_config, device_protocol_response_config = get_device_protocol_config_old(key)
        location_path = get_personal_project_old(project_path, key,
                                                 device_function,
                                                 device_protocol_config,
                                                 device_protocol_response_config,
                                                 return_type)
    else:
        device_function = get_device_function(key)
        device_protocol_config, device_protocol_response_config = get_device_protocol_config(key)

        location_path = get_personal_project(project_path, key,
                                             device_function,
                                             device_protocol_config,
                                             device_protocol_response_config,
                                             return_type)
    return location_path


###############################################################################################

def test_os():
    project_path = os.path.join(os.getcwd(), 'WiFiIot.zip')
    print(project_path)  # /home/am/deployment/open/static/sdk/WiFiIot.zip
    print(os.path.split(project_path))  # ('/home/am/deployment/open/static/sdk', 'WiFiIot.zip')
    print(os.path.splitext(project_path))  # ('/home/am/deployment/open/static/sdk/WiFiIot', '.zip')
    print(os.path.splitext('WiFiIot.zip'))  # ('WiFiIot', '.zip')
    print(os.path.basename(project_path))  # WiFiIot.zip
    print(os.path.split('/home/am/deployment/open/static/sdk'))  # ('/home/am/deployment/open/static', 'sdk')


def test_zip():
    unzip_project('/home/am/deployment/open/static/sdk/WiFiIot.zip')

    zip_project('/home/am/deployment/open/static/sdk/WiFiIot', 'WiFiIot_dnZj13MV.zip',
                '/home/am/deployment/open/static/sdk/main_dnZj13MV.lua')


def test_config_change():
    device_function = get_device_function('fnXNO5Kj')
    device_protocol_config = get_device_protocol_config('fnXNO5Kj')

    print(change_config(device_function))
    if device_protocol_config:
        print(change_config(device_protocol_config))


def test_get_personal_project():
    key = 'fnXNO5Kj'

    project_path = '/home/am/deployment/open/static/sdk/WiFiIot.zip'
    device_function = get_device_function(key)
    device_protocol_config, device_protocol_response_config = get_device_protocol_config(key)

    pprint.pprint(device_function)

    print(get_personal_project(project_path, key, device_function, device_protocol_config,
                               device_protocol_response_config, 'zip'))


def test_get_personal_project_old():
    key = 'fnXNO5Kj'

    project_path = '/home/am/deployment/open/static/sdk/WiFiIot.zip'
    device_function = get_device_function_old(key)
    device_protocol_config, device_protocol_response_config = get_device_protocol_config_old(key)

    pprint.pprint(device_function)

    print(get_personal_project_old(project_path, key, device_function, device_protocol_config,
                                   device_protocol_response_config, 'zip'))


if __name__ == '__main__':
    pass
    """使用说明
    
    - 初始准备，在此方法的同目录下放置项目文件其中
        - 格式 zip
        - main.lua 中需要替换的内容使用   -- start xxx config    -- end xxx config 包裹
    - 解压生成
        - 项目默认解压在同目录下
        - 解压后 拷贝 main.lua 为 main.origin.lua
        - 生成的文件 main.lua 中的配置会替换，main.origin.lua 也会打包进项目中
    - 打包
        - 打包后文件名 prject_name + '_' + new_key.zip 
    - 调用
         get_personal_project(project_path: str,
                         key: str,
                         device_function: dict,
                         device_protocol_config: dict or bool(False),
                         device_protocol_response_config: dict or bool(False),
                         return_type: 'zip or lua' = 'zip')
         get_personal_project_by_key(project_path, key, return_type)      
    - 其他
        - main.lua 使用utf-8编码进行存储
        - 更新原始项目包时 删除 WiFiIot.zip 以及 WiFiIot文件夹 
        - 以 项目名_key 形式存放的文件属于临时文件可以进行删除
            - ls WiFiIot_*zip
            - rm WiFiIot_*zip
        - 格式转换基于文本的替换，并且转换后的数据会使用 lua5.1 模拟运行
    """

    # test_get_personal_project()
    # test_get_personal_project_old()
