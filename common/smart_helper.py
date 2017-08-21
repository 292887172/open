import logging

import pymysql

from base.connection import SysMysqlHandler
from base.crypto import md5_en


def check_user_password(user, password):
    """
    从ebdb_smartsys库的ebt_user表中校验用户名和密码只有厂商能登录，其他用户不可登录
    :param user:
    :param password:
    :return:
    """
    conn = SysMysqlHandler().conn
    obj = {"status": None, "result": None}

    try:
        cursor = conn.cursor()
        sql = 'select ebf_user_password,ebf_user_phone,ebf_user_is_forbid FROM ebt_user i, ebt_user_factory n  ' \
              ' WHERE i.ebf_user_id=n.ebf_user_id ANd ebf_user_account="{0}" LIMIT 1'.format(user)

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
    except Exception as e:
        print(e)
    finally:
        conn.close()
    return obj


def get_device_type(device_type):
    """
    从ebdb_smartsys的ebt_device表中获取device_type对应的dt_id
    然后从ebt_device_type表中根据dt_id返回对应dt_name
    :param device_type:
    :return:
    """

    conn = SysMysqlHandler().conn
    try:
        cursor = conn.cursor()
        sql = 'SELECT dt_name FROM ebt_device_type WHERE dt_id="{0}"'.format(device_type)
        # sql = 'SELECT dt_name FROM ebt_device_type WHERE dt_id="2"'
        cursor.execute(sql)
        re = cursor.fetchone()
        if re:
            return re['dt_name']
    except Exception as e:
        print(e)
        pass
    finally:
        conn.close()
    return ''


def get_device_list(device_secret):
    """
    根据key从ebdb_smartsys的ebt_device表中获取关联查询secret
    返回id,mac,时间
    :param device_secret:
    :return:
    """

    conn = SysMysqlHandler().conn
    key = device_secret[len(device_secret)-8:]
    try:
        cursor = conn.cursor()
        sql = 'SELECT ebf_device_id,ebf_device_oc_date,ebf_device_mac FROM ebt_device WHERE SUBSTRING(ebf_device_secret,-8)="{0}"'.format(key)
        cursor.execute(sql)
        re = cursor.fetchall()
        if re:
            return re
    except Exception as e:
        print(e)
        pass
    finally:
        conn.close()
    return ''


def get_factory_info(user_id):
    """
    从ebdb_smartsys的ebt_factory表中获取某厂家名称和id
    :return:
    """
    conn = SysMysqlHandler().conn
    try:
        cursor = conn.cursor()
        sql = 'SELECT ebf_factory_id FROM ebt_user_factory WHERE ebf_user_id="{0}"'.format(user_id)
        cursor.execute(sql)
        re = cursor.fetchone()
        if re:
            sql = 'SELECT ebf_factory_uid as factory_uid,ebf_factory_name as factory_name, ebf_factory_contact as phone FROM ebt_factory WHERE ' \
                  'ebf_factory_id={0}'.format(re['ebf_factory_id'])
            cursor.execute(sql)
            result = cursor.fetchone()
            return result
    except Exception as e:
        print(e)
        pass
    finally:
        conn.close()
    return ''


def get_factory_list():
    """
    从ebdb_smartsys的ebt_factory表中获取所有厂家名称和id
    :return:
    """

    conn = SysMysqlHandler().conn
    try:
        cursor = conn.cursor()
        sql = 'SELECT ebf_factory_uid as brandId,ebf_factory_name as brandName FROM ebt_factory'
        cursor.execute(sql)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(e)
        pass
    finally:
        conn.close()
    return ''


def check_factory_uuid(factory_name, factory_uuid):
    """
    从ebdb_smartsys的ebt_factory表中校验id名称和uuid
    返回为ok表示校验成功，false为校验失败
    :param factory_name:
    :param factory_uuid:
    :return: status,为ok表示校验成功，false为校验失败
    """
    conn = SysMysqlHandler().conn
    status = 'false'
    try:
        cursor = conn.cursor()
        sql = 'SELECT ebf_factory_uid as factory_uid FROM ebt_factory WHERE ebf_factory_name LIKE "%{0}%" LIMIT 1'\
            .format(factory_name)

        cursor.execute(sql)
        result = cursor.fetchone()
        if result['factory_uid'] == factory_uuid:
            status = 'ok'
        else:
            status = 'false'
    except Exception as e:
        print(e)
        status = 'false'
        pass
    finally:
        conn.close()
    return status


if __name__ == '__main__':
    r = get_factory_list()
    print(r)
