# !/bash/bin/env python
# -*- coding: utf-8 -*-
import xlrd
from xlrd import xldate_as_tuple
from datetime import datetime, timedelta
import pymysql
import time
__author__ = 'rdy'


def get_main_connection():
    """
    连接主数据库
    :return:
    """
    conn = pymysql.connect(
        host='s73.53iq.com',
        port=3306,
        user='root',
        passwd='53iq.com',
        db='ebdb_smartsys_1',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn


def save_alidata2db():
    conn = get_main_connection()
    cursor = conn.cursor()
    fname = "1282zhi2.xls"
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
    n = 0
    for i in range(1, nrows):
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
            # did = '1000000022'
            if did:
                did = did.replace("'", "")
                try:
                    agency_id = int(sh.cell_value(i, 1))
                except Exception as e:
                    continue
                third_no = str(sh.cell_value(i, 2)).strip()

                pay_fee = float(sh.cell_value(i, 7))
                pay_is_success = int(sh.cell_value(i, 4))
                pay_status = int(sh.cell_value(i, 5))
                pay_create_date = datetime(*xldate_as_tuple(sh.cell_value(i, 8), 0))-timedelta(hours=8)
                # pay_create_date = datetime.utcnow()
                remarks = str(sh.cell_value(i, 6)).strip()
                pay_type = 1    # 1:支付宝， 2：微信
                factory_id = 10     # 10: 傻老板
                pay_trade_type = 1  # 1:消费订单 2：充值订单
                try:
                    sql = 'insert into ebt_pay(ebf_device_id, ebf_pay_trade_no, ebf_pay_fee, ebf_pay_is_success, ' \
                          'ebf_pay_create_date, ebf_pay_type, ebf_pay_remarks, ebf_pay_status, ebf_pay_pay_date, ' \
                          'ebf_third_trade_no, ebf_pay_agency_id, ebf_pay_factory_id, ebf_pay_trade_type) ' \
                          'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                    cursor.execute(sql, [did, trade_no, pay_fee, pay_is_success, pay_create_date, pay_type, remarks, pay_status,
                                    pay_create_date, third_no, agency_id, factory_id, pay_trade_type])
                    conn.commit()
                    print('saved', trade_no)
                    n += 1
                    time.sleep(0.2)
                except Exception as e:
                    print(e, trade_no)
                    time.sleep(0.2)
    print(n)


def save_wxdata2db():
    conn = get_main_connection()
    cursor = conn.cursor()
    fname = "1156wx2.xls"
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

    cell_value = sh.cell_value(2, 8)
    print(cell_value, datetime.strptime(cell_value, "%Y-%m-%d %H:%M:%S")-timedelta(hours=8))
    # 获取各行数据
    n = 0
    for i in range(1, nrows):
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
            # did = '1000000022'
            if did:
                did = did.replace("'", "")
                try:
                    agency_id = int(sh.cell_value(i, 1))
                except Exception as e:
                    continue
                third_no = str(sh.cell_value(i, 2)).strip()

                pay_fee = float(sh.cell_value(i, 7))
                pay_is_success = int(sh.cell_value(i, 4))
                pay_status = int(sh.cell_value(i, 5))
                pay_create_date = datetime.strptime(sh.cell_value(i, 8), "%Y-%m-%d %H:%M:%S")-timedelta(hours=8)
                # pay_create_date = datetime.utcnow()
                remarks = str(sh.cell_value(i, 6)).strip()
                pay_type = 2    # 1:支付宝， 2：微信
                factory_id = 10     # 10: 傻老板
                pay_trade_type = 1  # 1:消费订单 2：充值订单
                try:
                    sql = 'insert into ebt_pay(ebf_device_id, ebf_pay_trade_no, ebf_pay_fee, ebf_pay_is_success, ' \
                          'ebf_pay_create_date, ebf_pay_type, ebf_pay_remarks, ebf_pay_status, ebf_pay_pay_date, ' \
                          'ebf_third_trade_no, ebf_pay_agency_id, ebf_pay_factory_id, ebf_pay_trade_type) ' \
                          'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                    cursor.execute(sql, [did, trade_no, pay_fee, pay_is_success, pay_create_date, pay_type, remarks, pay_status,
                                    pay_create_date, third_no, agency_id, factory_id, pay_trade_type])
                    conn.commit()
                    print('saved', trade_no)
                    n += 1
                    time.sleep(0.2)
                except Exception as e:
                    print(e, trade_no)
                    time.sleep(0.2)
    print(n)


def save_wx2data2db():
    conn = get_main_connection()
    cursor = conn.cursor()
    fname = "order.xlsx"
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



    # 获取各行数据
    n = 0
    for i in range(1, nrows):
        trade_no = str(sh.cell_value(i, 0)).strip().replace("'", "")
        device_alias = str(sh.cell_value(i, 1)).strip().replace("'", "")
        agency_id = int(sh.cell_value(i, 2))
        try:
            sql = 'update ebt_pay set ebf_pay_agency_id={0} where ebf_pay_trade_no="{1}"'.format(agency_id, trade_no)

            cursor.execute(sql)
            conn.commit()
            print('saved', trade_no, agency_id)
        except Exception as e:
            print(e, trade_no)



def save_wx_chong_data2db():
    conn = get_main_connection()
    cursor = conn.cursor()
    fname = "32wxchong.xls"
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

    cell_value = sh.cell_value(2, 8)
    print(cell_value, datetime.strptime(cell_value, "%Y-%m-%d %H:%M:%S")-timedelta(hours=8))
    # 获取各行数据
    n = 0
    for i in range(1, nrows):
        trade_no = str(sh.cell_value(i, 3)).strip()
        sql = 'select ebf_third_trade_no FROM ebt_pay ' \
              ' WHERE ebf_pay_trade_no="{0}" LIMIT 1'.format(trade_no)

        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            print('already have', trade_no)
            pass
        else:

            third_no = str(sh.cell_value(i, 2)).strip()

            pay_fee = float(sh.cell_value(i, 7))
            pay_is_success = int(sh.cell_value(i, 4))
            pay_status = int(sh.cell_value(i, 5))
            pay_create_date = datetime.strptime(sh.cell_value(i, 8), "%Y-%m-%d %H:%M:%S")-timedelta(hours=8)
            # pay_create_date = datetime.utcnow()
            remarks = str(sh.cell_value(i, 6)).strip()
            pay_type = 2    # 1:支付宝， 2：微信
            factory_id = 10     # 10: 傻老板
            pay_trade_type = 2  # 1:消费订单 2：充值订单
            try:
                sql = 'insert into ebt_pay(ebf_pay_trade_no, ebf_pay_fee, ebf_pay_is_success, ' \
                      'ebf_pay_create_date, ebf_pay_type, ebf_pay_remarks, ebf_pay_status, ebf_pay_pay_date, ' \
                      'ebf_third_trade_no, ebf_pay_agency_id, ebf_pay_factory_id, ebf_pay_trade_type) ' \
                      'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                cursor.execute(sql, [trade_no, pay_fee, pay_is_success, pay_create_date, pay_type, remarks, pay_status,
                                pay_create_date, third_no, None, factory_id, pay_trade_type])
                conn.commit()
                print('saved', trade_no)
                n += 1
                time.sleep(0.2)
            except Exception as e:
                print(e, trade_no)
                time.sleep(0.2)
    print(n)


def save_ali_chong_data2db():
    conn = get_main_connection()
    cursor = conn.cursor()
    fname = "17alichong.xls"
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
    n = 0
    for i in range(1, nrows):
        trade_no = str(sh.cell_value(i, 3)).strip()
        sql = 'select ebf_third_trade_no FROM ebt_pay ' \
              ' WHERE ebf_pay_trade_no="{0}" LIMIT 1'.format(trade_no)

        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            print('already have', trade_no)
            pass
        else:

            third_no = str(sh.cell_value(i, 2)).strip()

            pay_fee = float(sh.cell_value(i, 7))
            pay_is_success = int(sh.cell_value(i, 4))
            pay_status = int(sh.cell_value(i, 5))
            pay_create_date = datetime(*xldate_as_tuple(sh.cell_value(i, 8), 0))-timedelta(hours=8)
            # pay_create_date = datetime.utcnow()
            remarks = str(sh.cell_value(i, 6)).strip()
            pay_type = 1    # 1:支付宝， 2：微信
            factory_id = 10     # 10: 傻老板
            pay_trade_type = 2  # 1:消费订单 2：充值订单
            try:
                sql = 'insert into ebt_pay(ebf_pay_trade_no, ebf_pay_fee, ebf_pay_is_success, ' \
                      'ebf_pay_create_date, ebf_pay_type, ebf_pay_remarks, ebf_pay_status, ebf_pay_pay_date, ' \
                      'ebf_third_trade_no, ebf_pay_agency_id, ebf_pay_factory_id, ebf_pay_trade_type) ' \
                      'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

                cursor.execute(sql, [trade_no, pay_fee, pay_is_success, pay_create_date, pay_type, remarks, pay_status,
                                pay_create_date, third_no, None, factory_id, pay_trade_type])
                conn.commit()
                print('saved', trade_no)
                n += 1
                time.sleep(0.2)
            except Exception as e:
                print(e, trade_no)
                time.sleep(0.2)
    print(n)

if __name__ == '__main__':
    # save_alidata2db()
    save_wx2data2db()