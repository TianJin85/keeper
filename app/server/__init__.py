# -*- encoding: utf-8 -*-
"""
@File    : __init__.py
@Time    :  2020/2/12 17:33
@Author  : Tianjin
@Email   : tianjincn@163.com
@Software: PyCharm
"""
from loguru import logger
logger.add(r"../app/logfile/get_server_resource.log", backtrace=True, diagnose=True, rotation="50 MB")
