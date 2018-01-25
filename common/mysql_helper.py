import logging

import pymysql

from conf.mysqlconf import MYSQL_HOST_SYS, MYSQL_PORT_SYS, MYSQL_USER_SYS, MYSQL_PWD_SYS, MYSQL_DB_SYS
from base.crypto import md5_en
import datetime


def get_main_connection():
    """
    连接主数据库
    :return:
    """
    conn = pymysql.connect(
        host=MYSQL_HOST_SYS,
        port=MYSQL_PORT_SYS,
        user=MYSQL_USER_SYS,
        passwd=MYSQL_PWD_SYS,
        db=MYSQL_DB_SYS,
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    return conn


def close_connection(conn):
    """
    关闭数据库连接
    :param conn:
    :return:
    """
    conn.close()


def check_user_password(user, password):
    """
    从ebdb_smartsys库的ebt_user表中校验用户名和密码
    :param user:
    :param password:
    :return:
    """
    conn = get_main_connection()
    obj = {"status": None, "result": None}

    try:
        cursor = conn.cursor()
        sql = 'select ebf_user_password,ebf_user_phone,ebf_user_is_forbid FROM ebt_user ' \
              ' WHERE ebf_user_id="{0}" LIMIT 1'.format(user)

        cursor.execute(sql)
        result = cursor.fetchone()
        if result:
            if md5_en(password) == result['ebf_user_password']:
                re = {
                    'phone': result['ebf_user_phone'],
                    'is_forbid': result['ebf_user_is_forbid']
                }
                obj['status'] = 'ok'
                obj['result'] = re
            else:
                obj['status'] = 'error'
                obj['result'] = 'invalid password'
        else:
            obj['status'] = 'error'
            obj['result'] = 'invalid user_id'
    finally:
        close_connection(conn)
    return obj


def edit_maker(id):
    """
    根据id修改厂家信息
    :param id:
    :return:
    """

    conn = get_main_connection()
    try:
        cursor = conn.cursor()
        sql = 'SELECT * FROM ebt_factory WHERE ebf_factory_id="{0}" LIMIT 1'.format(id)
        cursor.execute(sql)
        result = cursor.fetchone()
        return result
    except Exception as e:
        pass
    finally:
        close_connection(conn)


def select_maker_info(pagenum=0, pagesize=20, field='ebf_factory_id', order='DESC', maker_alias=''):
    """
    分页从ebdb_smartsys库的ebt_factory表中获取厂家信息
    :param pagenum:
    :param pagesize:
    :param field:
    :param order:
    :return:
    """
    conn = get_main_connection()
    obj = {"total": None, "result": None}

    try:
        cursor = conn.cursor()
        pagestart = pagenum * pagesize
        sql = 'select * FROM ebt_factory WHERE ebf_factory_name LIKE "%{0}%" ORDER BY {1} {2} LIMIT {3},{4}'.format(
            maker_alias, field, order, pagestart, pagesize)
        cursor.execute(sql)
        result = cursor.fetchall()

        obj["result"] = result
        # 查询总数
        scout = 'select count(ebf_factory_id) as total FROM ebt_factory WHERE ebf_factory_name LIKE "%{0}%" '.format(
            maker_alias)
        cursor.execute(scout)
        resulttotal = cursor.fetchone()
        obj["total"] = resulttotal["total"]
    finally:
        close_connection(conn)
    return obj


def select_maker_account_by_id(user_id):
    """
    通过user_id查询用户详细信息
    :param user_id:
    :return:
    """
    conn = get_main_connection()
    try:
        cursor = conn.cursor()
        sql = 'SELECT * FROM ebt_user_factory i, ebt_user n WHERE i.ebf_user_id = n.ebf_user_id AND n.ebf_user_id="{0}" LIMIT 1'.format(
            user_id)
        cursor.execute(sql)
        res = cursor.fetchone()
        return res
    except Exception as e:
        print(e)
    finally:
        close_connection(conn)


def query_data(key):
    """
    通过key查找设备的配置(ebt_protocol_conf)
    :param key: 
    :return: 
    """
    conn = get_main_connection()
    try:
        cursor = conn.cursor()
        sql = "select * from ebt_protocol_conf where ebf_pc_device_key = '%s'" %(key)
        cursor.execute(sql)
        res = cursor.fetchone()
        print(res)
        return res
    except Exception as e:
        print(e)
        print('exits')
    finally:
        close_connection(conn)


def query_ui_conf(key):
    """
    通过key查找设备的配置(ebt_protocol_conf)
    :param key: 
    :param conn
    :return: 
    """
    conn = get_main_connection()
    try:
        cursor = conn.cursor()
        sql = "select ebf_page_conf from ebt_device_page_conf where ebf_device_key='%s'" %(key)
        cursor.execute(sql)
        res = cursor.fetchone()
        return res
    except Exception as e:
        print(e)
        return 'error'
    finally:
        close_connection(conn)


def get_ui_base_conf(key, conf):
    """
    获取自定义ui配置并且保存
    :param key: 
    :param conf: 
    :return: 
    """
    conn = get_main_connection()
    isExit = query_ui_conf(key)
    if isExit:
        back_data = modify_ui_conf(key, conf, conn)
        if back_data == 'ok':
            return 'ok'
    else:
        try:
            cursor = conn.cursor()
            sql = '''insert into ebt_device_page_conf(ebf_device_key,ebf_page_conf,ebf_ui_create_date) values(%s,%s,%s)'''
            l = [[key, conf, datetime.datetime.utcnow()]]
            cursor.executemany(sql, l)
            conn.commit()
            return 'ok'
        except Exception as e:
            print(e)
        finally:
            close_connection(conn)


def modify_ui_conf(key, conf, conn):
    """
    通过key查询是否存在配置，存在时修改配置
    :param key: 
    :param conf:
    :param conn    
    :return: 
    """
    sql = "UPDATE ebt_device_page_conf SET ebf_page_conf = '%s', ebf_ui_update_date = '%s' WHERE ebf_device_key = '%s'" % (conf, datetime.datetime.utcnow(), key)
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        return 'ok'
    except Exception as e:
        print(e)
    finally:
        close_connection(conn)



