import logging

import pymysql
import time
from conf.mysqlconf import MYSQL_HOST_SYS, MYSQL_PORT_SYS, MYSQL_USER_SYS, MYSQL_PWD_SYS, MYSQL_DB_SYS
from base.crypto import md5_en
from model.center.message import Message
from model.center.doc_ui import DocUi
import datetime
import json


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
        sql = "select * from ebt_protocol_conf where ebf_pc_device_key = '%s'" % (key)
        cursor.execute(sql)
        res = cursor.fetchone()
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
        sql = "select ebf_page_conf from ebt_device_page_conf where ebf_device_key='%s'" % (key)
        cursor.execute(sql)
        res = cursor.fetchone()
        return res
    except Exception as e:
        print(e)
        return 'error'
    finally:
        close_connection(conn)


def get_ui_base_conf(key, conf, cook_ies):
    """
    获取自定义ui配置并且保存
    :param key: 
    :param conf: 
    :return: 
    """
    conn = get_main_connection()
    isExit = query_ui_conf(key)
    if isExit:
        back_data = modify_ui_conf(key, conf, conn, cook_ies)
        if back_data == 'ok':
            return 'ok'
    else:
        try:

            Message.objects.create(message_content='UI更新', message_type=int(3), message_handler_type=int(3),
                                   device_key=key, message_sender=cook_ies, message_target=cook_ies,
                                   create_date=datetime.datetime.utcnow(), update_date=datetime.datetime.utcnow())

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


def get_ui_static_conf(key, file_path, id=0, filename='',
                       user=''):
    """
    获取自定义ui配置并且保存
    :param key:
    :param conf:
    :return:
    """

    try:
        # 插入前判断是否更新！
        # 增加message信息
        # :param message_handler_type 消息处理类型，0：无， 1：功能编辑， 2：协议编辑，3：UI编辑

        ui_obj = DocUi.objects.filter(ui_upload_id=id, ui_key=key)
        if ui_obj:
            for i in ui_obj:
                if i.ui_content:
                    print(i.ui_content)
                    print('1')
                    url_list_now = json.loads(i.ui_content)
                    url_dict = {"urll": file_path, "filename": filename, "user": user,
                                "date": time.strftime("%Y-%m-%d")}
                    url_list_now.append(url_dict)
                    url_list_now = json.dumps(url_list_now)
                    ui_obj.update(ui_content=url_list_now, ui_type='UI',
                                  update_date=datetime.datetime.utcnow())
                else:
                    print('2')
                    url_list1 = []
                    url_dict = {"urll": file_path, "filename": filename, "user": user,
                                "date": time.strftime("%Y-%m-%d")}
                    url_list1.append(url_dict)
                    url_list1 = json.dumps(url_list1)
                    ui_obj.update(ui_content=url_list1, ui_type='UI',
                                  update_date=datetime.datetime.utcnow())
            return {"code": 0, "url": file_path, "filename": filename,
                    "date": time.strftime("%Y-%m-%d"), "user": user}
        else:
            print('3')
            url_list1 = [{"urll": file_path, "filename": filename, "user": user,
                          "date": time.strftime("%Y-%m-%d")}]
            url_list1 = json.dumps(url_list1)
            DocUi.objects.create(ui_upload_id=id, ui_key=key, ui_content=url_list1, ui_type='UI',
                                 update_date=datetime.datetime.utcnow())
            return {"code": 1, "url": file_path, "filename": filename,
                    "date": time.strftime("%Y-%m-%d"), "user": user}
    except Exception as e:
        print(e)
        return {"code": 2}



def remove_up_url(key, del_id, del_filename):
    """
    删除上传的文件
    :param key:
    :param del_id:
    :param del_url:
    :return:
    """
    try:
        url_list = DocUi.objects.filter(ui_key=key, ui_upload_id=del_id)
        url_listed = ''
        for i in url_list:
            url_listed = json.loads(i.ui_content)
            for ii in url_listed:
                if del_filename in ii.values():
                    url_listed.remove(ii)
            if url_listed:
                # 删除后还有url处理
                url_listed = json.dumps(url_listed)
                DocUi.objects.filter(ui_key=key, ui_upload_id=del_id).update(ui_content=url_listed)
            else:
                # 删除后没有url了
                url_listed = ''
                DocUi.objects.filter(ui_key=key, ui_upload_id=del_id).update(ui_content=url_listed)
    except Exception as e:
        print(e)


def get_ui_base_conf(key, conf, cook_ies):
    """
    获取自定义ui配置并且保存
    :param key:
    :param conf:
    :return:
    """
    conn = get_main_connection()
    isExit = query_ui_conf(key)
    if isExit:
        back_data = modify_ui_conf(key, conf, conn, cook_ies)
        if back_data == 'ok':
            return 'ok'
    else:
        try:

            Message.objects.create(message_content='UI更新', message_type=int(3), message_handler_type=int(3),
                                   device_key=key, message_sender=cook_ies, message_target=cook_ies,
                                   create_date=datetime.datetime.utcnow(), update_date=datetime.datetime.utcnow())

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


def modify_ui_conf(key, conf, conn, cook_ies):
    """
    通过key查询是否存在配置，存在时修改配置
    :param key: 
    :param conf:
    :param conn    
    :return: 
    """
    sql = "UPDATE ebt_device_page_conf SET ebf_page_conf = '%s', ebf_ui_update_date = '%s' WHERE ebf_device_key = '%s'" % (
        conf, datetime.datetime.utcnow(), key)
    try:
        Message.objects.create(message_content='UI更新', message_type=int(3), message_handler_type=int(3), device_key=key,
                               message_sender=cook_ies, message_target=cook_ies, create_date=datetime.datetime.utcnow(),
                               update_date=datetime.datetime.utcnow())

        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

        return 'ok'
    except Exception as e:
        print(e)
    finally:
        close_connection(conn)
