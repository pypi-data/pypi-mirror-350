"""
商家后台-数据中心数据采集器
"""

from functools import partial
from random import uniform
from time import sleep
from typing import Callable

from DrissionPage import Chromium
from PxxFontDecrypt.decrypt import FontDecrypter

from .._utils import Utils
from ._dict import Dictionary
from ._utils import (
    Pagination,
    download__font,
    pick__custom_date,
    pick__custom_date_range,
)


class Urls:
    flow_plate = (
        'https://mms.pinduoduo.com/sycm/search_data/plate?dateFlag=5&day={date}'
    )
    flow_plate__day30 = 'https://mms.pinduoduo.com/sycm/search_data/plate?dateFlag=2'
    goods_effect = 'https://mms.pinduoduo.com/sycm/goods_effect?msfrom=mms_sidenav'
    transaction__overview = (
        'https://mms.pinduoduo.com/sycm/stores_data/operation?dateFlag=5&day={date}'
    )
    service__comment = (
        'https://mms.pinduoduo.com/sycm/goods_quality/comment?dateFlag=5&day={date}'
    )
    service__exp = 'https://mms.pinduoduo.com/sycm/goods_quality/help'
    service__detail = (
        'https://mms.pinduoduo.com/sycm/goods_quality/detail?dateFlag=5&day={date}'
    )


class DataPacketUrls:
    flow_plate__overview = 'mms.pinduoduo.com/sydney/api/mallFlow/queryMallFlowOverView'
    flow_plate__overview_list = (
        'mms.pinduoduo.com/sydney/api/mallFlow/queryMallFlowOverViewList'
    )
    goods_effect__overview = (
        'mms.pinduoduo.com/sydney/api/goodsDataShow/queryGoodsPageOverView'
    )
    goods_effect__detail = '/sydney/api/goodsDataShow/queryGoodsDetailVOListForMMS'
    transaction__overview = 'mms.pinduoduo.com/sydney/api/mallTrade/queryMallTradeList'
    service__comment__overview = (
        'mms.pinduoduo.com/sydney/api/saleQuality/queryMallDsrVO'
    )
    service__exp__overview = (
        'mms.pinduoduo.com/sydney/api/mallService/getMallServeScoreV2'
    )
    service__detail__overview = (
        'mms.pinduoduo.com/sydney/api/saleQuality/querySaleQualityDetailInfo'
    )


class DataCenter:
    def __init__(self, browser: Chromium):
        self._browser = browser
        self._timeout = 15

    def get__flow_plate__overview(
        self, date: str, timeout: float = None, raw=False
    ) -> dict | None:
        """
        [流量数据-流量看板-数据概览] 数据获取

        Args:
            date: 日期，格式：YYYY-MM-DD
            timeout: 超时时间，默认 15 秒
            raw: 是否返回原始数据，默认 False
        Returns:
            看板数据
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.flow_plate__overview_list,
            method='POST',
            res_type='Fetch',
        )

        uri = Urls.flow_plate.format(date=date)
        page.get(uri)

        packet = page.listen.wait(timeout=_timeout)

        page.close()

        if not packet:
            raise TimeoutError('数据包获取超时')

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('在数据包中未找到 result 字段')

        result: list[dict] = resp.get('result')
        if not result or not isinstance(result, list):
            raise TypeError('数据包中的 result 字段空的或不是预期的 list 类型')

        target_record: dict = next(
            filter(lambda x: x.get('statDate') == date, result), None
        )
        if not target_record or raw is True:
            return target_record

        record = Utils.dict_mapping(
            target_record, Dictionary.data_center.flow_plate__overview
        )
        record = Utils.dict_format__ratio(record, fields=['成交转化率'])
        record = Utils.dict_format__round(
            record, fields=['成交转化率', '客单价', '成交UV价值']
        )

        return record

    def get__flow_plate__overview_day30(
        self, timeout: float = None, raw=False, open_page=True
    ):
        """
        获取近 30 天的流量数据概览

        Args:
            timeout: 超时时间，默认 15 秒
            raw: 是否返回原始数据，默认 False
            open_page: 是否打开新页面，默认 True
        Returns:
            近 30 天的流量数据概览
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = (
            self._browser.new_tab() if open_page is True else self._browser.latest_tab
        )
        page.listen.start(
            targets=DataPacketUrls.flow_plate__overview + '$',
            method='POST',
            res_type='Fetch',
            is_regex=True,
        )
        page.get(Urls.flow_plate__day30)
        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise TimeoutError('数据获取超时')

        resp = packet.response.body
        if not isinstance(resp, dict):
            raise TypeError('数据非预期的 dict 类型')

        if 'result' not in resp:
            raise ValueError('数据中未找到 result 字段')

        result = resp['result']
        if not isinstance(result, dict):
            raise TypeError('数据中的 result 字段非预期的 dict 类型')

        # 下载加密字体
        font_filepath = download__font(page=page)
        font_decrypter = FontDecrypter(font_path=font_filepath)

        record = {
            k: font_decrypter.decrypt(v)
            for k, v in result.items()
            if isinstance(v, str)
        }

        if open_page is True:
            page.close()

        if raw is True:
            return record

        record = Utils.dict_mapping(record, Dictionary.data_center.flow_plate__overview)
        record = Utils.dict_format__strip(record, fields=['成交转化率'], suffix=['%'])
        record = Utils.dict_format__number(record)

        return record

    def get__goods_effect__overview(self, date: str, timeout: float = None, raw=False):
        """
        [商品数据-商品概况] 数据获取
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.goods_effect__overview + '$',
            is_regex=True,
            method='POST',
            res_type='Fetch',
        )
        page.get(Urls.goods_effect)
        if not page.listen.wait(timeout=_timeout):
            raise TimeoutError('首次进入页面获取数据包超时')

        page.listen.start(
            targets=DataPacketUrls.goods_effect__overview + '$',
            is_regex=True,
            method='POST',
            res_type='Fetch',
        )
        if Utils.date_yesterday() == date:
            yesterday_btn = page.ele('t:label@@text()=昨日', timeout=2)
            yesterday_btn.click(by_js=True)
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
            raise TypeError('数据包中的 result 字段不是预期的 dict 类型')

        # 下载加密字体
        font_filepath = download__font(page=page)
        font_decrypter = FontDecrypter(font_path=font_filepath)

        record: dict[str, str] = {}
        for field, value in result.items():
            if not isinstance(value, str):
                continue

            record[field] = font_decrypter.decrypt(value)

        page.close()

        if raw is True:
            return record

        record = Utils.dict_mapping(
            record, Dictionary.data_center.goods_effect__overview
        )
        record = Utils.dict_format__strip(record, fields=['成交转化率'], suffix=['%'])
        record = Utils.dict_format__number(record)

        return record

    def get__goods_effect__detail(
        self,
        goods_ids: list[str],
        date: str,
        timeout: float = None,
        set_max_page=False,
        raw=False,
    ):
        """
        [商品数据-商品明细] 数据获取

        Args:
            goods_ids: 商品 ID 列表
            date: 日期，格式：YYYY-MM-DD
            timeout: 超时时间，默认 15 秒
            set_max_page: 是否设置最大页码，默认 False
            raw: 是否返回原始数据，默认 False
        Returns:
            商品明细数据 {'商品ID': {'字段1': '值1', '字段2': '值2',...}}
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.goods_effect__detail,
            method='POST',
            res_type='Fetch',
        )
        page.get(Urls.goods_effect)
        if not page.listen.wait(timeout=_timeout):
            raise TimeoutError('首次进入页面获取数据包超时')

        if not page.ele(
            't:span@@class^goods-content_tabLabel@@text()=商品明细', timeout=2
        ):
            raise RuntimeError('未找到商品明细选项卡')

        tab_container = page.ele('c:div[class^=goods-content_goodsContent]', timeout=5)
        if not tab_container:
            raise RuntimeError('未找到商品明细数据容器')

        # ========== 输入多个商品ID ==========
        goods_ids_str = ','.join([str(goods_id) for goods_id in goods_ids])
        goods_id_input = tab_container.ele(
            't:input@placeholder^请输入商品ID查询', timeout=2
        )
        if not goods_id_input:
            raise RuntimeError('未找到商品ID输入框')

        goods_id_input.input(goods_ids_str, clear=True)
        # ========== 输入多个商品ID ==========

        packet = None
        page.listen.start(
            targets=DataPacketUrls.goods_effect__detail,
            method='POST',
            res_type='Fetch',
        )
        if Utils.date_yesterday() == date:
            # 若获取昨日数据，则直接点击 [昨日] 按钮
            yesterday_btn = tab_container.ele('t:label@@text()=昨日', timeout=2)
            yesterday_btn.click(by_js=True)
        else:
            pick__custom_date(date=date, page=page, container=tab_container)

        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise RuntimeError('获取商品明细数据超时')

        # ========== 修改页码最大值 ==========
        if set_max_page is True:
            page.listen.start(
                targets=DataPacketUrls.goods_effect__detail,
                method='POST',
                res_type='Fetch',
            )
            if Pagination.set__max_page_size(page=page) is False:
                page.listen.stop()
            else:
                packet = page.listen.wait(timeout=_timeout)
                if not packet:
                    raise RuntimeError('修改页码后获取商品明细数据超时')
        # ========== 修改页码最大值 ==========

        resp: dict = packet.response.body
        result: dict = resp.get('result')
        if not result:
            raise ValueError('数据包中未找到 result 字段')

        goods_detail_list: list[dict] = result.get('goodsDetailList')
        if not goods_detail_list or not isinstance(goods_detail_list, list):
            raise ValueError('数据包中未找到 result.goodsDetailList 字段或非 list 格式')

        # 下载加密字体
        font_filepath = download__font(page=page)
        font_decrypter = FontDecrypter(font_path=font_filepath)

        records: dict[str, dict] = {}
        for item in goods_detail_list:
            for field, value in item.items():
                if not isinstance(value, str):
                    continue

                item[field] = font_decrypter.decrypt(value)

            records[str(item.get('goodsId'))] = item

        if raw is True:
            return records

        for goods_id, record in records.items():
            _record = Utils.dict_mapping(
                record, Dictionary.data_center.goods_effect__detail
            )
            _record = Utils.dict_format__strip(
                _record, fields=['成交转化率', '下单率', '成交率'], suffix=['%']
            )
            _record = Utils.dict_format__number(_record)
            _record = Utils.dict_format__round(_record)
            records[goods_id] = _record

        page.close()

        return records

    def get__goods_effect__detail__all(
        self,
        date: str | list[str],
        timeout: float = None,
        raw=False,
        open_page=True,
        interval_sleep_range: tuple | list = None,
    ):
        """
        [商品数据-商品明细] 数据获取-全部商品

        Args:
            date: 日期，格式：YYYY-MM-DD
            timeout: 超时时间，默认 15 秒
            raw: 是否返回原始数据，默认 False
            open_page: 是否打开新页面，默认 True
            interval_sleep_range: 间隔休眠时间范围，默认 (2.5, 3.5)
        Returns:
            商品明细数据 {日期: {商品ID: {字段: 值, ...}}}
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout
        _interval_sleep_range = (
            interval_sleep_range
            if isinstance(interval_sleep_range, (tuple, list))
            else (2.5, 3.5)
        )

        page = (
            self._browser.new_tab() if open_page is True else self._browser.latest_tab
        )

        def wait__goods_packet(callback: Callable, action: str, parse=False):
            """等待商品明细数据包"""
            page.listen.start(
                targets=DataPacketUrls.goods_effect__detail,
                method='POST',
                res_type='Fetch',
            )
            if callback() is False:
                page.listen.stop()
                return

            packet = page.listen.wait(timeout=_timeout)
            if not packet:
                raise RuntimeError(f'{action}: 获取商品明细数据超时')

            if parse is not True:
                return packet

            resp = packet.response.body
            if not isinstance(resp, dict):
                raise TypeError(f'{action}: 数据包非预期的 dict 类型')

            result: dict = resp['result']
            if not result:
                raise ValueError(f'{action}: 数据包中未找到 result 字段')

            if 'goodsDetailList' not in result:
                raise ValueError(
                    f'{action}: 数据包中未找到 result.goodsDetailList 字段'
                )

            goods_detail_list: list[dict] = result['goodsDetailList']
            if not isinstance(goods_detail_list, list):
                raise TypeError(
                    f'{action}: 数据包的 result.goodsDetailList 字段非预期 list 格式'
                )

            return goods_detail_list

        wait__goods_packet(lambda: page.get(Urls.goods_effect), '进入页面')

        if not page.ele(
            't:span@@class^goods-content_tabLabel@@text()=商品明细', timeout=2
        ):
            raise RuntimeError('未找到商品明细选项卡')

        list_container = page.ele('c:div[class^=goods-content_goodsContent]', timeout=5)
        if not list_container:
            raise RuntimeError('未找到商品明细数据容器')

        wait__goods_packet(
            lambda: Pagination.set__max_page_size(page=page), '修改最大页码'
        )

        font_filepath = download__font(page=page)
        font_decrypter = FontDecrypter(font_path=font_filepath)

        def get__goods_data(date):
            """获取商品数据"""
            goods_detail_list = wait__goods_packet(
                lambda: pick__custom_date(
                    date=date, page=page, container=list_container
                ),
                action=f'选择日期 {date}',
                parse=True,
            )
            if not goods_detail_list:
                return

            goods_detail_list__hub = [*goods_detail_list]
            while True:
                next_btn = Pagination.next(page=page, click=False)
                if not next_btn:
                    break

                sleep(uniform(*_interval_sleep_range))
                goods_detail_list: list[dict] = wait__goods_packet(
                    partial(next_btn.click, by_js=True),
                    action=f'日期 {date} 下一页',
                    parse=True,
                )
                if not goods_detail_list:
                    break

                goods_detail_list__hub.extend(goods_detail_list)

            return {
                str(goods.get('goodsId')): goods for goods in goods_detail_list__hub
            }

        begin_date, end_date = date if isinstance(date, list) else [date, date]
        date_list = Utils.date_range(begin_date, end_date)
        goods_datas: dict[str, dict[str, dict]] = {}
        date_list__size = len(date_list)
        for i, date in enumerate(date_list, 1):
            try:
                goods_data = get__goods_data(date)
                if not goods_data:
                    continue

                goods_datas[date] = goods_data
            except Exception as e:
                print(f'- 出错了: {e}')
                break

            if date_list__size > i:
                sleep(uniform(*_interval_sleep_range))

        if open_page is True:
            page.close()

        if raw is True:
            return goods_datas

        records: dict[str, dict[str, dict]] = {}
        for date, goods_data in goods_datas.items():
            record: dict[str, dict] = {}
            for goods_id, item in goods_data.items():
                _record = Utils.dict_mapping(
                    item, Dictionary.data_center.goods_effect__detail
                )
                _record = Utils.dict_format__strip(
                    _record, fields=['成交转化率', '下单率', '成交率'], suffix=['%']
                )
                for k, v in _record.items():
                    if not isinstance(v, str):
                        continue
                    _record[k] = font_decrypter.decrypt(v)

                _record = Utils.dict_format__number(_record)
                _record = Utils.dict_format__round(_record)

                record[goods_id] = _record

            records[date] = record

        return records

    def get__goods_effect__detail__all_day30(
        self,
        timeout: float = None,
        raw=False,
        open_page=True,
        interval_sleep_range: tuple | list = None,
    ):
        """
        [商品数据-商品明细] 近30天数据获取-全部商品

        Args:
            timeout: 超时时间，默认 15 秒
            raw: 是否返回原始数据，默认 False
            open_page: 是否打开新页面，默认 True
            interval_sleep_range: 间隔休眠时间范围，默认 (2.5, 3.5)
        Returns:
            商品明细数据 {商品ID: {字段: 值, ...}}
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout
        _interval_sleep_range = (
            interval_sleep_range
            if isinstance(interval_sleep_range, (tuple, list))
            else (2.5, 3.5)
        )

        page = (
            self._browser.new_tab() if open_page is True else self._browser.latest_tab
        )

        def wait__goods_packet(callback: Callable, action: str, parse=False):
            """等待商品明细数据包"""
            page.listen.start(
                targets=DataPacketUrls.goods_effect__detail,
                method='POST',
                res_type='Fetch',
            )
            if callback() is False:
                page.listen.stop()
                return

            packet = page.listen.wait(timeout=_timeout)
            if not packet:
                raise RuntimeError(f'{action}: 获取商品明细数据超时')

            if parse is not True:
                return packet

            resp = packet.response.body
            if not isinstance(resp, dict):
                raise TypeError(f'{action}: 数据包非预期的 dict 类型')

            result: dict = resp['result']
            if not result:
                raise ValueError(f'{action}: 数据包中未找到 result 字段')

            if 'goodsDetailList' not in result:
                raise ValueError(
                    f'{action}: 数据包中未找到 result.goodsDetailList 字段'
                )

            goods_detail_list: list[dict] = result['goodsDetailList']
            if not isinstance(goods_detail_list, list):
                raise TypeError(
                    f'{action}: 数据包的 result.goodsDetailList 字段非预期 list 格式'
                )

            return goods_detail_list

        wait__goods_packet(lambda: page.get(Urls.goods_effect), '进入页面')

        if not page.ele(
            't:span@@class^goods-content_tabLabel@@text()=商品明细', timeout=2
        ):
            raise RuntimeError('未找到商品明细选项卡')

        list_container = page.ele('c:div[class^=goods-content_goodsContent]', timeout=5)
        if not list_container:
            raise RuntimeError('未找到商品明细数据容器')

        target_btn = list_container.ele(
            't:label@@data-testid=beast-core-radio@@text()=30日', timeout=3
        )
        if not target_btn:
            raise RuntimeError('未找到近30日按钮')

        wait__goods_packet(
            lambda: Pagination.set__max_page_size(page=page), '修改最大页码'
        )

        goods_detail_list = wait__goods_packet(
            lambda: target_btn.click(by_js=True),
            action='选择目标天数',
            parse=True,
        )
        if raw is True or not goods_detail_list:
            return goods_detail_list

        goods_detail_list__hub = [*goods_detail_list]
        while True:
            next_btn = Pagination.next(page=page, click=False)
            if not next_btn:
                break

            sleep(uniform(*_interval_sleep_range))
            goods_detail_list: list[dict] = wait__goods_packet(
                partial(next_btn.click, by_js=True),
                action='下一页',
                parse=True,
            )
            if not goods_detail_list:
                break

            goods_detail_list__hub.extend(goods_detail_list)

        font_filepath = download__font(page=page)
        font_decrypter = FontDecrypter(font_path=font_filepath)

        if open_page is True:
            page.close()

        records: dict[str, dict[str, dict]] = {}
        for item in goods_detail_list__hub:
            _record = Utils.dict_mapping(
                item, Dictionary.data_center.goods_effect__detail
            )
            _record = Utils.dict_format__strip(
                _record, fields=['成交转化率', '下单率', '成交率'], suffix=['%']
            )
            for k, v in _record.items():
                if not isinstance(v, str):
                    continue
                _record[k] = font_decrypter.decrypt(v)

            _record = Utils.dict_format__number(_record)
            _record = Utils.dict_format__round(_record)

            goods_id = str(item.get('goodsId'))
            records[goods_id] = _record

        return records

    def get__transaction__overview(self, date: str, timeout: float = None, raw=False):
        """
        [交易数据-交易概况-数据概览] 数据获取

        Args:
            date: 日期，格式：YYYY-MM-DD
            timeout: 超时时间，默认 15 秒
            raw: 是否返回原始数据，默认 False
        Returns:
            交易概况数据
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.transaction__overview,
            method='POST',
            res_type='Fetch',
        )
        uri = Urls.transaction__overview.format(date=date)
        page.get(uri)
        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise TimeoutError('数据包获取超时')

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('在数据包中未找到 result 字段')
        result = resp['result']
        if not isinstance(result, dict):
            raise TypeError('数据包中的 result 字段非预期的 dict 类型')
        if 'dayList' not in result:
            raise ValueError('数据包中未找到 result.dayList 字段')
        day_list: list[dict] = result['dayList']
        if not isinstance(day_list, list):
            raise TypeError('数据包中的 result.dayList 字段非预期的 list 类型')

        record = next(filter(lambda x: x.get('stateDate') == date, day_list), None)

        page.close()

        if raw is True:
            return record

        record = Utils.dict_mapping(
            record, Dictionary.data_center.transaction__overview
        )
        record = Utils.dict_format__ratio(
            record, fields=['成交转化率', '成交老买家占比']
        )
        record = Utils.dict_format__round(record)

        return record

    def get__service__comment__overview(
        self, date: str, timeout: float = None, raw=False
    ):
        """
        [服务数据-评价数据-总览] 数据获取
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.service__comment__overview + '$',
            is_regex=True,
            method='POST',
            res_type='Fetch',
        )
        uri = Urls.service__comment.format(date=date)
        page.get(uri)
        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise TimeoutError('数据包获取超时')

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('在数据包中未找到 result 字段')

        result: dict = resp.get('result')
        if not result:
            raise ValueError('数据包中未找到 result 字段')
        if not isinstance(result, dict):
            raise TypeError('数据包中的 result 字段非预期的 dict 类型')

        page.close()

        if raw is True:
            return result

        record = Utils.dict_mapping(
            result, Dictionary.data_center.service__comment__overview
        )
        record = Utils.dict_format__round(record, fields=['店铺评价分'])

        return record

    def get__service__exp__overview(self, timeout: float = None, raw=False):
        """
        [服务数据-消费者体验指标-概览] 数据获取
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.service__exp__overview,
            method='POST',
            res_type='Fetch',
        )
        page.get(Urls.service__exp)
        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise TimeoutError('数据包获取超时')

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('在数据包中未找到 result 字段')

        result: dict = resp.get('result')
        if not isinstance(result, dict):
            raise TypeError('数据包中的 result 字段非预期的 dict 类型')

        page.close()

        if raw is True:
            return result

        record = Utils.dict_mapping(
            result, Dictionary.data_center.service__exp__overview
        )
        record = Utils.dict_format__round(
            record, fields=['消费者服务体验分'], precision=1
        )

        return record

    def get__service__detail__overview(
        self, date: str, timeout: float = None, raw=False
    ):
        """
        [服务数据-售后数据-整体情况] 数据获取
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else self._timeout

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.service__detail__overview,
            method='POST',
            res_type='Fetch',
        )
        uri = Urls.service__detail.format(date=date)
        page.get(uri)
        packet = page.listen.wait(timeout=_timeout)
        if not packet:
            raise TimeoutError('数据包获取超时')

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('在数据包中未找到 result 字段')

        result: dict = resp.get('result')
        if not isinstance(result, dict):
            raise TypeError('数据包中的 result 字段非预期的 dict 类型')

        page.close()

        if raw is True:
            return result

        record = Utils.dict_mapping(
            result, Dictionary.data_center.service__detail__overview
        )
        record = Utils.dict_format__ratio(
            record, fields=['纠纷退款率', '平台介入率', '品质退款率', '成功退款率']
        )
        record = Utils.dict_format__round(
            record, fields=['纠纷退款率', '平台介入率', '品质退款率', '成功退款率']
        )

        return record
