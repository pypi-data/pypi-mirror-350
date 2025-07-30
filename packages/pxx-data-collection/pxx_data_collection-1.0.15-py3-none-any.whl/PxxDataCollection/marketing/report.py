"""
推广中心-报表数据采集器
"""

from DrissionPage import Chromium
from DrissionPage._units.listener import DataPacket

from .._utils import Utils
from ._dict import Dictionary
from ._utils import Pagination


class Urls:
    goods_promotion = 'https://yingxiao.pinduoduo.com/goods/report/promotion/overView?beginDate={begin_date}&endDate={end_date}'


class DataPacketUrls:
    goods_promotion__overview = (
        'yingxiao.pinduoduo.com/mms-gateway/apollo/api/report/queryEntityReport'
    )
    goods_promotion__detail = (
        'yingxiao.pinduoduo.com/mms-gateway/apollo/api/report/queryEntityReport'
    )


class Report:
    def __init__(self, browser: Chromium):
        self._browser = browser

    def get__goods_promotion__overview(
        self, begin_date: str, end_date: str, timeout: float = None, raw=False
    ):
        """
        [报表-商品推广-数据概况] 数据获取
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else 15

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.goods_promotion__overview,
            method='POST',
            res_type='XHR',
        )
        uri = Urls.goods_promotion.format(begin_date=begin_date, end_date=end_date)
        page.get(uri)
        packet_list: list[DataPacket] = page.listen.wait(
            count=2, timeout=_timeout, fit_count=False
        )
        packet = None
        for item in packet_list:
            reqdata: dict = item.request.postData
            if (
                reqdata.get('startDate') == begin_date
                and reqdata.get('endDate') == end_date
            ):
                packet = item
                break

        if not packet:
            raise RuntimeError('进入页面后获取数据包超时, 可能访问失败')

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('数据包中未找到 result 字段')

        result: dict = resp.get('result')
        if not isinstance(result, dict):
            raise ValueError('数据包中 result 字段类型非预期的 dict 类型')

        if 'totalSumReport' not in result:
            raise ValueError('数据包中未找到 result.totalSumReport 字段')

        record = result.get('totalSumReport')
        if not isinstance(record, dict):
            raise ValueError('数据包中 result.totalSumReport 字段非预期的 dict 类型')

        page.close()

        if raw is True:
            return record

        record = Utils.dict_mapping(record, Dictionary.report.goods_promotion__overview)
        record = Utils.dict_format__float(
            record,
            fields=[
                '总花费',
                '成交花费',
                '交易额',
                '净交易额',
                '每笔净成交花费',
                '每笔成交花费',
                '每笔成交金额',
            ],
            precision=3,
        )
        record = Utils.dict_format__float(
            record, fields=['净实际投产比', '实际投产比'], precision=4
        )
        record = Utils.dict_format__ratio(
            record, fields=['净交易额占比', '全站推广费比']
        )
        record = Utils.dict_format__round(record)

        return record

    def get__goods_promotion__detail(
        self,
        goods_ids: list[str],
        begin_date: str,
        end_date: str,
        timeout: float = None,
        set_max_page=False,
        raw=False,
    ):
        """
        [报表-商品推广-数据明细] 数据获取

        Args:
            goods_ids: 商品 ID 列表
            begin_date: 开始日期
            end_date: 结束日期
            timeout: 超时时间, 默认 15 秒
            set_max_page: 是否设置最大分页, 默认 False
            raw: 是否返回原始数据, 默认 False
        Returns:
            商品推广明细数据. {'商品ID': {'字段1': '值1', '字段2': '值2'}}
        """

        _timeout = timeout if isinstance(timeout, (int, float)) else 15

        page = self._browser.new_tab()
        page.listen.start(
            targets=DataPacketUrls.goods_promotion__detail,
            method='POST',
            res_type='XHR',
        )
        uri = Urls.goods_promotion.format(begin_date=begin_date, end_date=end_date)
        page.get(uri)
        packet_list: list[DataPacket] = page.listen.wait(
            count=2, timeout=_timeout, fit_count=False
        )
        packet = None
        for item in packet_list:
            reqdata: dict = item.request.postData
            if (
                reqdata.get('startDate') == begin_date
                and reqdata.get('endDate') == end_date
            ):
                packet = item
                break

        if not packet:
            raise RuntimeError('进入页面后获取数据包超时, 可能访问失败')

        # ========== 修改页面大小 ==========
        if set_max_page is True:
            page.listen.start(
                targets=DataPacketUrls.goods_promotion__detail,
                method='POST',
                res_type='XHR',
            )
            Pagination.set__max_page_size(page=page)
            packet = page.listen.wait(timeout=_timeout)

            if not packet:
                raise RuntimeError('修改页面大小后获取数据包超时')
        # ========== 修改页面大小 ==========

        resp: dict = packet.response.body
        if 'result' not in resp:
            raise ValueError('数据包中未找到 result 字段')

        result: dict = resp.get('result')
        if not isinstance(result, dict):
            raise ValueError('数据包中 result 字段类型非预期的 dict 类型')

        if 'entityReportList' not in result:
            raise ValueError('数据包中未找到 result.entityReportList 字段')

        data_list: list[dict] = result.get('entityReportList')
        if not isinstance(data_list, list):
            raise ValueError(
                '数据包中 result.entityReportList 字段类型非预期的 list 类型'
            )

        records: dict[str, dict] = {}
        notfind_goods_ids = [*goods_ids]
        for item in data_list:
            if not notfind_goods_ids:
                break

            goods_info: dict = item.get('externalFieldValues')
            if not goods_info:
                continue

            if (item_goods_id := goods_info.get('goodsId')) in notfind_goods_ids:
                records[item_goods_id] = item
                notfind_goods_ids.remove(item_goods_id)
                continue

        if raw is True:
            return records

        for goods_id, record in records.items():
            _record = Utils.dict_mapping(
                record, Dictionary.report.goods_promotion__detail
            )
            _record = Utils.dict_format__float(
                _record,
                fields=[
                    '总花费',
                    '成交花费',
                    '交易额',
                    '净交易额',
                    '每笔净成交花费',
                    '每笔成交花费',
                    '每笔成交金额',
                    '直接交易额',
                    '间接交易额',
                    '每笔直接成交金额',
                    '每笔间接成交金额',
                ],
                precision=3,
            )
            _record = Utils.dict_format__float(
                _record, fields=['净实际投产比', '实际投产比'], precision=4
            )
            _record = Utils.dict_format__ratio(
                _record, fields=['净交易额占比', '全站推广费比']
            )
            _record = Utils.dict_format__round(_record)
            records[goods_id] = _record

        return records
