import os
import json
import logging
import zipfile

from django.http import HttpResponse

from util.excelutil import write_data
from model.center.app import App


def write_excel(items):
    headers = {'id': '功能序号', 'name': "产品功能", 'remarks': '备注', 'values': '值域', 'Stream_ID': '功能属性', 'mxsLength': '长度(bit)', 'command': '全指令'}
    items.insert(0, headers)
    header = ['id', 'name', 'remarks', 'values', 'Stream_ID', 'mxsLength', 'command']
    excel_name = write_data(items, header)
    return excel_name


def write_json(items):
    file = open("TRD.json", 'w')
    file.write(json.dumps(items))
    file.close()
    return file.name


def write_zip(items):
    try:
        # 将两个文件写入zip
        j_name = write_json(items)
        e_name = write_excel(items)
        z_file = zipfile.ZipFile("森太油烟机TRD.zip", 'w')
        z_file.write(j_name)
        z_file.write(e_name)
        z_file.close()
        os.remove(e_name)
        os.remove(j_name)
        # 再次读取zip文件，将文件流返回
        z_file = open("森太油烟机TRD.zip", 'rb')
        data = z_file.read()
        z_file.close()
        os.remove(z_file.name)
        response = HttpResponse(data, content_type='application/zip')

        from urllib import parse
        response['Content-Disposition'] = 'attachment;filename=' + parse.quote("森太油烟机TRD") + '.zip'
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
        tem = []
        all_data = json.loads(app.device_conf)
        for data in all_data:
            i = {}
            i['remarks'] = ""
            for j in range(len(data['mxs'])):
                i['remarks'] += data['mxs'][j]['data']
                i['remarks'] += data['mxs'][j]['desc']

            i['id'] = data['id']
            i['name'] = data['name']
            i['values'] = json.dumps([data['min'], data['max']])
            i['Stream_ID'] = data['Stream_ID']
            i['mxsLength'] = data['mxsLength']
            i['command'] = app.app_command
            tem.append(i)
        res = write_zip(tem)
        return res
    except Exception as e:
        logging.error(e)
        print(e)