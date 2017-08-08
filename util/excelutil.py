# -*- coding: utf-8 -*-

import xlwt

__author__ = 'sunshine'


def write_data(data, header):
    """
    导出excel
    :param data:
    :param name:
    :param header:
    :return:
    """
    excel_name = 'TRD.xls'
    file = xlwt.Workbook(encoding="utf-8")
    table = file.add_sheet(excel_name, cell_overwrite_ok=True)
    if data is None:
        return file
    # l表示行
    l = 0
    n = len(header)
    data1 = data[1:]
    data1.sort(key = lambda x: int(x.get('id')))
    for i in range(n):
        table.write(l, i, data[0][header[i]])
    for line in data1:
        l += 1
        for i in range(n):
            table.write(l, i, line[header[i]])
    file.save(excel_name)
    return excel_name
