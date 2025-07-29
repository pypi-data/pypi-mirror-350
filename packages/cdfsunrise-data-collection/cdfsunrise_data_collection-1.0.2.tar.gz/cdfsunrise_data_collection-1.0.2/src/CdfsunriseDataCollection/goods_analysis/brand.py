"""
品牌分析数据采集
"""

from copy import deepcopy
from tempfile import gettempdir
from time import sleep
from typing import Callable

from BrowserAutomationLauncher import DataPacketProcessor
from BrowserAutomationLauncher._browser import Browser
from BrowserAutomationLauncher._utils.tools import DateTimeTools, DictUtils, OsTools
from DrissionPage._pages.mix_tab import MixTab

from .._types import PUB_WEB_REQUEST_HEADERS
from ._types import PostData
from ._utils import generate__h_enc, pick__date


class Urls:
    brand = 'https://business-decision.cdfsunrise.com/business_decision/analysis/brandAnalysis'


class DataPacketUrls:
    brand_info = 'https://business-decision.cdfsunrise.com/base-api/report/brand/info'
    """品牌信息数据"""
    channel_detail = (
        'https://business-decision.cdfsunrise.com/base-api/report/brand/channel'
    )
    """品牌+场域表格数据"""
    channel_detail__export = (
        'https://business-decision.cdfsunrise.com/base-api/report/brand/channel/export'
    )
    """品牌+场域表格数据导出"""


class Brand:
    def __init__(self, browser: Browser):
        self._browser = browser
        self._timeout = 15

    def __format__data_list(self, data_list: list[dict]):
        """格式化数据列表"""

        _data_list = []
        for item in deepcopy(data_list):
            temp = DictUtils.dict_format__number(item, exclude_fields=['场域'])
            temp = DictUtils.dict_format__ratio(
                temp,
                fields=['商详到达率（日均）', '加购率（日均）', '购买转化率（日均）'],
            )
            _data_list.append(temp)

        return _data_list

    def _download_report(
        self, page: MixTab, timeout: float = None, download_btn_index: int = None
    ) -> str:
        """
        下载报表

        Args:
            page: 页面对象
            timeout: 超时时间
            download_btn_index: 下载按钮的序号, 默认为 0
        Returns:
            表格文件路径
        """

        trigger_btns = page.eles('t:div@@class=rs-btn@@text()=下载为Excel', timeout=1)
        if not trigger_btns:
            raise RuntimeError('未找到 [下载为Excel] 按钮')
        trigger_btn = trigger_btns[download_btn_index or 0]
        trigger_btn.click(by_js=True)

        drawer = page.ele('c:div.ant-drawer-content', timeout=3)
        if not drawer:
            raise RuntimeError('未找到 [下载抽屉]')

        sleep(0.5)
        select_all_btn = drawer.ele(
            'c:div.ant-transfer-list-header label.ant-transfer-list-checkbox', timeout=3
        )
        if not select_all_btn:
            raise RuntimeError('未找到 [全选] 按钮')
        select_all_btn.click(by_js=True)

        sleep(0.5)
        transfer_arrow_btn = drawer.ele(
            'c:button.ant-btn span.anticon-right', timeout=1
        )
        if not transfer_arrow_btn:
            raise RuntimeError('未找到 [右箭头] 按钮')
        transfer_arrow_btn.click(by_js=True)

        download_btn = drawer.ele('t:div@@class=rs-btn@@text()=下载', timeout=1)
        if not download_btn:
            raise RuntimeError('未找到 [下载] 按钮')

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout
        mission = download_btn.click.to_download(
            save_path=gettempdir(),
            by_js=True,
            timeout=_timeout,
        )
        file_path: str = mission.wait(show=False)
        return file_path

    def get__channel_detail(self, date: str, raw=False, timeout: float = None):
        """
        获取场域表格详情数据

        Args:
            date: 日期
            raw: 为 True 则返回下载的文件路径, 否则返回表格数据
            timeout: 超时时间
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout
        page = self._browser.chromium.new_tab(Urls.brand)

        # 切换到 品牌+场域 标签页
        channel_tab = page.ele('#rc-tabs-1-tab-3', timeout=5)
        if not channel_tab:
            raise RuntimeError('未找到 [品牌+场域] 标签页')

        def wait__detail_datapacket(callback: Callable):
            page.listen.start(
                targets=DataPacketUrls.channel_detail, method='POST', res_type='XHR'
            )
            callback()
            datapacket = page.listen.wait(timeout=_timeout)
            return datapacket

        detail_datapacket = wait__detail_datapacket(
            lambda: channel_tab.click(by_js=True)
        )
        if not detail_datapacket:
            raise TimeoutError('进入页面后获取表格详情数据包超时')

        detail_datapacket__processor = DataPacketProcessor(detail_datapacket)
        detail_datapacket__data = detail_datapacket__processor.filter('?content.total')
        if not detail_datapacket__data.get('total'):
            raise ValueError('表格详情数据为空')

        is_yeasterday = DateTimeTools.date_yesterday() == date
        if not is_yeasterday and not wait__detail_datapacket(
            lambda: pick__date(date, page)
        ):
            raise RuntimeError('修改日期后获取表格详情数据包超时')

        try:
            report_file_path = self._download_report(page, download_btn_index=1)
        except Exception as e:
            raise RuntimeError(f'下载报表失败: {e}') from e

        page.close()

        if raw is True:
            return report_file_path

        data_list = OsTools.xlsx_read(file_path=report_file_path)
        OsTools.file_remove(report_file_path)

        data_list = self.__format__data_list(data_list)
        return data_list

    def get__channel_detail__by_api(
        self, begin_date: str, end_date: str, raw=False, timeout: float = None
    ):
        """
        通过 API 获取品牌+场域表格数据

        Args:
            begin_date: 开始日期
            end_date: 结束日期
            raw: 为 True 则返回下载的文件路径, 否则返回表格数据
            timeout: 超时时间
        Returns:
            表格数据或表格文件的路径
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.chromium.new_tab()
        page.listen.start(
            targets=DataPacketUrls.brand_info, method='POST', res_type='XHR'
        )
        page.get(Urls.brand)
        detail_datapacket = page.listen.wait(timeout=_timeout)
        if not detail_datapacket:
            raise TimeoutError('进入页面后获取品牌信息数据包超时')

        auth_token = detail_datapacket.request.headers.get('auth-token')
        post_data = {
            'beginDate': begin_date,
            'endDate': end_date,
            **PostData.brand_channel_export,
        }
        post_data_str, h_enc = generate__h_enc(
            auth_token, DataPacketUrls.channel_detail__export, post_data
        )
        headers = {
            **PUB_WEB_REQUEST_HEADERS,
            'H-Enc': h_enc,
            'Auth-Token': auth_token,
            'Content-Type': 'application/json',
        }

        page.change_mode('s', go=False)
        resp = page.post(
            DataPacketUrls.channel_detail__export,
            data=post_data_str,
            headers=headers,
            timeout=_timeout,
        )
        resp_data: dict = resp.json()
        if resp_data.get('code') != 20000:
            errmsg = resp_data.get('message')
            raise RuntimeError(f'表格下载出错: {errmsg}')

        download_url = resp_data.get('content')
        download_state, file_path = page.download(
            file_url=download_url,
            save_path=gettempdir(),
            file_exists='overwrite',
            timeout=_timeout,
            show_msg=False,
        )
        if download_state != 'success':
            raise RuntimeError('表格下载失败')

        page.change_mode('d', go=False)
        page.close()

        if raw is True:
            return file_path

        data_list = OsTools.xlsx_read(file_path=file_path)
        OsTools.file_remove(file_path)

        data_list = self.__format__data_list(data_list)
        return data_list
