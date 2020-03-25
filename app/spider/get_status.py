# -*- encoding: utf-8 -*-
"""
@File    : get_status.py
@Time    :  2020/1/21 17:34
@Author  : Tianjin
@Email   : tianjincn@163.com
@Software: PyCharm
"""
import os


from pyppeteer import launch, errors
from lxml import etree

from app.logfile import logger
import json

from setting import on_line



class Web:
    """
    """
    browser = None
    page = None

    images_path = None

    async def start(self, url: str):
        """
        请求网站
        :param url:
        :return:
        """
        result = {"url": None, "status": None, "images_name": None, "err_list": {"title": None, "err_content": None}}
        self.browser = await launch({"userDataDir": os.path.join(os.getcwd(), "app", "spider", "DataDir")}, headless=False)  # 实例化浏览器
        self.page = await self.browser.newPage()
        if "http://" in url or "https://" in url:
            pass
        else:
            url = "".join(["http://", url])
        try:

            result["url"] = url
            res = await self.page.goto(url)  # 请求网站
            result["status"] = res.status

            if res.status == 200:   # 正常
                if on_line:
                    self.images_path = os.path.join(os.getcwd(), "python/app", "images",
                                                    '%s.png' % url.split("//")[1].replace("/", ""))
                else:
                    self.images_path = os.path.join(os.getcwd(), "app", "images",
                                                    '%s.png' % url.split("//")[1].replace("/", ""))
                await self.page.screenshot(
                    {'path': self.images_path, "fullPage": True, "width": 1080, "height": 1920})  # 截图保存到本地

                result["images_name"] = '%s.png'%url.split("//")[1].replace("/", "")
                logger.info("网站状态正常")
            elif res.status == 403:
                if on_line:
                    self.images_path = os.path.join(os.getcwd(), "python/app", "images",
                                                    '%s.png' % url.split("//")[1].replace("/", ""))
                else:
                    self.images_path = os.path.join(os.getcwd(), "app", "images",
                                                    '%s.png' % url.split("//")[1].replace("/", ""))
                await self.page.screenshot(
                    {'path': self.images_path, "fullPage": True, "width": 1080, "height": 1920})  # 截图保存到本地

                result["images_name"] = '%s.png'%url.split("//")[1].replace("/", "")

                html = etree.HTML(await self.page.content())
                src_href = html.xpath('//*[@id="mainFrame"]/@src')

                if len(src_href):  # 网站备案未审核通过

                    title = html.xpath('/html/head/title/text()')
                    await self.page.goto(src_href[0])
                    xpat_row = await self.page.content()
                    next_page = etree.HTML(xpat_row)
                    content = next_page.xpath('//p/text()')
                    result["err_list"]["title"] = title
                    result["err_list"]["err_content"] = content
            await self.browser.close()
            print(json.dumps(result))

        except errors.TimeoutError as e:
            result["status"] = "Timeout"
            result["images_name"] = None
            await self.browser.close()
            logger.debug("请求超时:%s"%e)
            print(json.dumps(result))

        except errors.NetworkError as e:
            result["status"] = "NetworkError"
            result["images_name"] = None
            await self.browser.close()
            logger.debug("网络异常:%s"%e)
            print(json.dumps(result))


