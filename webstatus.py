# -*- encoding: utf-8 -*-
"""
@File    : webstatus.py
@Time    :  2020/1/21 17:34
@Author  : Tianjin
@Email   : tianjincn@163.com
@Software: PyCharm
"""
import sys
import io
import urllib.parse
import time
import asyncio
from urllib import request

from pyppeteer import launch, errors
from lxml import etree


class Web:
    """
    """
    browser = None
    page = None
    result = {}

    async def start(self, url: str):
        """
        请求网站
        :param url:
        :return:
        """
        self.browser = await launch({'headless': False})  # 实例化浏览器
        self.page = await self.browser.newPage()
        try:

            res = await self.page.goto(url)  # 请求网站
            await self.page.screenshot({'path': './images/%s.png' % url.split("//")[1].replace("/", "_")})  # 截图保存到本地

            self.result["status"] = res.status
            if res.status == 200:
                pass
            elif res.status == 403:

                html = etree.HTML(await self.page.content())
                src_href = html.xpath('//*[@id="mainFrame"]/@src')

                if len(src_href):  # 网站备案未审核通过

                    title = html.xpath('/html/head/title/text()')
                    await self.page.goto(src_href[0])
                    next_page = etree.HTML(await self.page.content())
                    content = next_page.xpath('//p/text()')
                    self.result["title"] = title
                    self.result["err_content"] = content
            await self.browser.close()
            return self.result

        except errors.TimeoutError as e:
            print(e)
        except errors.NetworkError as e:
            print(e)


if __name__ == '__main__':
    # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='UTF-8')
    # data_url = urllib.parse.unquote(sys.argv[1])
    web = Web()
    data_url = ["http://www.jkqzs.cn/","http://www.gzredcross.org/","http://www.wowcan.cn/","http://boya.tooge.cn/","http://www.gzqc.com.cn/","http://www.cmfilm.cn/","http://www.hszx.com.cn/","http://qngz.tooge.cn/","http://www.cgisn.com/","http://www.gzph.org.cn/","http://www.gzzxpx.cn/","http://www.gzyouth.cn","http://www.gzqc.com.cn/","http://www.gzxkyy.com/","http://www.likeqf.com/"]
    start = time.time()
    for url in data_url:
        print(asyncio.get_event_loop().run_until_complete(web.start(url)))
    end = time.time()
    print(end - start)






