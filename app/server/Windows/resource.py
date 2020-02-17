# -*- encoding: utf-8 -*-
"""
@File    : resource.py
@Time    :  2020/2/13 3:26
@Author  : Tianjin
@Email   : tianjincn@163.com
@Software: PyCharm
"""
import os

import paramiko

from app.server import Connect_server
from setting import on_line


class Windows:

    def __init__(self, ssh):
        self.ssh = ssh

    def command(self, command="if exist winInfo.py (echo True ) else (echo False)"):
        stdin, stdout, stderr = self.ssh.exec_command(command)
        return stdout.readlines()

    def get_path(self):

        return self.command("chdir")

    def put_file(self, sftp, path):

        remotepath = os.path.join(path, "winInfo.py")

        if on_line:
            localpath = os.path.join(os.getcwd(), "python", "app", "server", "Windows", "winInfo.py")
        else:
            localpath = os.path.join(os.getcwd(), "app", "server", "Windows", "winInfo.py")

        sftp.put(localpath, remotepath)

    def main(self):
        self.exist_file()


    






