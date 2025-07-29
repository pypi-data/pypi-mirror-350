"""
Copyright (c) 2025-now Martian Bugs All rights reserved.
Build Date: 2025-05-20
Author: Martian Bugs
Description: 商品分析模块
"""

from BrowserAutomationLauncher._browser import Browser

from .brand import Brand
from .ranking import Ranking


class GoodsAnalysis:
    def __init__(self, browser: Browser):
        self._browser = browser
        self._ranking = None
        self._brand = None

    @property
    def ranking(self):
        """商品排行数据采集"""

        if not self._ranking:
            self._ranking = Ranking(self._browser)
        return self._ranking

    @property
    def brand(self):
        """品牌分析数据采集"""

        if not self._brand:
            self._brand = Brand(self._browser)
        return self._brand
