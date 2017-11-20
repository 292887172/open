# !/bash/bin/env python
# -*- coding: utf-8 -*-
import xlrd
from xlrd import xldate_as_tuple
from datetime import datetime, timedelta
import pymysql
__author__ = 'rdy'


def get_main_connection():
    """
    连接主数据库
    :return:
    """
    conn = pymysql.connect(
        host='192.168.0.62',
        port=3306,
        user='root',
        passwd='53iq.com',
        db='ebdb_smartsys',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn


def save_alidata2db():
    conn = get_main_connection()
    cursor = conn.cursor()
    fname = "2375zhi.xls"
    bk = xlrd.open_workbook(fname)
    shxrange = range(bk.nsheets)
    try:
        sh = bk.sheet_by_name("Sheet1")
    except:
        print("no sheet in %s named Sheet1" % fname)
        return ''
    # 获取行数
    nrows = sh.nrows
    # 获取列数
    ncols = sh.ncols
    print("nrows %d, ncols %d" % (nrows, ncols))
    # 获取第一行第一列数据
    cell_value = sh.cell_value(5, 4)
    print(cell_value)
    # 获取各行数据
    for i in range(1, 2):
        trade_no = str(sh.cell_value(i, 3)).strip()
        sql = 'select ebf_third_trade_no FROM ebt_pay ' \
              ' WHERE ebf_pay_trade_no="{0}" LIMIT 1'.format(trade_no)

        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            print('already have', trade_no)
            pass
        else:
            did = str(sh.cell_value(i, 0)).strip()
            agency_id = int(sh.cell_value(i, 1))
            third_no = str(sh.cell_value(i, 2)).strip()

            pay_fee = float(sh.cell_value(i, 7))
            pay_is_success = int(sh.cell_value(i, 4))
            pay_status = int(sh.cell_value(i, 5))
            pay_create_date = datetime(*xldate_as_tuple(sh.cell_value(i, 8), 0))-timedelta(hours=8)
            remarks = str(sh.cell_value(i, 6)).strip()
            pay_type = 1    # 1:支付宝， 2：微信
            factory_id = 10     # 10: 傻老板
            pay_trade_type = 1  # 1:消费订单 2：充值订单
            sql = 'insert into ebt_pay(ebf_device_id, ebf_pay_trade_no, ebf_pay_fee, ebf_pay_is_success, ' \
                  'ebf_pay_create_date, ebf_pay_type, ebf_pay_remarks, ebf_pay_status, ebf_pay_pay_date, ' \
                  'ebf_third_trade_no, ebf_pay_agency_id, ebf_pay_factory_id, ebf_pay_trade_type) ' \
                  'VALUES ({0},{1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}, {11}, {12})' \
                  ''.format(did, trade_no, pay_fee, pay_is_success, pay_create_date, pay_type, remarks, pay_status,
                            pay_create_date, third_no, agency_id, factory_id, pay_trade_type)
            print(sql)
            cursor.execute(sql)
            conn.commit()
            print('saved', trade_no)

if __name__ == '__main__':
    save_alidata2db()