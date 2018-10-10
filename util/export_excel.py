# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import logging
import zipfile
from django.http import HttpResponse


from util.excelutil import write_data
from model.center.app import App
from model.center.protocol import Protocol


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
        path2 = os.getcwd()+"/static/sdk/53IQ电控通信协议V1.1.docx"
        z_file.write(path2, '53IQ电控通信协议V1.1.docx')
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
        j = {"remarks": ""}
        for l in range(len(data["mxs"])):
            j["remarks"] += data["mxs"][l]["data"] + ' '
            j["remarks"] += data["mxs"][l]["desc"] + ' '
        j['id'] = data['id']
        j["name"] = data["name"]
        j["Stream_ID"] = data["Stream_ID"]
        j["mxsLength"] = data["mxsLength"]
        j["values"] = json.dumps([data.get("min", 0), data.get("max")])
        j['widget'] = data.get('widget', 'button')
        j['isFunction'] = data.get("isFunction", 1)
        j['toSwitch'] = data.get('toSwitch', 0)

        # 写入json的数据
        i = dict()
        i['value_des'] = data['mxs']
        i["id"] = data["id"]
        i["no"] = i["id"]
        i["name"] = data["Stream_ID"]
        i["title"] = data["name"]
        i["length"] = data["mxsLength"]
        i['unit'] = data['corpMark']
        i['isFunction'] = data.get("isFunction", 1)
        i['toSwitch'] = data.get('toSwitch', 0)
        i["isCardShow"] = data.get('isShow', 0)
        i["isUiShow"] = data.get("isDisplay", 0)
        i["widget"] = data.get("widget", "button")
        i['widgetId'] = ""
        i["value"] = 0
        i["values"] = [data.get("min", 0), data.get("max")]
        if data['paramType'] == 1:
            i['type'] = 'bool'
        elif data['paramType'] == 3:
            i['type'] = 'error'
        elif data['paramType'] == 4:
            i['type'] = 'int'
        elif data['paramType'] == 5:
            i['type'] = 'timer'
        if str(data["isControl"]) == '1':
            i['permission'] = '777'
            j['permission'] = "读写"
        else:
            i['permission'] = '477'
            j['permission'] = "读"

        temp1_data.append(i)
        temp2_data.append(j)
    try:
        p = Protocol.objects.filter(protocol_device_key=key[len_key:])
        frame_content = []
        for z in p:
            pc = json.loads(z.protocol_factory_content)
            j_data["cmdconfig"] = {
                "SendHeart": pc.get("active_heartbeat"),
                "HeartFrequency": pc.get("heart_rate"),
                "SupportSerial": pc.get("support_serial"),
                "ResendInterval": pc.get("repeat_rate"),
                "ResendTimes": pc.get("repeat_count"),
                "SupportSingleContorl": pc.get("is_single_instruction"),
                "SendResponse": pc.get("support_response_frame"),
                # "CheckoutAlgorithm": pc.get("checkout_algorithm"),
                # "StartCheckPid": pc.get("start_check_number"),
                # "EndCheckPid": pc.get("end_check_number"),
                "AnalyzeData": True,
                "isStandard": False,
                "serial_name": "/dev/ttyS1",
                "serial_baudrate": 9600,
                "serial_csize": 8,
                "serial_parity": -1,
                "serial_stopbits": 1

            }
            frame = {
                "check_type": pc.get("checkout_algorithm"),
                "check_data_start": pc.get("start_check_number"),
                "check_data_end": pc.get("end_check_number"),
                "endian_type": pc.get("endian_type", "0"),
                "length": "",
                "length_start": "",
                "length_end": "",
                "length_offset": "",
            }
            if z.protocol_factory_type == 1:
                # 下行数据
                frame["Type"] = "DownStream"
            else:
                # 上行数据
                frame["Type"] = "UpStream"
            f_content = []
            for i in pc.get('frame_content', []):
                code = []
                if i['code']:
                    for j in i['code']:
                        c = {"value": j['value'], "type": j['type']}
                        code.append(c)
                if code:
                    tmp = {"pid": i['number'], "length": i.get('length', 0), "name": i['name'], "value": code}
                else:
                    tmp = {"pid": i['number'], "length": i.get('length', 0), "name": i['name']}
                f_content.append(tmp)
            frame['structs'] = f_content
            frame_content.append(frame)
        j_data['frames'] = frame_content
    except Exception as e:
        print('处理自定义协议出错', e)
        logging.getLogger('').info("处理自定义协议出错:"+str(e))
        j_data["cmdconfig"] = {
            "SendHeart": True,
            "HeartFrequency": 1000,
            "SupportSerial": True,
            "ResendInterval": 100,
            "ResendTimes": 5,
            "SupportSingleContorl": False,
            "SendResponse": True,
            "AnalyzeData": True,
            "isStandard": True,
            "serial_name": "/dev/ttyS1",
            "serial_baudrate": 9600,
            "serial_csize": 8,
            "serial_parity": -1,
            "serial_stopbits": 1

        }
        j_data['frames'] = []
        pass
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
        print("写入excel出错", e)
