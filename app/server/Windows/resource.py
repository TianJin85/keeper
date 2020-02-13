# -*- encoding: utf-8 -*-
"""
@File    : resource.py
@Time    :  2020/2/13 3:26
@Author  : Tianjin
@Email   : tianjincn@163.com
@Software: PyCharm
"""
import paramiko


class Windows:

    def __init__(self, ssh):
        self.ssh = ssh

    def get_cpu(self):
        pass

    def get_disk(self):
        pass

    def get_memory(self):
        pass
