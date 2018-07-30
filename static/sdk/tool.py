# coding=utf-8

import zipfile
import os
import re
from pathlib import Path
import shutil


def unzip(project_name):
    project_path = os.path.join(os.getcwd(), project_name)
    if os.path.isdir(project_path):
        return
    else:
        project_file_path = project_path + '.zip'

        with zipfile.ZipFile(project_file_path, 'r') as file:
            for item in file.namelist():
                extracted_path = Path(file.extract(item))
                extracted_path.rename(item.encode('cp437').decode('gbk'))
        del_output(project_name)


def del_output(project_name):
    output_path = os.path.join(os.getcwd(), project_name, 'output')
    if os.path.isdir(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)


def get_personal_project(project_name: str, new_key: str) -> str:
    """根据原始的项目文件生成自定义用户key的用户项目，生成过程中
    在解压后的项目文件夹中替换main.lua中的key，替换后删除output文件夹下所有文件，并压缩成zip文件

    :param project_name: 项目文件夹压缩包的名字（WiFiIot）
    :param new_key: 用户的 key （keyqwerty）
    :return: 以 (项目名_用户的key.zip) 形式的压缩包名 （WiFiIot_keyqwerty.zip）
    """

    unzip(project_name)

    project_path = os.getcwd()
    personal_path = os.path.join(project_path, project_name + '_' + new_key + '.zip')
    main_lua_path = os.path.join(project_path, project_name, 'main.lua')
    lines = []
    with open(main_lua_path, encoding='utf-8') as file:
        for item in file.readlines():
            item = re.sub('(?<=^local product_key=["|\'])(\w+)(?=["|\']$)', new_key, item)
            lines.append(item)
    file.close()
    with open(main_lua_path, 'w+', encoding='utf-8') as file:
        for line in lines:
            file.write(line)
    file.close()
    del lines

    zip_file = zipfile.ZipFile(personal_path, 'w', zipfile.ZIP_DEFLATED)
    for folder, subfolder, file in os.walk(os.path.join(project_path, project_name)):
        for item in file:
            file_path = os.path.join(folder, item)
            file_name = file_path.replace(project_path, '')
            zip_file.write(file_path, file_name)
        if len(file) == 0:
            file_path = folder.replace(project_path, '')
            zip_file.write(folder, file_path)

    zip_file.close()
    return os.path.join(project_name + '_' + new_key + '.zip')


if __name__ == '__main__':
    """使用说明
    main.lua 使用utf-8编码进行存储
    更新项目时 删除 WiFiIot.zip 以及 WiFiIot文件夹 
    以 项目名_key 形式存放的文件属于临时文件可以进行删除
    ls WiFiIot_*zip
    rm WiFiIot_*zip
    """
    my_project_name = get_personal_project('WiFiIot', 'keyqwerty')
    print(my_project_name)
    # WiFiIot_keyqwerty.zip
