"""
Copyright (c) 2025-now Martian Bugs All rights reserved.
Build Date: 2025-05-19
Author: Martian Bugs
Description: 后台登录
"""

from os import path
from tempfile import gettempdir
from time import sleep

from BrowserAutomationLauncher._browser import Browser
from BrowserAutomationLauncher._utils.tools import OsTools
from ddddocr import DdddOcr


class Urls:
    home = 'https://business-decision.cdfsunrise.com/'


class DataPacketUrls:
    captcha_img = (
        'https://uoc-gateway-lion.cdfsunrise.com/admin-api/system/captcha/generate'
    )
    # 图形验证码生成接口
    login = 'https://uoc-gateway-lion.cdfsunrise.com/admin-api/system/auth/sso-login'


class Login:
    def __init__(self, browser: Browser):
        self._browser = browser

    def _parse_captcha_img(self, img_path: str):
        """
        识别图形验证码

        Args:
            img_path: 验证码图片路径
        Returns:
            验证码字符串
        """

        if not path.exists(img_path):
            raise FileNotFoundError(f'验证码图片 {img_path} 不存在')

        try:
            ocr = DdddOcr(show_ad=False)
            code = None
            with open(img_path, 'rb') as f:
                code = ocr.classification(f.read())

            OsTools.file_remove(img_path)
            return code
        except Exception as e:
            raise RuntimeError(f'图形验证码识别出错: {e}') from e

    def by_password(self, username: str, password: str):
        """
        通过账号密码登录

        Args:
            username: 登录名
            password: 密码
        """

        cache_token_key = 'Y2FjaGUtdG9rZW4='

        page = self._browser.chromium.new_tab()
        page.listen.start(
            targets=DataPacketUrls.captcha_img, method='GET', res_type='XHR'
        )
        page.get(Urls.home)

        if page.local_storage(cache_token_key):
            sleep(5)
            if page.local_storage(cache_token_key):
                page.listen.stop()
                return

        captcha_datapacket = page.listen.wait(timeout=8)
        if not captcha_datapacket:
            raise TimeoutError('图形验证码获取超时')

        captcha_img_path = path.join(gettempdir(), 'cdfsunrise_login_captcha.png')
        with open(captcha_img_path, 'wb') as f:
            f.write(captcha_datapacket.response.body)

        captcha_code = self._parse_captcha_img(captcha_img_path)
        if not captcha_code or not isinstance(captcha_code, str):
            raise ValueError('图形验证码识别失败')

        username_input = page.ele('#username', timeout=3)
        if not username_input:
            raise RuntimeError('未找到 [用户名] 输入框')
        username_input.input(username, clear=True)

        password_input = page.ele('#password', timeout=1)
        if not password_input:
            raise RuntimeError('未找到 [密码] 输入框')
        password_input.input(password, clear=True)

        captcha_input = page.ele('#code', timeout=1)
        if not captcha_input:
            raise RuntimeError('未找到 [验证码] 输入框')
        captcha_input.input(captcha_code, clear=True)

        login_btn = page.ele('t:button@@text()=登 录', timeout=1)
        if not login_btn:
            raise RuntimeError('未找到 [登录] 按钮')

        page.listen.start(targets=DataPacketUrls.login, method='POST', res_type='XHR')
        login_btn.click(by_js=True)
        login_datapacket = page.listen.wait(timeout=15)
        login_datapacket_data = login_datapacket.response.body
        if isinstance(login_datapacket_data, dict) and (
            login_msg := login_datapacket_data.get('msg')
        ):
            raise RuntimeError(f'登录失败: {login_msg}')

        for _ in range(15):
            cache_token = page.local_storage(cache_token_key)
            if cache_token:
                break
            sleep(1)
        else:
            raise TimeoutError('登录超时, 未找到 cache-token 值')
