import datetime
import json
import os
import codecs
import time
import logging

from django.http import HttpResponse


from util.excelutil import get_excel_stream,save_json
from model.center.app import App



def write_excel(items):
    try:
        excel_name = time.strftime("%Y%m%d.%H.%M.%S")
        headers = {'id': '功能序号', 'name': "产品功能",'remarks':'备注','values':'值域','Stream_ID': '功能属性','mxsLength': '长度(bit)','command':'全指令'}
        items.insert(0, headers)
        header = ['id', 'name','remarks','values', 'Stream_ID', 'mxsLength','command']
        excel_stream = get_excel_stream(items, excel_name, header)
        response = HttpResponse(content_type='application/vnd.ms-excel')
        from urllib import parse

        response['Content-Disposition'] = 'attachment;filename=' + parse.quote(excel_name) + '.xls'

        #print(excel_stream)
        #print("excel_stream",excel_name)
        #print("response",response['Content-Disposition'])
        response.write(excel_stream)
        return response
    except Exception as e:
        logging.error(e)
        print(e)

def write_json(item):
    try:
        file_name = "TRD"
        json_stream=save_json(item,file_name)
        response = HttpResponse(content_type='application/json')
        from urllib import parse

        response['Content-Disposition'] = 'attachment;filename=' + parse.quote(file_name) + '.json'
        response.write(json_stream)
        return response
        # return HttpResponse(temp)
    except Exception as e:
        logging.error(e)
        print(e)
def date_deal(id):
    """
    时间段处理，并且生成表格
    :param dateRange:
    :param device_ids:
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
        #res = write_excel(tem)
        res=write_json(tem)
        return res
    except Exception as e:
        logging.error(e)
        print(e)

