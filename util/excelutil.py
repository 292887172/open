import io

import datetime
import xlwt
import json

import codecs
__author__ = 'sunshine'


def write_data(data, name, header):
    """
    导出excel
    :param data:
    :param name:
    :param header:
    :return:
    """
    file = xlwt.Workbook(encoding="utf-8")
    table = file.add_sheet(name, cell_overwrite_ok=True)
    print("excel_name",name)
    if data is None:
        return file
    l = 0  # 表示行
    n = len(header)
    for line in data:
        for i in range(n):
            table.write(l, i, line[header[i]])
        l += 1
    # file.save('excel.xls')

    return file
def save_json(data,file_name):
    file = io.StringIO()
    data=json.dumps(data)
    file.write(data,encode='utf-8')
    res=file.getvalue()
    file.close()
    return  res

def get_excel_stream(data, name, header):
    excel = write_data(data, name, header)
    excel_stream = io.BytesIO()
    print("excel_stream",excel_stream)
    excel.save(excel_stream)
    res = excel_stream.getvalue()
    excel_stream.close()
    return res


if __name__ == "__main__":
    # main()
    data = [
        ['a', 'b', 'c', 'd', 'e'],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
        [1, 2, 3, 4, 5],
    ]
    name = ['a', 'b', 'c', 'd', 'e']
    get_excel_stream(data, 'demo', name)
    pass
