import json
import socket

from conf.twistedconf import *
from util.logutil import print_log


__author__ = 'sunshine'


def connect_twisted():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(TWISTED_TIMEOUT)
    client.connect((TWISTED_HOST, TWISTED_PORT))
    return client


def connect_close(client):
    if client:
        client.close()


def send(cmd, value, remarks=""):
    """
    发送命令
    :param cmd:
    :param value:
    :param remarks:
    :return:
    """
    data = json.dumps({"msg": {"type": cmd, "value": value, "remarks": remarks}})
    if data:
        client = None
        try:
            client = connect_twisted()
            client.send(data.encode())
            result = client.recv(TWISTED_BUFFER_SIZE)
            print(result)
            if result:
                print(json.loads(result.decode()))
                return json.loads(result.decode())
        except Exception as e:
            print_log(e)
        finally:
            connect_close(client)
    return {"value": "", "status": -1, "error": "命令发送失败"}


def send_cmd(cmd):
    """
    发送完整命令
    :param cmd:
    :return:
    """
    if cmd:
        client = None
        try:
            client = connect_twisted()
            client.send(cmd.encode())
            result = client.recv(TWISTED_BUFFER_SIZE)
            print(result)
            if result:
                return result.decode()
        except Exception as e:
            print_log(e)
        finally:
            connect_close(client)
    return {"value": "", "status": -1, "error": "命令发送失败"}


if __name__ == '__main__':
    # send('sandbox', '-1|3|ACCF2362E057')
    send('sandbox', 'query_state|ACCF2362E057')