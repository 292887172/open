import json
import logging
import zipfile

from django.http import HttpResponse

from django.core.servers.basehttp import FileWrapper
from util.excelutil import get_excel_stream, get_stream
from model.center.app import App



def write_excel(items):
    try:
        excel_name = "TRD"
        headers = {'id': '功能序号', 'name': "产品功能",'remarks':'备注','values':'值域','Stream_ID': '功能属性','mxsLength': '长度(bit)','command':'全指令'}
        items.insert(0, headers)
        header = ['id', 'name','remarks','values', 'Stream_ID', 'mxsLength','command']
        excel_stream = get_excel_stream(items, excel_name, header)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        from urllib import parse
        response['Content-Disposition'] = 'attachment;filename=' + parse.quote(excel_name) + '.xls'
        response.write(excel_stream)
        return response
    except Exception as e:
        logging.error(e)
        print(e)


def write_json(item):
    try:
        file_name="TRD"
        json_stream=get_stream(item)
        response = HttpResponse(content_type='application/json')
        from urllib import parse
        response['Content-Disposition'] = 'attachment;filename=' + parse.quote(file_name) + '.json'
        response.write(json_stream)
        return response
    except Exception as e:
        logging.error(e)
        print(e)

def write_zip(items):
    try:
        file1=open("TRD.json",'w')
        file1.write(json.dumps(items))
        file1.close()

        file2=zipfile.ZipFile("森太油烟机TRD.zip",'w')
        file2.write(file1.name)
        file2.close()

        wrapper = FileWrapper(file1.name)
        response = HttpResponse(wrapper,content_type='application/zip')
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
        # tem 最总写入excel的数据列表
        app=App.objects.get(app_id=id)
        print(id,type(app.device_conf))
        tem=[]
        all_data = json.loads(app.device_conf)
        for data in all_data:
            i={}
            i['remarks']=""
            for j in range(len(data['mxs'])):
                i['remarks']+=data['mxs'][j]['data']
                i['remarks']+=data['mxs'][j]['desc']
            i['id']=data['id']
            i['name']=data['name']
            i['values']=json.dumps([data['min'],data['max']])
            i['Stream_ID']=data['Stream_ID']
            i['mxsLength']=data['mxsLength']
            i['command']=app.app_command
            tem.append(i)
        res = write_excel(tem)
        #res=write_json(tem)
        #res=write_zip(tem)
        return res
    except Exception as e:
        logging.error(e)
        print(e)