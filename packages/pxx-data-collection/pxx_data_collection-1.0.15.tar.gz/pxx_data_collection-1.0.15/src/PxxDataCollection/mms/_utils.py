import json
import re
from os import path
from tempfile import gettempdir
from time import sleep

from DrissionPage._elements.chromium_element import ChromiumElement
from DrissionPage._pages.mix_tab import MixTab


def download__font(page: MixTab) -> str:
    """
    获取并下载反爬字体

    Args:
        tab: 浏览器标签页对象
    Returns:
        字体文件路径
    """

    style_ele = page.ele('c:style[data-id^="spider"]', timeout=5)

    if not style_ele:
        raise ValueError('未在网页中找到包含字体文件路径的 style 元素')

    rs = re.findall(r'https:[^\s]+\.ttf', style_ele.raw_text)
    if not rs:
        raise ValueError('未在 style 元素中找到反爬字体的 url')

    font_url = rs[0]

    download_status, file_path = page.download(
        file_url=font_url,
        save_path=gettempdir(),
        rename='mms_crawl_font.ttf',
        file_exists='overwrite',
        show_msg=False,
    )
    if download_status != 'success' or not path.exists(file_path):
        raise RuntimeError('下载反爬字体失败')

    return file_path


def pick__custom_date(
    date: str, page: MixTab = None, container: ChromiumElement = None
):
    """
    自定义日期选择

    Args:
        date: 需要选择的日期
        page: 浏览器标签页对象
        container: 父容器元素, 留空则表示 body 元素
    """

    custom_date_picker__id = 'custom_date_picker'
    new_picker = page.ele(f'#{custom_date_picker__id}', timeout=3)
    if not new_picker:
        _container = container if isinstance(container, ChromiumElement) else page
        custom_date_picker = _container.ele('t:label@@text()=自定义', timeout=3)
        if not custom_date_picker:
            raise RuntimeError('未找到自定义日期范围按钮')

        custom_date_picker.scroll.to_see()
        custom_date_picker.set.attr('id', custom_date_picker__id)
        page.run_js(
            f'const el = document.getElementById("{custom_date_picker__id}"); document.body.appendChild(el);'
        )
        new_picker = page.ele(f'#{custom_date_picker__id}', timeout=3)
        new_picker.set.style('position', 'fixed')
        new_picker.set.style('zIndex', '2147483647')
        new_picker.set.style('left', '0')
        new_picker.set.style('top', '0')

    new_picker.click()

    date_picker_modal = page.ele(
        'c:div[data-testid=beast-core-datePicker-dropdown-contentRoot]',
        timeout=3,
    )
    if not date_picker_modal:
        raise RuntimeError('未找到自定义日期选择器弹出面板')

    year, month, day = date.split('-')
    month = month.lstrip('0')
    day = day.lstrip('0')

    # 判断年份
    year_selector = date_picker_modal.ele(
        'c:input[data-testid=beast-core-select-htmlInput]', timeout=2
    )
    if not year_selector:
        raise RuntimeError('未找到日期选择器面板中的年份下拉选择器')

    if year_selector.attr('value').rstrip('年') != year:
        year_selector.click(by_js=True)
        target_year_option = page.ele(f't:li@@role=option@@text()={year}年', timeout=2)
        if not target_year_option:
            raise RuntimeError(f'未找到 {year} 年份选项')
        target_year_option.click(by_js=True)

    # 判断月份
    month_text = page.ele(
        'c:div[class^=RPR_headerSelector] span[class^=RPR_dateText]', timeout=2
    )
    if not month_text:
        raise RuntimeError('未找到日期选择器面板中的月份标签')

    if (page_month := month_text.text.rstrip('月')) != month:
        month_num = int(month)
        page_month_num = int(page_month)
        month_diff = page_month_num - month_num
        month_switch_arrow = 'left' if month_diff > 0 else 'right'
        month_switch_btn = page.ele(
            f'c:section[data-testid=beast-core-datePicker-dropdown-header] svg[data-testid=beast-core-icon-{month_switch_arrow}]',
            timeout=1,
        )
        for _ in range(abs(month_diff)):
            month_switch_btn.click()
            sleep(0.5)

    # 选择日期
    day_cell_ele = page.ele(
        f'c:td[role=date-cell]:not([class*=RPR_outOfMonth]) div[title="{day}"]',
        timeout=1,
    )
    if not day_cell_ele:
        raise RuntimeError(f'未找到 {month} 号日期')

    day_cell_ele.click(by_js=True)


def pick__custom_date_range(begin_date: str, end_date: str, page: MixTab = None):
    """
    自定义日期范围选择
    - 暂时只能选择当月的日期和上个月的最后2天

    Args:
        begin_date: 开始日期
        end_date: 结束日期
        page: 浏览器标签页对象
    """

    custom_btn = page.ele(
        't:label@@data-testid=beast-core-radio@@text()=自定义', timeout=3
    )
    if not custom_btn:
        raise RuntimeError('未找到自定义日期范围按钮')
    custom_btn.scroll.to_see()
    custom_btn.set.style('zIndex', '2147483647')
    custom_btn.click()

    container_ele = page.ele(
        't:div@data-testid^beast-core-rangePicker-dropdown', timeout=3
    )
    if not container_ele:
        raise RuntimeError('未找到日期选择器 dropdown 元素')

    panel_eles = container_ele.eles('c:div[class^="RPR_tableWrapper"]', timeout=3)
    if not panel_eles:
        raise RuntimeError('未找到日期范围选择板列表')

    panel_ele = panel_eles[-1]
    begin_day, end_day = [
        date.split('-')[-1].lstrip('0') for date in [begin_date, end_date]
    ]

    for day in [begin_day, end_day]:
        cell_ele = panel_ele.ele(f'c:div[title="{day}"]', timeout=1)
        if not cell_ele:
            raise RuntimeError(f'未找到 {day} 号日期单元格元素')
        cell_ele.click(by_js=True)
        sleep(0.5)

    confirm_btn = container_ele.ele('t:button@@text()=确认', timeout=3)
    if not confirm_btn:
        raise RuntimeError('未找到确认按钮')

    confirm_btn.click(by_js=True)


def get__shop_name(page: MixTab, throw_exception=True):
    """
    获取店铺名称

    Args:
        throw_exception: 是否抛出异常
    Returns:
        店铺名称
    """

    def find():
        new_userinfo = page.local_storage('new_userinfo')
        if not new_userinfo:
            raise ValueError('未找到本地信息数据或数据为空')
        try:
            new_userinfo: dict = json.loads(new_userinfo)
        except json.JSONDecodeError as e:
            raise ValueError('本地数据信息解析出错') from e
        if 'mall' not in new_userinfo:
            raise ValueError('本地数据中未找到 mall 字段')
        mall = new_userinfo.get('mall')
        if not isinstance(mall, dict):
            raise ValueError('本地数据中 mall 字段非预期 dict 类型')
        if 'mall_name' not in mall:
            raise ValueError('本地数据中未找到 mall.mall_name 字段')
        mall_name: str = mall.get('mall_name')
        return mall_name

    shop_name = None
    try:
        shop_name = find()
    except Exception as e:
        if throw_exception:
            raise e

    return shop_name


class Pagination:
    """分页器处理类"""

    @staticmethod
    def set__max_page_size(page: MixTab):
        """设置最大分页大小"""

        page_size_changer = page.ele(
            'c:li[class^=PGT_sizeChanger] div[data-testid="beast-core-select"]',
            timeout=5,
        )
        if not page_size_changer:
            # 有些店铺因为商品较少, 可能不会提供分页器
            # raise RuntimeError('未找到分页大小切换器')
            return False

        page_size_changer.scroll.to_see()
        page_size_changer.click(by_js=True)

        page_size_option = page.ele('c:li[role="option"]:last-of-type', timeout=3)
        if not page_size_option:
            raise RuntimeError('未找到分页选项')

        page_size_option.click(by_js=True)
        return True

    @staticmethod
    def next(page: MixTab, click=True):
        """下一页, 如果返回 False 则表示已经是最后一页"""

        next_btn = page.ele('c:li[data-testid="beast-core-pagination-next"]', timeout=3)
        if not next_btn:
            # 部分店铺的商品列表页没有下一页按钮
            # raise RuntimeError('未找到 [下一页] 按钮')
            return False

        if 'disabled' in next_btn.attr('class'):
            return False

        if click is True:
            next_btn.click(by_js=True)

        return next_btn
