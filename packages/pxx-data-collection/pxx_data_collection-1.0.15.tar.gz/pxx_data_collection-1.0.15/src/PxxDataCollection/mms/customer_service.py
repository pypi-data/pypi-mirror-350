"""
商家后台-多多客服数据采集器
"""

from DrissionPage import Chromium

from .._utils import Utils
from ._dict import Dictionary
from ._utils import get__shop_name, pick__custom_date_range


class Urls:
    service = 'https://mms.pinduoduo.com/mms-chat/overview/service'
    sales = 'https://mms.pinduoduo.com/mms-chat/overview/marketing'
    performance = 'https://mms.pinduoduo.com/mms-chat/overview/merchant'
    """客服绩效数据页面"""


class DataPacketUrls:
    service__overview = 'mms.pinduoduo.com/desert/stat/mallServiceOverviewData'
    sales__overview = 'mms.pinduoduo.com/desert/stat/mallSalesOverviewData'
    performance__live__overview = 'mms.pinduoduo.com/chats/csReport/overview'
    """客服绩效实时数据概览接口"""


class ApiUrls:
    performance__report__download = (
        'https://mms.pinduoduo.com/chats/csReportDetail/download'
    )
    """客服绩效报表下载接口"""


class CustomerService:
    def __init__(self, browser: Chromium):
        self._browser = browser
        self._timeout = 15

    def get__service__overview(self, date: str, timeout: float = None, raw=False):
        """
        [多多客服-客服数据-服务数据概览] 数据获取
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()

        page.listen.start(
            targets=DataPacketUrls.service__overview, method='POST', res_type='Fetch'
        )
        page.get(Urls.service)
        if not page.listen.wait(timeout=_timeout):
            raise TimeoutError('首次进入页面获取数据包超时')

        page.listen.start(
            targets=DataPacketUrls.service__overview, method='POST', res_type='Fetch'
        )
        if date == Utils.date_yesterday():
            yesterday_btn_ele = page.ele('t:button@@text()=近1天', timeout=3)
            if not yesterday_btn_ele:
                raise ValueError('未找到 [近1天] 按钮')

            yesterday_btn_ele.click(by_js=True)
        else:
            pick__custom_date_range(begin_date=date, end_date=date, page=page)

        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise TimeoutError('获取数据包超时')

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('在数据包中未找到 result 字段')

        result: dict = resp.get('result')
        if not isinstance(result, dict):
            raise ValueError('数据包中的 result 字段非预期的 dict 类型')

        page.close()

        if raw is True:
            return result

        record = Utils.dict_mapping(
            result, Dictionary.customer_service.service__overview
        )
        record = Utils.dict_format__round(
            record, fields=['平均人工响应时长'], precision=0
        )
        record = Utils.dict_format__ratio(record, fields=['3分钟人工回复率'])

        return record

    def get__sales__overview(self, date: str, timeout: float = None, raw=False):
        """
        [多多客服-客服数据-销售数据概览] 数据获取
        - 只能获取前3天的数据, 例如 18 号只能获取 15 号的数据
        - 如果获取的日期大于3天前, 将返回空数据
        """

        min_date = Utils.date_calculate(days=3)
        if Utils.date_diff_days(date, min_date) > 0:
            return

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.sales__overview, method='POST', res_type='Fetch'
        )
        page.get(Urls.sales)
        if not page.listen.wait(timeout=_timeout):
            raise TimeoutError('首次进入页面获取数据包超时')

        page.listen.start(
            targets=DataPacketUrls.sales__overview, method='POST', res_type='Fetch'
        )
        if date == min_date:
            # 如果指定的日期刚好等于 3 天前的日期, 则可以直接点击近 1 天按钮
            quick_btn_ele = page.ele('t:button@@text()=近1天', timeout=3)
            if not quick_btn_ele:
                raise ValueError('未找到 [近1天] 按钮')

            quick_btn_ele.click(by_js=True)
        else:
            pick__custom_date_range(begin_date=date, end_date=date, page=page)

        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise TimeoutError('获取数据包超时')

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('在数据包中未找到 result 字段')

        result: dict = resp.get('result')
        if not isinstance(result, dict):
            raise ValueError('数据包中的 result 字段非预期的 dict 类型')

        page.close()

        if raw is True:
            return result

        record = Utils.dict_mapping(result, Dictionary.customer_service.sales__overview)
        record = Utils.dict_format__ratio(record, fields=['询单转化率'])
        record = Utils.dict_format__round(record, fields=['询单转化率'])

        return record

    def download__performance__detail(
        self,
        date: str | list[str],
        save_path: str,
        save_name: str,
        timeout: float = None,
        download_timeout: float = None,
        open_page=False,
        get_shop_name=False,
    ) -> tuple[str | None, str] | str:
        """
        下载客服绩效数据详情表单文件

        Args:
            download_timeout: 下载超时时间, 默认 120 秒
            open_page: 是否打开页面, 如果为 False 则使用当前激活的页面
            get_shop_name: 是否获取店铺名称, 默认为 False
        Returns:
            - 如果 get_shop_name 为 True 则返回 (店铺名称, 下载的文件路径)
            - 否则, 仅返回 下载的文件路径
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout
        _download_timeout = (
            download_timeout if isinstance(download_timeout, (int, float)) else 120
        )

        page = (
            self._browser.new_tab() if open_page is True else self._browser.latest_tab
        )
        if open_page is True:
            page.listen.start(
                targets=DataPacketUrls.performance__live__overview,
                method='GET',
                res_type='Fetch',
            )
            page.get(Urls.performance)
            if not page.listen.wait(timeout=_timeout):
                raise TimeoutError('首次进入页面获取数据超时, 可能页面访问失败')

        if not page.ele('t:a@@text()=下载表单', timeout=3):
            raise RuntimeError('未找到 [下载表单] 按钮')

        page.change_mode('s', go=False)

        date_range = date
        if isinstance(date, str):
            date_range = [date, date]

        starttime, endtime = [Utils.date_to_timestamp(date) for date in date_range]
        query_data = {
            'starttime': starttime,
            'endtime': endtime,
            'csRemoveRefundSalesAmountGray': True,
        }

        if not page.get(ApiUrls.performance__report__download, params=query_data):
            raise RuntimeError('报表下载接口请求失败')

        response = page.response.json()
        if 'result' not in response:
            raise ValueError('数据包未找到 result 字段')

        result = response.get('result')
        if not isinstance(result, str):
            raise ValueError('数据包中的 result 字段非预期的 str 类型')

        status, file_path = page.download(
            file_url=result,
            save_path=save_path,
            rename=save_name,
            file_exists='overwrite',
            show_msg=False,
            timeout=_download_timeout,
        )

        if status != 'success':
            raise RuntimeError('报表下载失败')

        result = file_path

        if get_shop_name is True:
            shop_name = get__shop_name(page, throw_exception=False)
            result = shop_name, file_path

        if open_page is True:
            page.close()

        return result
