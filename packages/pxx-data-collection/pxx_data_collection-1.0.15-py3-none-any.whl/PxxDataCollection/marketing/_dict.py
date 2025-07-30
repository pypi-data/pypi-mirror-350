class Account:
    report__daily = {'交易金额': 'amount'}


class Report:
    goods_promotion__overview = {
        '总花费': 'spend',
        '成交花费': 'orderSpend',
        '交易额': 'gmv',
        '实际投产比': 'orderSpendRoiUnified',
        '净实际投产比': 'orderSpendNetRoi',
        '净交易额': 'netGmv',
        '净成交笔数': 'netOrderNum',
        '每笔净成交花费': 'orderSpendNetCostPerOrder',
        '净交易额占比': 'netGmvRate',
        '成交笔数': 'orderNum',
        '每笔成交花费': 'costPerOrder',
        '每笔成交金额': 'avgPayAmount',
        '全站推广费比': 'globalTakeRate',
        '曝光量': 'impression',
        '点击量': 'click',
    }
    goods_promotion__detail = {
        '总花费': 'spend',
        '成交花费': 'orderSpend',
        '交易额': 'gmv',
        '实际投产比': 'orderSpendRoiUnified',
        '净实际投产比': 'orderSpendNetRoi',
        '净交易额': 'netGmv',
        '净成交笔数': 'netOrderNum',
        '每笔净成交花费': 'orderSpendNetCostPerOrder',
        '净交易额占比': 'netGmvRate',
        '成交笔数': 'orderNum',
        '每笔成交花费': 'costPerOrder',
        '每笔成交金额': 'avgPayAmount',
        '直接交易额': 'directGmv',
        '间接交易额': 'indirectGmv',
        '直接成交笔数': 'directOrderNum',
        '间接成交笔数': 'indirectOrderNum',
        '每笔直接成交金额': 'avgDirectPayAmount',
        '每笔间接成交金额': 'avgIndirectPayAmount',
        '全站推广费比': 'globalTakeRate',
        '曝光量': 'impression',
        '点击量': 'click',
    }


class Dictionary:
    account = Account()
    report = Report()
