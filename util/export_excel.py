import json
import logging
import zipfile
import tarfile
import os
from django.http import HttpResponse

from django.core.servers.basehttp import FileWrapper
from util.excelutil import get_excel_stream, get_stream,write_data
from model.center.app import App



def write_excel(items):
    excel_name = "TRD"
    headers = {'id': '功能序号', 'name': "产品功能",'remarks':'备注','values':'值域','Stream_ID': '功能属性','mxsLength': '长度(bit)','command':'全指令'}
    items.insert(0, headers)
    header = ['id', 'name','remarks','values', 'Stream_ID', 'mxsLength','command']
    file=write_data(items,excel_name,header)
    return file


def write_json(items):
    file =open("TRD.json",'w')
    file.write(json.dumps(items))
    file.close()
    return file.name


def write_zip(items):
    try:
        file_json = write_json(items)
        file_excel = write_excel(items)
        file_zip = zipfile.ZipFile("森太油烟机TRD.zip", 'wb', zipfile.ZIP_DEFLATED)
        file_zip.write(file_json)
        file_zip.write(file_excel)
        file_zip.close()
        os.remove(file_excel)
        os.remove(file_json)

        response = HttpResponse(content_type = 'application/zip')
        from urllib import parse
        response['Content-Disposition'] = 'attachment;filename=森太油烟机TRD.zip'
        #ff = zipfile.ZipFile("森太油烟机TRD.zip",'r')
        ff=open("森太油烟机TRD.zip",'r')

        response.write(ff)
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
        # tem 最总写入excel的数据列表
        app = App.objects.get(app_id=id)
        print(id,type(app.device_conf))
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
            i['values'] = json.dumps([data['min'],data['max']])
            i['Stream_ID'] = data['Stream_ID']
            i['mxsLength'] = data['mxsLength']
            i['command'] = app.app_command
            tem.append(i)
        #res = write_excel(tem)
        #res=write_json(tem)
        res = write_zip(tem)
        return res
    except Exception as e:
        logging.error(e)
        print(e)