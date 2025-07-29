import json
from base64 import b64encode
from hashlib import md5

from BrowserAutomationLauncher._utils.tools import DateTimeTools
from DrissionPage._pages.mix_tab import MixTab


def pick__date(date: str, page: MixTab):
    """
    选择指定日期

    Args:
        date: 日期字符串，格式为'YYYY-MM-DD'
        page: MixTab 页面对象
    """

    trigger_btn = page.ele(
        't:div@@class=ant-segmented-item-label@@text()=日', timeout=1
    )
    if not trigger_btn:
        raise RuntimeError('未找到日期选择按钮')
    trigger_btn.click()

    date_picker__panel = page.ele('c:div.ant-picker-panel', timeout=3)
    if not date_picker__panel:
        raise RuntimeError('未找到日期选择面板')

    target_date_btn = date_picker__panel.ele(f'c:td[title="{date}"]', timeout=1)
    if target_date_btn:
        target_date_btn.click(by_js=True)
        return

    target_year, target_month, _ = date.split('-')
    target_year_month = f'{target_year}-{target_month}'

    curr_year_ele = date_picker__panel.ele('c:button.ant-picker-year-btn', timeout=1)
    if target_year + '年' != curr_year_ele.text:
        curr_year_ele.click(by_js=True)
        target_year_btn = date_picker__panel.ele(
            f'c:td[title="{target_year}"]', timeout=2
        )
        if not target_year_btn:
            raise RuntimeError(f'未找到年份 [{target_year}] 按钮')
        target_year_btn.click(by_js=True)

        target_month_btn = date_picker__panel.ele(
            f'c:td[title="{target_year_month}"]', timeout=2
        )
        if not target_month_btn:
            raise RuntimeError(f'未找到年月 [{target_year_month}] 按钮')
        target_month_btn.click(by_js=True)
    else:
        curr_month_ele = date_picker__panel.ele(
            'c:button.ant-picker-month-btn', timeout=1
        )
        if target_month.lstrip('0') + '月' != curr_month_ele.text:
            curr_month_ele.click(by_js=True)
            target_month_btn = date_picker__panel.ele(
                f'c:td[title="{target_year_month}"]', timeout=2
            )
            if not target_month_btn:
                raise RuntimeError(f'未找到月份 [{target_month}] 按钮')
            target_month_btn.click(by_js=True)

    target_date_btn = date_picker__panel.ele(f'c:td[title="{date}"]', timeout=1)
    if not target_date_btn:
        raise RuntimeError(f'未找到日期 [{date}] 按钮')

    target_date_btn.click(by_js=True)


def generate__h_enc(token: str, api_url: str, request_body: dict | str):
    """
    生成 H-Enc 值（用于签名请求）

    Args:
        token: 固定的 token 字符串（例如 JWT）
        api_url: 完整请求 URL，比如 "https://.../base-api/xxx"
        request_body: POST 请求体（Python dict），key 顺序须和前端 JSON.stringify 保持一致
    Returns:
        (JSON 化的请求参数, H-Enc 值（32 位小写 MD5）)
    """

    path = '/' + api_url.split('/base-api/')[1]
    t_path = b64encode(path.encode('utf-8')).decode('ascii')
    json_str = (
        json.dumps(request_body, separators=(',', ':'), ensure_ascii=False)
        if isinstance(request_body, dict)
        else request_body
    )
    t_body = b64encode(json_str.encode('utf-8')).decode('ascii')
    raw_string = (
        token + t_path + t_body + DateTimeTools.date_calculate(0, pattern='%Y%m%d')
    )
    return json_str, md5(raw_string.encode('utf-8')).hexdigest()
