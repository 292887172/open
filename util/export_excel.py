import os
import re
import json
import logging
import zipfile

from django.http import HttpResponse

from util.excelutil import write_data
from model.center.app import App


def write_excel(items, filename):
    headers = {'id': '功能序号', 'name': "产品功能", 'remarks': '备注', 'values': '值域', 'Stream_ID': '功能属性', 'mxsLength': '长度(bit)', 'command': '全指令','permission':'权限'}
    items.insert(0, headers)
    header = ['id', 'name', 'remarks', 'values', 'Stream_ID', 'mxsLength', 'command','permission']
    excel_name = write_data(items, header, filename)
    return excel_name


def write_json(items, filename):
    filename += ".json"
    file = open(filename, 'w')
    data = json.dumps(items).encode('utf-8')
    data = data.decode('unicode-escape')
    data = re.sub(r'",', '",\n\t', data)
    data = re.sub(r'],', '],\n\t', data)
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
        z_file = zipfile.ZipFile(z_name, 'w')
        z_file.write(j_name, "TDR.json")
        z_file.write(e_name, "TRD.xls")
        os.remove(j_name)
        os.remove(e_name)
        z_file.close()
        # 再次读取zip文件，将文件流返回
        z_file = open(z_name, 'rb')
        data = z_file.read()
        z_file.close()
        os.remove(z_file.name)
        response = HttpResponse(data, content_type='application/zip')
        from urllib import parse
        response['Content-Disposition'] = 'attachment;filename=' + parse.quote(z_name)
        return response
    except Exception as e:
        logging.error(e)
        print(e)


def date_deal(id):
    """
     数据处理，分别写入json和excel的数据
    :return:
    """
    try:
        app = App.objects.get(app_id = id)
        export_name = []
        temp = app.developer_id
        temp = temp.split('_')[1]
        export_name.append(app.app_name)
        export_name.append(temp)

        temp = []
        e_data = []
        j_data = {}
        j_data['name'] = app.app_name
        j_data['model'] = app.app_model
        j_data['key'] = "0053iq11"
        config_data = json.loads(app.device_conf)
        for data in config_data:
            # 写入Excel的数据
            j = {}
            j["remarks"] = ""
            for l in range(len(data["mxs"])):
                j["remarks"] += data["mxs"][l]["data"]
                j["remarks"] += data["mxs"][l]["desc"]
            j['id'] = data['id']
            j["name"] = data["name"]
            j["Stream_ID"] = data["Stream_ID"]
            j["mxsLength"] = data["mxsLength"]
            j["command"] = app.app_command
            j["values"] = json.dumps([data["min"], data["max"]])

            # 写入json的数据
            i = {}
            i['value_des'] = []
            for l in data["mxs"]:
                k = {}
                k[l['data']] = l['desc']
                i['value_des'].append(k)
            i["id"] = data["id"]
            i["no"] = i["id"]
            i["name"] = data["Stream_ID"]
            i["title"] = data["name"]
            i["length"] = data["mxsLength"]
            i["command"] = app.app_command
            i["value"] = 0
            i["values"] = json.dumps([data["min"], data["max"]])
            if str(data["isControl"]) == '1':
                i['permission'] = '777'
                j['permission'] = "读写"
            else:
                i['permission'] = '766'
                j['permission'] = "读"
            if str(data['state']) == '1':
                temp.append(i)
                e_data.append(j)
        j_data['function'] = temp
        res = write_zip(e_data, j_data, export_name)
        return res
    except Exception as e:
        logging.error(e)
        print(e)