# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import logging
import zipfile
from django.http import HttpResponse
from common.app_helper import update_app_fun_widget


from util.excelutil import write_data
from model.center.app import App


def write_excel(items, filename):
    headers = {'id': '功能序号', 'name': "产品功能", 'remarks': '备注', 'values': '值域', 'Stream_ID': '功能标识',
               'mxsLength': '长度(bit)', 'widget': '单位', 'permission': '权限', 'isFunction': '功能（属性）', 'toSwitch': '总开关'}
    items['functions'].insert(0, headers)
    header = ['id', 'name', 'remarks', 'values', 'Stream_ID', 'mxsLength', 'widget', 'permission', 'isFunction', 'toSwitch']
    excel_name = write_data(items, header, filename)
    return excel_name


def write_json(items, filename):
    filename += ".json"
    file = open(filename, 'w')
    data = json.dumps(items).encode('utf-8')
    data = data.decode('unicode-escape')
    file.write(data)
    file.close()
    return file.name


def write_zip(e_data, j_data, export_name):
    try:
        # 保存到本地文件
        z_name = export_name[0] + 'TRD.zip'
        j_name = write_json(j_data, export_name[1])
        e_name = write_excel(e_data, export_name[1])
        # 本地文件写入zip，重命名，然后删除本地临时文件
        zipFileFullDir = os.getcwd() + "/static/sdk/" + z_name
        z_file = zipfile.ZipFile(zipFileFullDir, 'w')
        z_file.write(j_name, "TRD.json")
        path = os.getcwd()+"/static/sdk/WIFI设备于53iq智能云通信协议V1.0.docx"
        z_file.write(path, 'WIFI设备于53iq智能云通信协议V1.0.docx')
        z_file.write(e_name, "TRD.xls")
        os.remove(j_name)
        os.remove(e_name)
        z_file.close()
        # 再次读取zip文件，将文件流返回
        z_file = open(zipFileFullDir, 'rb')
        data = z_file.read()
        z_file.close()

        response = HttpResponse(data, content_type='application/zip')
        from urllib import parse
        response['Content-Disposition'] = 'attachment;filename=' + parse.quote(z_name)
        return response
    except Exception as e:
        print("该出出现错误")
        logging.error(e)
        print(e)


def deal_json(app):
    temp1_data = []
    temp2_data = []
    e_data = {}
    j_data = {}
    key = app.app_appid
    len_key = len(key) - 8
    e_data['secret'] = app.app_appsecret
    e_data['key'] = key[len_key:]
    e_data['model'] = app.app_model
    e_data['command'] = app.app_command
    from common.smart_helper import get_factory_name
    e_data['band_name'] = get_factory_name(app.app_factory_uid)
    j_data['name'] = app.app_name
    j_data['model'] = app.app_model
    j_data['key'] = key[len_key:]
    j_data['secret'] = app.app_appsecret
    try:
        config_data = json.loads(app.device_conf)
    except Exception as e:
        config_data = []
        print("json loads error in :", e)
    for data in config_data:
        # 写入Excel的数据
        j = {}
        j["remarks"] = ""
        for l in range(len(data["mxs"])):
            j["remarks"] += data["mxs"][l]["data"] + ' '
            j["remarks"] += data["mxs"][l]["desc"] + ' '
        j['id'] = data['id']
        j["name"] = data["name"]
        j["Stream_ID"] = data["Stream_ID"]
        j["mxsLength"] = data["mxsLength"]
        j["values"] = json.dumps([data["min"], data["max"]])
        j['widget'] = data['corpName']
        j['isFunction'] = data.get("isFunction", 1)
        j['toSwitch'] = data.get('toSwitch', 0)

        # 写入json的数据
        i = {}
        i['value_des'] = data['mxs']
        i["id"] = data["id"]
        i["no"] = i["id"]
        i["name"] = data["Stream_ID"]
        i["title"] = data["name"]
        i["length"] = data["mxsLength"]

        i['unit'] = data['corpMark']
        i['isFunction'] = data.get("isFunction", 1)
        i['toSwitch'] = data.get('toSwitch', 0)
        i['isShow'] = data.get('isShow', 0)
        i["value"] = 0
        i["values"] = [data["min"], data["max"]]
        if data['paramType'] == 1:
            i['type'] = 'int'
        elif data['paramType'] == 3:
            i['type'] = 'error'
        elif data['paramType'] == 4:
            i['type'] = 'enum'
        elif data['paramType'] == 5:
            i['type'] = 'timer'
        if str(data["isControl"]) == '1':
            i['permission'] = '777'
            j['permission'] = "读写"
        else:
            i['permission'] = '477'
            j['permission'] = "读"
        if str(data['state']) == '1' and data.get('toSwitch') != 1:
            temp1_data.append(i)
            temp2_data.append(j)
    e_data['functions'] = temp2_data
    j_data['functions'] = temp1_data
    return {'e_data': e_data, 'j_data': j_data}


def date_deal(app_id):
    """
     数据处理，分别写入json和excel的数据
    :return:
    """
    try:
        app = App.objects.get(app_id=app_id)
        export_name = []
        temp = app.developer_id
        temp = temp.split('_')[1]
        export_name.append(app.app_name)
        export_name.append(temp)
        re = deal_json(app)
        res = write_zip(re['e_data'], re['j_data'], export_name)
        return res
    except Exception as e:
        logging.error(e)
        print(e)
