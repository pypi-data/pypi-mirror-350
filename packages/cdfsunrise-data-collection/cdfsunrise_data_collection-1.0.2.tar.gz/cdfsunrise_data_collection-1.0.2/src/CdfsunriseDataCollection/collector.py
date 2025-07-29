"""
Copyright (c) 2025-now Martian Bugs All rights reserved.
Build Date: 2025-05-19
Author: Martian Bugs
Description: 数据采集器
"""

from BrowserAutomationLauncher import BrowserInitOptions, Launcher

from ._login import Login
from .goods_analysis.goods_analysis import GoodsAnalysis


class Collector:
    """采集器. 使用之前请先调用 `connect_browser` 方法连接浏览器."""

    def __init__(self):
        self._browser_launcher = Launcher()
        self._goods_analysis = None

    def connect_browser(self, port: int):
        """
        连接浏览器

        Args:
            port: 浏览器调试端口号
        """

        browser_init_options = BrowserInitOptions()
        browser_init_options.set_basic_options(port=port)
        self._browser = self._browser_launcher.init_browser(browser_init_options)

        self._login_utils = Login(self._browser)

    def login_by_password(self, username: str, password: str):
        """
        通过 账号密码 登录账号

        Args:
            username: 账号
            password: 密码
        """

        return self._login_utils.by_password(username, password)

    @property
    def goods_analysis(self):
        """商品分析模块"""

        if not self._goods_analysis:
            self._goods_analysis = GoodsAnalysis(self._browser)
        return self._goods_analysis
