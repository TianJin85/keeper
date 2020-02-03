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
import asyncio
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
        self.browser = await launch()   # 实例化浏览器
        page = await self.browser.newPage()
        try:
            res = await page.goto(url)  # 请求网站
            await page.screenshot({'path': './images/%s.png' % url.split("//")[1].replace("/", "_")})  # 截图保存到本地

            self.result["status"] = res.status
            if res.status == 200:
                pass
            elif res.status == 403:

                html = etree.HTML(await page.content())
                src_href = html.xpath('//*[@id="mainFrame"]/@src')

                if len(src_href):  # 网站备案未审核通过

                    title = html.xpath('/html/head/title/text()')
                    await page.goto(src_href[0])
                    next_page = etree.HTML(await page.content())
                    content = next_page.xpath('//p/text()')
                    self.result["title"] = title
                    self.result["err_content"] = content
            await self.browser.close()
            print(self.result)
            return self.result

        except errors.TimeoutError as e:
            raise e

    async def close(self):
        await self.browser.close()


if __name__ == '__main__':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='UTF-8')
    data_url = urllib.parse.unquote(sys.argv[1])
    web = Web()
    # ls = ["https://www.baidu.com", "https://www.cnblogs.com", "https://lxml.de/tutorial.html", "https://www.jb51.net", "http://www.xnlp.gov.cn/", "http://www.dzxn.gov.cn/"]
    for url in data_url:
        asyncio.get_event_loop().run_until_complete(web.start(url))





