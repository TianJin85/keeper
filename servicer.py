# -*- encoding: utf-8 -*-
"""
@File    : servicer.py
@Time    :  2020/2/4 10:45
@Author  : Tianjin
@Email   : tianjincn@163.com
@Software: PyCharm
"""
import os
import json

import paramiko
import psutil as pu

# 远程服务参数
Port = 22
Ip = '49.235.110.51'
Username = 'ubuntu'
Password = 'Tj307440205'


class Connect_server:
    ssh = None

    def __init__(self, ip, username, password, port=22):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port

    def open_server(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.ip, self.port, self.username, self.password)
        # top - b - n1
        # cat /proc/meminfo
        stdin, stdout, stderr = self.ssh.exec_command('df -h')
        ##读取信息
        print(stdout.read().decode('utf-8'))
        print(stderr.read().decode('utf-8'))

        self.close_server()

    def close_server(self):
        self.ssh.close()


if __name__ == '__main__':
    conn = Connect_server(ip=Ip, username=Username, password=Password)
    conn.open_server()