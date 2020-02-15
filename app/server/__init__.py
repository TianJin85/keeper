# -*- encoding: utf-8 -*-
"""
@File    : __init__.py
@Time    :  2020/2/12 17:33
@Author  : Tianjin
@Email   : tianjincn@163.com
@Software: PyCharm
"""
import paramiko
from loguru import logger

logger.add(r"../app/logfile/get_server_resource.log", backtrace=True, diagnose=True, rotation="50 MB")


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
        try:

            self.ssh.connect(self.ip, self.port, self.username, self.password)
        except paramiko.ssh_exception.AuthenticationException as e:
            print(e)
        except TimeoutError as e:
            print(e)
        except paramiko.ssh_exception.SSHException as e:
            print(e)

        return self.ssh

    def close_server(self):
        self.ssh.close()


class Connect_sftp:

    sftp = None
    transport = None

    def __init__(self, ip, username, password, port=22):
        self.ip = ip
        self.username = username
        self.password = password
        self.port = port

    def conn_sftp(self):
        try:
            self.transport = paramiko.Transport((self.ip, 22))
            self.transport.connect(username=self.username, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except paramiko.ssh_exception.AuthenticationException as e:
            print(e)
        except TimeoutError as e:
            print(e)
        except paramiko.ssh_exception.SSHException as e:
            print(e)
        return self.sftp

    def close_sftp(self):
        self.transport.close()