import pymysql
from conf.mysqlconf import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PWD, MYSQL_DB


def get_device_connection():
    """
    连接主数据库
    :return:
    """
    conn = pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        passwd=MYSQL_PWD,
        db=MYSQL_DB,
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
def get_device_list():
    """
    根据id修改厂家信息
    :param id:
    :return:
    """

    conn = get_device_connection()
    try:
        cursor = conn.cursor()
        sql = 'SELECT * FROM ebt_device_menu'

        cursor.execute(sql)
        result = cursor.fetchone()
        return result
    except Exception as e:
        pass
    finally:
        close_connection(conn)


