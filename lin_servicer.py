# -*- encoding: utf-8 -*-
"""
@File    : lin_servicer.py
@Time    :  2020/2/4 10:45
@Author  : Tianjin
@Email   : tianjincn@163.com
@Software: PyCharm
"""
import io
import sys
import urllib

from app.server import Connect_server
from app.server.Linux.resource import Linux

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='UTF-8')
    ip = urllib.parse.unquote(sys.argv[1])
    username = urllib.parse.unquote(sys.argv[2])
    password = urllib.parse.unquote(sys.argv[3])

    conn = Connect_server(ip=ip, username=username, password=password)
    ssh = conn.open_server()
    linux = Linux(ssh=ssh)
    linux.get_resource()