"""
Copyright (c) 2025-now Martian Bugs All rights reserved.
Build Date: 2025-01-18
Author: Martian Bugs
Description: 推广中心数据采集模块
"""

from DrissionPage import Chromium

from .account import Account
from .report import Report


class Marketing:
    def __init__(self, browser: Chromium):
        self._browser = browser
        self._account = None
        self._report = None

    @property
    def account(self):
        """账户管理"""

        if self._account is None:
            self._account = Account(self._browser)

        return self._account

    @property
    def report(self):
        """报表数据"""

        if self._report is None:
            self._report = Report(self._browser)

        return self._report
