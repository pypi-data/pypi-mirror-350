"""
Copyright (c) 2025-now Martian Bugs All rights reserved.
Build Date: 2025-01-17
Author: Martian Bugs
Description: 数据采集器
"""

from DrissionPage import Chromium, ChromiumOptions

from ._login import Login
from .marketing.marketing import Marketing
from .mms.mms import Mms


class Collector:
    """采集器. 使用之前请先调用 `connect_browser` 方法连接浏览器."""

    def __init__(self):
        self._mms = None
        self._marketing = None

    def connect_browser(self, port: int):
        """
        连接浏览器

        Args:
            port: 浏览器调试端口号
        """

        chrome_options = ChromiumOptions(read_file=False)
        chrome_options.set_local_port(port=port)

        self.browser = Chromium(addr_or_opts=chrome_options)

    def login(
        self,
        account: str,
        password: str,
        wait_captcha: float = None,
    ):
        """
        商家后台登录

        Args:
            account: 登录账号
            password: 登录密码
            wait_captcha: 等待验证码时间, 默认 10 分钟
        Returns:
            如果登录成功, 将返回操作的浏览器标签页对象
        """

        login_utils = Login(browser=self.browser)
        return login_utils.login(
            account=account, password=password, wait_captcha=wait_captcha
        )

    @property
    def mms(self):
        """商家后台"""

        if self._mms is None:
            self._mms = Mms(self.browser)

        return self._mms

    @property
    def marketing(self):
        """推广中心"""

        if self._marketing is None:
            self._marketing = Marketing(self.browser)

        return self._marketing
