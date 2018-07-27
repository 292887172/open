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


def get_personal_project(project_name, new_key):
    """
    :param project_name: 项目文件夹的名字
    :param new_key: 用户的 key
    :return: 以 (项目名_用户的key.zip) 形式的压缩包
    """
    # 项目文件夹的路径，（项目以文件夹形式存放，方便后续生成指定压缩包）此py文件与项目文件放在同一目录下

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


if __name__ == '__main__':
    """备注
    main.lua 使用utf-8编码进行存放
    """
    get_personal_project('WiFiIot', 'keyqwerty')
    # del_output('WiFiIot')
