"""
Copyright (c) 2025-now Martian Bugs All rights reserved.
Build Date: 2025-01-17
Author: Martian Bugs
Description: 商家后台数据采集模块
"""

from DrissionPage import Chromium

from .customer_service import CustomerService
from .data_center import DataCenter


class Mms:
    def __init__(self, browser: Chromium):
        self._browser = browser

        self._data_center = None
        self._customer_service = None

    @property
    def data_center(self):
        """数据中心"""

        if self._data_center is None:
            self._data_center = DataCenter(self._browser)

        return self._data_center

    @property
    def customer_service(self):
        """多多客服"""

        if self._customer_service is None:
            self._customer_service = CustomerService(self._browser)

        return self._customer_service
