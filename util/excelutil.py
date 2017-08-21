# -*- coding: utf-8 -*-

import xlwt

__author__ = 'sunshine'


def set_style(name, height, bold=False):
    style = xlwt.XFStyle()  # 初始化样式

    font = xlwt.Font()  # 为样式创建字体
    font.name = name  # 'Times New Roman'
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style


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
    table = file.add_sheet(excel_name, cell_overwrite_ok=True)

    if data is None:
        return file
    table.write_merge(0, 3, 0, 0, '对接信息', set_style('Arial', 220, True))
    table.write_merge(0, 1, 1, 1, '沙箱环境')
    table.write(0, 2, 'url')
    table.write(1, 2, 'port')
    table.write(0, 3, 'suite.63iq.com')
    table.write(1, 3, '2502')
    table.write_merge(2, 3, 1, 1, '生产环境')
    table.write(2, 2, 'url')
    table.write(3, 2, 'port')
    table.write(2, 3, 'suite.53iq.com')
    table.write(3, 3, '2502')
    table.write_merge(4, 5, 0, 0, '产品信息', set_style('Arial', 220, True))
    table.write(4, 1, '品牌')
    table.write(4, 2, '纳帕集成灶')
    table.write(5, 1, '型号')
    table.write(5, 2, data['model'])
    table.write_merge(6, 9, 0, 0, '授权信息', set_style('Arial', 220, True))
    table.write_merge(6, 7, 1, 1, '沙箱环境')
    table.write_merge(8, 9, 1, 1, '生产环境')
    table.write(6, 2, 'key')
    table.write(6, 3, data['key'])
    table.write(7, 2, 'secret')
    table.write(7, 3, data['secret'])
    table.write(8, 2, 'key')
    table.write(8, 3, data['key'])
    table.write(9, 2, 'secret')
    table.write(9, 3, data['secret'])
    # l表示行
    l = 10
    n = len(header)
    for index, line in enumerate(data['function']):
        for i in range(n):
            table.col(index).width = 256*30
            if index == 0:
                table.write(l, i, line[header[i]], set_style('Arial', 220, True))
            else:
                table.write(l, i, line[header[i]])
        l += 1
    file.save(excel_name)
    return excel_name
