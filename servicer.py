# -*- encoding: utf-8 -*-
"""
@File    : servicer.py
@Time    :  2020/2/4 10:45
@Author  : Tianjin
@Email   : tianjincn@163.com
@Software: PyCharm
"""
import io
import sys
import urllib

from app.server.Linux.resource import Connect_server

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='UTF-8')
    data = dict(urllib.parse.unquote(sys.argv[1]))

    conn = Connect_server(ip=data["ip"], username=data["username"], password=data["password"])
    conn.open_server()
