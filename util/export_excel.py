import os
import json
import logging
import zipfile

from django.http import HttpResponse

from util.excelutil import write_data
from model.center.app import App


def write_excel(items, filename):
    headers = {'id': '功能序号', 'name': "产品功能", 'remarks': '备注', 'values': '值域', 'Stream_ID': '功能属性', 'mxsLength': '长度(bit)', 'command': '全指令'}
    items.insert(0, headers)
    header = ['id', 'name', 'remarks', 'values', 'Stream_ID', 'mxsLength', 'command']
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
        z_file = zipfile.ZipFile(z_name, 'w')
        z_file.write(j_name, "TRD.json")
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
     并且生成表格
    :return:
    """
    try:
        app = App.objects.get(app_id = id)
        export_name = []
        temp=app.developer_id
        temp=temp.split('_')[1]
        export_name.append(app.app_name)
        export_name.append(temp)

        e_data = []
        j_data = {}
        j_data['name'] = export_name
        j_data['model'] = app.app_model
        config_data = json.loads(app.device_conf)
        for data in config_data:
            i = {}
            i["remarks"] = ""
            for j in range(len(data["mxs"])):
                i["remarks"] += data["mxs"][j]["data"]
                i["remarks"] += data["mxs"][j]["desc"]

            i["id"] = data["id"]
            i["name"] = data["name"]
            i["values"] = json.dumps([data["min"], data["max"]])
            i["Stream_ID"] = data["Stream_ID"]
            i["mxsLength"] = data["mxsLength"]
            i["command"] = app.app_command
            e_data.append(i)
        e_data.sort(key=lambda x: int(x.get("id")))
        j_data['function'] = e_data
        res = write_zip(e_data, j_data, export_name)
        return res
    except Exception as e:
        logging.error(e)
        print(e)