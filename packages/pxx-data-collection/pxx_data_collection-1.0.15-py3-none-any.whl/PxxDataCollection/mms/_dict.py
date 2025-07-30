class DataCenter:
    flow_plate__overview = {
        '店铺访客数': 'uv',
        '店铺浏览量': 'pv',
        '商品访客数': 'guv',
        '商品浏览量': 'gpv',
        '成交买家数': 'payOrdrUsrCnt',
        '成交订单数': 'payOrdrCnt',
        '成交金额': 'payOrdrAmt',
        '成交转化率': 'payUvRto',
        '客单价': 'payOrdrAup',
        '成交UV价值': 'uvCfmVal',
    }
    goods_effect__overview = {
        '商品访客数': 'guv',
        '商品浏览量': 'gpv',
        '商品收藏用户数': 'goodsFavCnt',
        '被访问商品数': 'vstGoodsCnt',
        '成交金额': 'payOrdrAmt',
        '成交订单数': 'payOrdrCnt',
        '成交买家数': 'payOrdrUsrCnt',
        '成交转化率': 'payUvRto',
    }
    goods_effect__detail = {
        '商品名称': 'goodsName',
        '商品访客数': 'goodsUv',
        '商品浏览量': 'goodsPv',
        '成交金额': 'payOrdrAmt',
        '成交件数': 'payOrdrGoodsQty',
        '成交订单数': 'payOrdrCnt',
        '成交买家数': 'payOrdrUsrCnt',
        '成交转化率': 'goodsVcr',
        '商品收藏用户数': 'goodsFavCnt',
        '下单率': 'ordrVstrRto',
        '成交率': 'payOrdrRto',
    }
    transaction__overview = {
        '成交金额': 'payOrdrAmt',
        '成交买家数': 'payOrdrUsrCnt',
        '客单价': 'payOrdrAup',
        '成交转化率': 'payUvRto',
        '店铺关注用户数': 'mallFavCnt',
        '成交订单数': 'payOrdrCnt',
        '成交老买家占比': 'rpayUsrRtoDth',
        '退款金额': 'sucRfOrdrAmt1d',
        '退款单数': 'sucRfOrdrCnt1d',
    }
    service__comment__overview = {'店铺评价分': 'descOver50RevScr3m'}
    service__exp__overview = {'消费者服务体验分': 'cstmrServScore'}
    service__detail__overview = {
        '纠纷退款数': 'dsptRfSucOrdrCnt1m',
        '纠纷退款率': 'dsptRfSucRto1m',
        '介入订单数': 'pltInvlOrdrCnt1m',
        '平台介入率': 'pltInvlOrdrRto1m',
        '品质退款率': 'qurfOrdRto1m',
        '成功退款订单数': 'sucRfOrdrCnt1d',
        '成功退款金额': 'sucRfOrdrAmt1d',
        '成功退款率': 'rfSucRto1m',
    }


class CustomerService:
    service__overview = {
        '咨询人数': 'consultUserCnt',
        '需人工回复的咨询人数': 'needManuReplyConsultUserCnt',
        '人工接待人数': 'receiveUserCnt',
        '3分钟人工回复率': 'manuReplyRate3Min',
        '平均人工响应时长': 'artificialResponseTime',
    }
    sales__overview = {
        '询单人数': 'inquiryOrderUserCnt',
        '最终成团人数': 'groupUserCnt',
        '询单转化率': 'inquiryOrderTransformRate',
        '客服销售额': 'csSalesAmount',
        '客服可提升销售额': 'csCanImproveSalesAmount',
    }


class Dictionary:
    data_center = DataCenter()
    customer_service = CustomerService()
