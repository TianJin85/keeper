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

import pandas as pd
import paramiko
import psutil as pu

# 远程服务参数


class Connect_server:
    ssh = None
    memory = ["T", "G", "M", "K"]

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
        # print(stdout.read().decode('utf-8'))

        resutl = [item.split() for item in stdout.readlines()]
        resutl_df = pd.DataFrame(resutl)
        _resutl_np = resutl_df.to_numpy()[1:]
        _columns = resutl_df.to_numpy()[0]

        _resutl = pd.DataFrame(_resutl_np, columns=_columns)
        print(self.resource_sum("Size", _resutl))
        self.close_server()

    def close_server(self):
        self.ssh.close()

    def resource_sum(self, columns_name, _resutl):
        USED_SUM = []
        for USED in _resutl[columns_name].to_list():
            for me in self.memory:
                if me in USED:                  # 单位换算一律换成G为单位
                    _me = USED.split(me)[0]
                    if me == "T":
                        USED_SUM.append(float(_me) * 1012)
                    elif me == "G":
                        USED_SUM.append(float(_me))
                    elif me == "M":
                        USED_SUM.append(float(_me) / 1024)
                    elif me == "K":
                        USED_SUM.append(float(_me) / (1024 * 1024))
        return sum(USED_SUM)


if __name__ == '__main__':
    conn = Connect_server(ip=Ip, username=Username, password=Password)
    conn.open_server()