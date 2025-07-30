from time import sleep

from DrissionPage._pages.mix_tab import MixTab
from DrissionPage.common import Keys


def pick__custom_date(begin_date: str, end_date: str, page: MixTab):
    """
    选择自定义日期

    Args:
        begin_date: 开始日期
        end_date: 结束日期
        page: 浏览器标签页对象
    """

    mapping = [['开始日期', begin_date], ['结束日期', end_date]]

    for text, date in mapping:
        date_input_ele = page.ele(
            f'c:div.anq-picker-input input[placeholder="{text}"]', timeout=3
        )
        if not date_input_ele:
            raise RuntimeError(f'未找到 {text} 输入框元素')

        date_input_ele.input(date.replace('-', '/') + Keys.ENTER, clear=True)
        sleep(0.8)


class Pagination:
    """分页器处理类"""

    @staticmethod
    def set__max_page_size(page: MixTab):
        """设置最大分页大小"""

        page.scroll.to_bottom().scroll.to_rightmost()

        pagesize_pretext = page.ele(
            't:span@@class=anq-perpage-text@@text()=每页', timeout=3
        )
        pagesize_changer = pagesize_pretext.next('t:div')
        pagesize_changer.click()

        max_pagesize_item = page.ele('c:div.anq-select-item[title="100"]', timeout=3)
        max_pagesize_item.click()
