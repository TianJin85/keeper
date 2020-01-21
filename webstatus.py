# -*- encoding: utf-8 -*-
"""
@File    : webstatus.py
@Time    :  2020/1/21 17:34
@Author  : Tianjin
@Email   : tianjincn@163.com
@Software: PyCharm
"""
import asyncio
from pyppeteer import launch


class Web:
    """
    """
    browser = None
    page = None

    async def start(self):
        browser = await launch()   # 实例化浏览器
        page = await browser.newPage()
        return page

    async def close(self):
        await self.browser.close()
        return True

    async def methods(self, url):
        """
        请求网站
        :param url:请求方法
        :return:
        """
        await self.page.goto(url)




