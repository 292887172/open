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


def get_factory_info(user_id):
    """
    从ebdb_smartsys的ebt_factory表中获取所有厂家名称和id
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

def check_factory_uuid(factory_name, factory_uuid):
    """
    从ebdb_smartsys的ebt_factory表中校验id名称和uuid
    返回为ok表示校验成功，false为校验失败
    :param factory_id:
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
    r = get_factory_info('666')
    print(r['phone'])