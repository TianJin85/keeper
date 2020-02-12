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
from secure import Ip, Username, Password


class Connect_server:
    ssh = None
    memory = ["T", "G", "M", "K"]
    result = {
        "disk": {"磁盘大小": None, "使用大小": None, "未用大小": None, "使用率": None},
        "memory": {"内存总量": None, "使用内存": None, "空闲内存": None, "使用率": None },
        "cpu": {"用户占用": None, "内核占用": None, "空闲空间": None, "使用率": None}
    }

    def __init__(self, ip, username, password, port=22):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port

    def open_server(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:

            self.ssh.connect(self.ip, self.port, self.username, self.password)
            self.get_resource()
        except paramiko.ssh_exception.AuthenticationException as e:
            print(e)
        except TimeoutError as e:
            print(e)
        except paramiko.ssh_exception.SSHException as e:
            print(e)

        # top - b - n1
        # cat /proc/meminfo

    def get_resource(self):
        """

        :return:
        """
        # Filesystem
        # Size
        # Used
        # Avail
        # Use % Mounted
        # on

        # 获取磁盘信息
        resutl_disk = self.get_disk("df -h")
        size_disk = self.resource_sum("Size", resutl_disk)
        used_disk = self.resource_sum("Used", resutl_disk)
        avail_disk = self.resource_sum("Avail", resutl_disk)
        use_list = []
        for item in resutl_disk["Use%"].to_list():
            use = int(item.replace("%", ""))
            use_list.append(use)
        use_disk = sum(use_list)
        self.result["disk"]["磁盘大小"] = size_disk
        self.result["disk"]["使用大小"] = avail_disk
        self.result["disk"]["未用大小"] = used_disk
        self.result["disk"]["使用率"] = use_disk
        # 获取cpu信息以及内存信息
        cpu_memory = self.get_memory_cup()

        self.dispose_memory(cpu_memory)
        self.dispose_cpu(cpu_memory)

        print(json.dumps(self.result))

        self.close_server()

    def get_memory_cup(self):
        """

        :return:
        """

        stdin, stdout, stderr = self.ssh.exec_command("top - b - n1")
        cpu_memory = stdout.readlines()
        return cpu_memory

    def dispose_cpu(self, cpu_message):
        cup = cpu_message[2].split(",")    # 获取CPU信息

        us = cup[0].split(":")[1]

        # ['%Cpu(s):', '0.7 us,', '0.5 sy,', '0.0 ni, 98.5 id,', '0.2 wa,', '0.0 hi,', '0.0 si,', '0.0 st\n']
        # ['Cpu(s):', '0.0%us,', '0.0%sy,', '0.0%ni, 99.9%id,', '0.0%wa,', '0.0%hi,', '0.0%si,', '0.0%st\n']
        if "us" in us:
            us = us.replace("us", "")
            if "%" in us:
                us = us.replace("%", "")
            us = float(us)

        sy = cup[1]

        if "sy" in sy:
            sy = sy.replace("sy", "")
            if "%" in sy:
                sy = sy.replace("%", "")
            sy = float(sy)
        id = cup[3]
        if "id" in id:
            id = id.replace("id", "")

            if "%" in id:
                id = id.replace("%", "")
            id = float(id)

        ur = 100 - id
        self.result["cpu"]["用户占用"] = us
        self.result["cpu"]["内核占用"] = sy
        self.result["cpu"]["空闲空间"] = id
        self.result["cpu"]["使用率"] = ur

    def dispose_memory(self, cpu_message):
        # ['Mem:   8174436k total', '  1942672k used', '  6231764k free', '   401896k buffers\n']
        # ['KiB Mem :  1009152 total', '    88552 free', '   595688 used', '   324912 buff/cache\n']
        memory = cpu_message[3].split(",")   # 获取内存
        for index, item in enumerate(memory):
            if "total" in item:
                total = memory[index].split(":")[1]
                if "k total" in total:
                    total = total.replace("k total", "")
                elif "total" in total:
                    total = total.replace("total", "")
                total = float(total)/(1024 * 1024)
            elif "used" in item:
                used = memory[index]
                if "k used" in used:
                    used = used.replace("k used", "")
                elif "sed" in used:
                    used = used.replace("used", "")
                used = float(used)/(1024*1024)
            elif "free" in item:
                free = memory[index]
                if "k free" in free:
                    free = free.replace("k free", "")
                elif "free" in free:
                    free = free.replace("free", "")

                free = float(free)/(1024*1024)
        usage_rate = total/free
        self.result["memory"]["内存总量"] = total
        self.result["memory"]["使用内存"] = used
        self.result["memory"]["空闲内存"] = free
        self.result["memory"]["使用率"] = usage_rate
        return True

    def get_disk(self, command: str):
        """
        提交命令到服务器
        :param command:命令
        :return: __resutl 数据
        """
        stdin, stdout, stderr = self.ssh.exec_command(command)
        #读取信息
        # print(stdout.read().decode('utf-8'))

        resutl = [item.split() for item in stdout.readlines()]
        resutl_df = pd.DataFrame(resutl)
        _resutl_np = resutl_df.to_numpy()[1:]
        _columns = resutl_df.to_numpy()[0]

        _resutl = pd.DataFrame(_resutl_np, columns=_columns)

        return _resutl

    def close_server(self):
        self.ssh.close()

    def resource_sum(self, columns_name, _resutl):
        """
        数据单位换算
        :param columns_name:列名
        :param _resutl: 数据
        :return:以G为单位的数据
        """
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