# -*- encoding: utf-8 -*-
"""
@File    : winInfo.py
@Time    :  2020/2/15 12:14
@Author  : Tianjin
@Email   : tianjincn@163.com
@Software: PyCharm
"""
import json
import psutil as pu
import math

import pandas as pd


class WinInfo:

    def __init__(self):
        self.result = {
            "cpu": {"total": None, "percent": None},
            "disk": {"total": None, "use": None, "residue": None, "percent": None},
            "memory": {"total": None, "use": None, "residue": None, "percent": None}
        }

    def get_info(self):
        self.get_cpu()
        self.get_memory()
        self.get_disk()
        print(json.dumps(self.result))

    def get_cpu(self):
            self.result["cpu"]["totle"] = pu.cpu_count()
            self.result["cpu"]["percent"] = pu.cpu_percent(interval=1)

    def get_disk(self):
        disk_list = []

        for index, item in enumerate(pu.disk_partitions()):

            total = pu.disk_usage(item.device).total/math.pow(1024, 3)
            used = pu.disk_usage(item.device).used/math.pow(1024, 3)
            free = pu.disk_usage(item.device).free/math.pow(1024, 3)
            percent = pu.disk_usage(item.device).percent
            disk_list.append([total, used, free, percent])

        df = pd.DataFrame(disk_list, columns=["total", "used", "free", "percent"])
        self.result["disk"]["total"] = df.sum().total
        self.result["disk"]["use"] = df.sum().used
        self.result["disk"]["residue"] = df.sum().free
        self.result["disk"]["percent"] = df.sum().used/df.sum().total

    def get_memory(self):
        total, available, percent, used, free = pu.virtual_memory()
        self.result["memory"]["total"] = total/math.pow(1024, 3)
        self.result["memory"]["use"] = used/math.pow(1024, 3)
        self.result["memory"]["residue"] = available/math.pow(1024, 3)
        self.result["memory"]["percent"] = percent


if __name__ == '__main__':
    win = WinInfo()
    win.get_info()