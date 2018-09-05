# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import shutil

from base.connection import mysql_conn_poll


def test_name():
    root = "/Users/zhanlingjie/Documents/mypython/Git/open"

    for dirpath, dirnames, filenames in os.walk(root):
        for filepath in filenames:
            if '__' in dirpath:
                try:
                    shutil.rmtree(dirpath)
                    print(dirpath)
                except Exception as e:
                    pass


# def Square(num):
#     temp = str(num)
#     n = 0
#     for index,value in enumerate(temp):
#         if index == len(temp)-1:
#             print(value+'*'+value, end='')
#         else:
#             print(value+'*'+value+' + ', end='')
#         a= int(value)
#         n += a*a
#     print(' = ',n,)
#     if n == 1:
#         return 1
#     return Square(n)
# def countBits(self, num):
#         """
#         :type num: int
#         :rtype: List[int]
#         """
#         list = []
#         for i in range(0,num+1):
#             count = bin(i).count('1')
#             list.append(count)
#         return list


if __name__ == "__main__":
    conn = mysql_conn_poll.conn
    try:
        cursor = conn.cursor()
        sql = 'SELECT *  FROM ebt_doc_ui'
        cursor.execute(sql)
        result = cursor.fetchall()

        for i in result:
            print(i)
            sql = "INSERT INTO ebt_doc_ui_history(" \
                  "ebf_ui_key," \
                  "ebf_ui_content," \
                  "ebf_ui_type," \
                  "ebf_ui_title," \
                  "ebf_ui_create_date," \
                  "ebf_ui_update_date" \
                  "ebf_ui_upload_id" \
                  "ebf_ui_ack" \
                  "ebf_ui_time_stemp" \
                  "ebf_ui_remark" \
                  "ebf_ui_party" \
                  "ebf_ui_plan) "
            sql += "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args = [i.get('ebf_ui_key'), i.get('ebf_ui_content'), i.get('ebf_ui_type'),
                    i.get('ebf_ui_title'), i.get('ebf_ui_create_date'),
                    i.get('ebf_ui_update_date'), i.get('ebf_ui_upload_id'), i.get('ebf_ui_ack'),
                    i.get('ebf_ui_time_stemp'), i.get('ebf_ui_remark'), i.get('ebf_ui_party'), i.get('ebf_ui_plan')]
            print(len(args))
            cursor.execute(sql, args)
            conn.commit()
    except Exception as e:
        print(e)
        pass
    finally:
        conn.close()
