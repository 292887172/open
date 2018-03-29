# -*- coding: utf-8 -*-

import xlwt

__author__ = 'sunshine'


def set_style(name, height, color='black', bold=False):
    style = xlwt.easyxf('font: bold 1, color %s ;' %(color))  # 初始化样式
    style.font.height = height
    style.font.name = name
    style.font.bold = bold
    return style


def set_style1(name, height, bold=False):
    style = xlwt.easyxf()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


def to_check_bit(f_type, length, states):
    check_bit = int('A5', 16) + int('5A', 16) + int(f_type, 16) + length + states
    check_bit = bin(check_bit)[-8:]
    check_bit = hex(int(check_bit, 2))[2:]
    return check_bit


def to_com_frame(header, f_type, length, values, check_bit, result=''):
    com_frame = header + ' 00 ' + f_type + ' ' + to_hex(length) + ' ' + result + ' '.join(values) + ' ' + check_bit
    return com_frame


def to_hex(length):
    num = hex(length)[2:]
    if len(num) == 1:
        return "0" + num
    else:
        return num


def to_fun_state(num):
    if int(num) < 10:
        state = '0' + str(num)
    else:
        state = str(num)
    values = [state, '01', '', '']
    return values


def ascll_to_hex(key):
    list = []
    for i in key:
        str1 = hex(ord(i))[2:]
        if len(str1) == 1:
            list.append("0" + str1)
        else:
            list.append(str1)
    return list


def cal_ascll(key):
    num = 0
    for i in key:
        num += ord(i)
    return num


def getLength(temp,length,toLen):

    temp += length

    if(temp%8 == 0):
        toLen += temp//8
        temp = 0
    elif(temp>8):
        a = (temp-length)//8+1
        toLen += a
        temp = length
    return temp,toLen



def data_domain(sheet2, data, i):
    funs = data['functions']
    # 数据域功能数,除去头部
    k = len(funs)-1
    # 数据域长度（位数）
    toLen = 0
    temp = 0
    values = []
    long_values = []
    lamp_id = 1
    fun_value = 0
    fun_name = ''
    num = 0
    value = ''
    # 全功能头部部分
    sheet2.write_merge(4, 4, i, i+k, "数据域", set_style('Arial', 220))
    sheet2.write(5, i, "结果码", set_style('Arial', 220))
    for index, line in enumerate(funs[1:], i+1):
        # 获取数据域所有功能对应的值 默认第一个数据位为1
        _bit = '00'
        length = int(line['mxsLength'])
        num += length
        if index == i+1:
            lamp_id = line['id']
            fun_name = line['name']
            fun_value = 1
            if length % 8 == 0:
                _bit = '01' + ' 00'*(length//8-1)
                values.append(_bit)
            else:
                t = '0' * (length % 8-1) + '1'
                _bit = '01'
                value += t
        else:
            if num % 8 == 0 and length % 8 != 0:
                num = 0
                t = '0' * (length % 8)
                value += t
                v = int(value, 2)
                value = ''
                values.append(to_hex(v))
            elif length % 8 == 0:
                num = 0
                _bit = '00'+' 00'*(length//8-1)
                values.append(_bit)
            else:
                t = '0' * (length % 8)
                value += t
        long_values.append(_bit)
        temp, toLen = getLength(temp, length, toLen)
        # 找到照明对应的id
        sheet2.write(5, index, line['name'], set_style('Arial', 220))
    if temp > 0:
        if temp % 8 == 0:
            toLen += temp//8
        else:
            toLen += temp//8 + 1
    sheet2.write_merge(4, 5, i+k+1, i+k+1, "校验", set_style('Arial', 220))
    S_C = "点击屏上{0}按钮打开{0}".format(fun_name)
    C_S = "电控修改{0}按钮状态".format(fun_name)
    row4 = [S_C, '屏->电控', '', 'A5 5A', '00', '21', to_hex(toLen), '']
    row5 = [C_S, '电控->屏', '', '5A A5', '00', '21', to_hex(toLen + 1), '00']
    row6 = ['例子（单功能）', '', '', '帧头', '流水号', '帧类型', '长度', '结果码', '功能1', '状态1', '功能2', '状态2', '校验']
    row7 = [S_C, '屏->电控', '', 'A5 5A', '00', '31', '02', '']
    row8 = [C_S, '电控->屏', '', '5A A5', '00', '31', '03', '00']
    # 全功能数据
    check_bit1 = to_check_bit('21', toLen, fun_value)
    check_bit2 = to_check_bit('21', toLen + 1, fun_value)
    com_frame1 = to_com_frame('A5 5A', '21', toLen, values, check_bit1, result=' ')
    com_frame2 = to_com_frame('5A A5', '21', toLen + 1, values, check_bit2, result=' 00 ')
    row4[2] = com_frame1
    row5[2] = com_frame2
    row4.extend(long_values)
    row5.extend(long_values)
    row4.append(check_bit1)
    row5.append(check_bit2)
    # 单功能数据
    fun_state0 = to_fun_state(lamp_id)
    fun_state1 = to_fun_state(lamp_id)
    check_bit3 = to_check_bit('31', 2, int(lamp_id) + fun_value)
    check_bit4 = to_check_bit('31', 3, int(lamp_id) + fun_value)
    com_frame3 = to_com_frame('A5 5A', '31', 2, fun_state0, check_bit3, result='')
    com_frame4 = to_com_frame('5A A5', '31', 3, fun_state1, check_bit4, result='00 ')
    row7[2] = com_frame3
    row8[2] = com_frame4
    row7.extend(fun_state0)
    row8.extend(fun_state1)
    row7.append(check_bit3)
    row8.append(check_bit4)

    for i in range(len(row4)):
        if i == 6 or i == 7:
            sheet2.write(6, i, row4[i], set_style('Arial', 220, 'red'))
            sheet2.write(7, i, row5[i], set_style('Arial', 220, 'red'))
        else:
            sheet2.write(6, i, row4[i], set_style('Arial', 220))
            sheet2.write(7, i, row5[i], set_style('Arial', 220))
    for i in range(len(row6)):
        sheet2.write(9, i, row6[i], set_style('Arial', 220))
        if i == 6 or i == 7:
            sheet2.write(10, i, row7[i], set_style('Arial', 220, 'red'))
            sheet2.write(11, i, row8[i], set_style('Arial', 220, 'red'))
        else:
            sheet2.write(10, i, row7[i], set_style('Arial', 220))
            sheet2.write(11, i, row8[i], set_style('Arial', 220))


def write_example(sheet2, data):
    # 写入帧对应的表格
    key = data['key']
    model = "型号(%s)"%(key)
    row0 = ["例子（通信握手）", "指令流向", "完整帧", "帧头", "流水号", "帧类型", "长度", "结果码", "版本号",
            "唯一编号(MAC地址：AAAAAABBBBBB)", model, "校验"]
    row1 = ['连接上服务器后收到握手命令帧', '屏->电控', 'A5 5A 00 01 00 00', 'A5 5A', '00', '01', '00']
    row2 = ['电控应答握手帧上报MAC和型号编号', '电控->屏',
            '','5A A5', '00', '01', '17', '00', '00', '01']
    row3 = ["例子(全功能)", "指令流向", "完整帧", "帧头", "流水号", "帧类型", "长度"]

    result_and_version = '00 00 01 '
    value_list = ascll_to_hex("AAAAAABBBBBB") + ascll_to_hex(key)
    values = cal_ascll("AAAAAABBBBBB") + cal_ascll(key)
    check_bit = to_check_bit('01', 23, values + 1)
    com_frame = to_com_frame('5A A5', '01', 23, value_list, check_bit, result_and_version)
    row2[2] = com_frame
    row2.extend(value_list)
    row2.append(check_bit)

    j = 0
    sheet2.col(j).width = 256*40
    sheet2.col(2).width = 256*80

    # 通信握手头部
    for i in range(len(row0)):
        k = j
        if i == 8:
            j += 1
        elif i == 9:
            j += 11
        elif i == 10:
            j += 7
        if k != j:
            sheet2.write_merge(0, 0, k, j, row0[i], set_style('Arial', 220))
        else:
            sheet2.write(0, j, row0[i], set_style('Arial', 220))
        j += 1
    for i in range(len(row2)):
        # 通信握手数据部分
        if i < len(row1):
            sheet2.write(1, i, row1[i], set_style('Arial', 220))
        else:
            sheet2.write(1, len(row2)-1, '00', set_style('Arial', 220))
        sheet2.write(2, i, row2[i], set_style('Arial', 220))
        # 写入全功能例子
        if i < len(row3):
            sheet2.write_merge(4, 5, i, i, row3[i], set_style('Arial', 220))
        elif i == len(row3):
            # 写入数据域表格信息
            data_domain(sheet2, data, i)


def write_data(data, header, filename):
    """
    导出excel
    :param data:
    :param filename:
    :param header:
    :return:
    """
    excel_name = filename + ".xls"
    file = xlwt.Workbook(encoding="utf-8")
    sheet1 = file.add_sheet('功能映射表', cell_overwrite_ok=True)
    sheet2 = file.add_sheet('示例', cell_overwrite_ok=True)
    write_example(sheet2, data)
    if data is None:
        return file
    sheet1.write_merge(0, 3, 0, 0, '对接信息', set_style1('Arial', 220, True))
    sheet1.write_merge(0, 1, 1, 1, '沙箱环境')
    sheet1.write(0, 2, 'url')
    sheet1.write(1, 2, 'port')
    sheet1.write(0, 3, 'sandbox.53iq.com')
    sheet1.write(1, 3, '2502')
    sheet1.write_merge(2, 3, 1, 1, '生产环境')
    sheet1.write(2, 2, 'url')
    sheet1.write(3, 2, 'port')
    sheet1.write(2, 3, 'suite.53iq.com')
    sheet1.write(3, 3, '2502')
    sheet1.write_merge(4, 6, 0, 0, '产品信息', set_style1('Arial', 220, True))
    sheet1.write(4, 1, '品牌')
    sheet1.write(4, 2, data['band_name'])
    sheet1.write(5, 1, '型号')
    sheet1.write(5, 2, data['model'])
    sheet1.write(6, 1, '全指令')
    sheet1.write(6, 2, data['command'])
    sheet1.write_merge(7, 10, 0, 0, '授权信息', set_style1('Arial', 220, True))
    sheet1.write_merge(7, 8, 1, 1, '沙箱环境')
    sheet1.write_merge(9, 10, 1, 1, '生产环境')
    sheet1.write(7, 2, 'key')
    sheet1.write(7, 3, data['key'])
    sheet1.write(8, 2, 'secret')
    sheet1.write(8, 3, data['secret'])
    sheet1.write(9, 2, 'key')
    sheet1.write(9, 3, data['key'])
    sheet1.write(10, 2, 'secret')
    sheet1.write(10, 3, data['secret'])
    # l表示行
    l = 10
    n = len(header)
    for index, line in enumerate(data['functions']):
        for i in range(n):
            sheet1.col(index).width = 256*30
            if index == 0:
                sheet1.write(l, i, line[header[i]], set_style1('Arial', 220, True))
            else:
                sheet1.write(l, i, line[header[i]])
        l += 1
    file.save(excel_name)
    return excel_name
