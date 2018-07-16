__author__ = 'sunshine'


def print_log(*args):
    """
    打印日志到控制台
    :param args:
    :return:
    """
    print(*args)


if __name__ == '__main__':
    print_log('123', 'a', 1234)