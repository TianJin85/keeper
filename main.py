# -*- encoding: utf-8 -*-
"""
@File    : main.py
@Time    :  2020/2/6 14:30
@Author  : Tianjin
@Email   : tianjincn@163.com
@Software: PyCharm
"""
import asyncio
import time

from app.web.webstatus import Web

if __name__ == '__main__':
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='UTF-8')
    # data_url = urllib.parse.unquote(sys.argv[1])
    # web = Web()
    # # data_url = ["http://www.jkqzs.cn/", "http://www.gzredcross.org/", "http://www.wowcan.cn/","http://boya.tooge.cn/","http://www.gzqc.com.cn/","http://www.cmfilm.cn/","http://www.hszx.com.cn/","http://qngz.tooge.cn/","http://www.cgisn.com/","http://www.gzph.org.cn/","http://www.gzzxpx.cn/","http://www.gzyouth.cn","http://www.gzqc.com.cn/","http://www.gzxkyy.com/","http://www.likeqf.com/"]
    # print(asyncio.get_event_loop().run_until_complete(web.start(data_url)))

    data_url = ["http://www.jkqzs.cn/", "http://www.gzredcross.org/", "http://www.wowcan.cn/", "http://boya.tooge.cn/",
                "http://www.gzqc.com.cn/", "http://www.cmfilm.cn/", "http://www.hszx.com.cn/", "http://qngz.tooge.cn/",
                "http://www.cgisn.com/", "http://www.gzph.org.cn/", "http://www.gzzxpx.cn/", "http://www.gzyouth.cn",
                "http://www.gzqc.com.cn/", "http://www.gzxkyy.com/", "http://www.likeqf.com/"]
    start = time.time()
    for url in data_url:
        web = Web()
        print(asyncio.get_event_loop().run_until_complete(web.start(url)))
    end = time.time()
    print(end - start)