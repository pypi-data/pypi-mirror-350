"""
推广中心-账户管理数据采集器
"""

from DrissionPage import Chromium

from .._utils import Utils
from ._dict import Dictionary
from ._utils import pick__custom_date


class Urls:
    report = 'https://yingxiao.pinduoduo.com/mains/account/report'


class DataPacketUrls:
    report = (
        'yingxiao.pinduoduo.com/mms-gateway/reinhardt/account/v3/getSubAccountInvoice'
    )


class Account:
    def __init__(self, browser: Chromium):
        self._browser = browser

    def get__report__daily(
        self, begin_date: str, end_date: str, timeout: float = None, raw=False
    ):
        """
        获取财务流水日账单数据

        Args:
            begin_date: 开始日期
            end_date: 结束日期
            timeout: 超时时间, 默认为 15 秒
            raw: 是否返回原始数据, 默认为 False
        Returns:
            日账单数据字典 {'日期': 账单数据字典}
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else 15

        page = self._browser.new_tab()
        page.listen.start(targets=DataPacketUrls.report, method='POST', res_type='XHR')
        page.get(Urls.report)
        if not page.listen.wait(timeout=_timeout):
            raise TimeoutError('进入页面后获取数据包超时, 可能访问失败')

        page.listen.start(targets=DataPacketUrls.report, method='POST', res_type='XHR')
        pick__custom_date(
            begin_date=begin_date, end_date=end_date, page=self._browser.latest_tab
        )
        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise TimeoutError('修改日期后获取数据包超时')

        resp: dict = packet.response.body
        result: dict = resp.get('result')
        if not result:
            raise ValueError('在数据包中未找到 result 字段')

        if 'result' not in result:
            raise ValueError('在数据包中未找到 result.result 字段')

        result_list: list[dict] = result.get('result')
        if not isinstance(result_list, list):
            raise ValueError('在数据包中 result.result 字段不是预期的列表类型')

        records: dict[str, dict] = {}
        for item in result_list:
            if item.get('flowType') == 1:
                continue

            create_time: str = item.get('createTime')
            create_time = create_time.replace('23:59:59', '').strip()

            records[create_time] = item

        page.close()

        if raw is True:
            return records

        for date, record in records.items():
            _record = Utils.dict_mapping(record, Dictionary.account.report__daily)
            _record = Utils.dict_format__float(
                _record, fields=['交易金额'], precision=3
            )

            records[date] = _record

        return records
