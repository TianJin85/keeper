# -*- encoding: utf-8 -*-
"""
@File    : get_web.py
@Time    :  2020/2/12 17:46
@Author  : Tianjin
@Email   : tianjincn@163.com
@Software: PyCharm
"""
import asyncio
import io
import sys
import urllib

from app.spider.get_status import Web

if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='UTF-8')
    data_url = urllib.parse.unquote(sys.argv[1])
    web = Web()
    asyncio.get_event_loop().run_until_complete(web.start(data_url))

    # data_url = ["http://www.jkqzs.cn/", "http://www.tzxn.gov.cn/", "http://www.wowcan.cn/", "http://boya.tooge.cn/",
    #             "http://www.gzqc.com.cn/", "www.cmfilm.cn/", "http://www.hszx.com.cn/", "http://qngz.tooge.cn/",
    #             "http://www.cgisn.com/", "www.gzph.org.cn/", "http://www.gzzxpx.cn/", "http://www.gzyouth.cn",
    #             "http://www.gzqc.com.cn/", "www.gzxkyy.com/", "http://www.likeqf.com/"]
    # for url in data_url:
    #     web = Web()
    #     asyncio.get_event_loop().run_until_complete(web.start(url))