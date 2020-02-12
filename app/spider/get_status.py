# -*- encoding: utf-8 -*-
"""
@File    : get_status.py
@Time    :  2020/1/21 17:34
@Author  : Tianjin
@Email   : tianjincn@163.com
@Software: PyCharm
"""
import asyncio
import io
import os
import sys
import urllib

from pyppeteer import launch, errors
from lxml import etree

from app.logfile import logger
import json


class Web:
    """
    """
    browser = None
    page = None
    result = {"url": None, "status": None, "images_name": None, "err_list": {"title": None, "err_content": None}}
    images_path = None

    async def start(self, url: str):
        """
        请求网站
        :param url:
        :return:
        """
        self.browser = await launch({"userDataDir": os.path.join(os.getcwd(), "app", "spider", "DataDir")})  # 实例化浏览器
        self.page = await self.browser.newPage()
        if "http://" in url or "https://" in url:
            pass
        else:
            url = "".join(["http://", url])
        try:

            self.result["url"] = url
            res = await self.page.goto(url)  # 请求网站
            self.result["status"] = res.status

            if res.status == 200:   # 正常
                path = os.path.join(os.getcwd(), "app", "images")
                self.images_path = path+'/%s.png' % url.split("//")[1].replace("/", "")
                await self.page.screenshot({'path': self.images_path, "fullPage": True, "width": 1080, "height": 1920})  # 截图保存到本地
                self.result["images_name"] = '%s.png'%url.split("//")[1].replace("/", "")
                logger.info("网站状态正常")
            elif res.status == 403:

                html = etree.HTML(await self.page.content())
                src_href = html.xpath('//*[@id="mainFrame"]/@src')

                if len(src_href):  # 网站备案未审核通过

                    title = html.xpath('/html/head/title/text()')
                    await self.page.goto(src_href[0])
                    next_page = etree.HTML(await self.page.content())
                    content = next_page.xpath('//p/text()')
                    self.result["err_list"]["title"] = title
                    self.result["err_list"]["err_content"] = content
            await self.browser.close()
            print(json.dumps(self.result))

        except errors.TimeoutError as e:
            self.result["status"] = "Timeout"
            self.result["images_name"] = None
            await self.browser.close()
            logger.debug("请求超时:%s"%e)
            print(json.dumps(self.result))

        except errors.NetworkError as e:
            self.result["status"] = "NetworkError"
            self.result["images_name"] = None
            await self.browser.close()
            logger.debug("网络异常:%s"%e)
            print(json.dumps(self.result))

