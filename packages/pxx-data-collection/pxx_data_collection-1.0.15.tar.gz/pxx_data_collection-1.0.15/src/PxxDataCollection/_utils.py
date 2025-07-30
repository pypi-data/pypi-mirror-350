from copy import deepcopy
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse


class Utils:
    @staticmethod
    def date_yesterday(pattern='%Y-%m-%d'):
        """
        获取前一天的日期

        Args:
            pattern: 日期格式
        """

        return Utils.date_calculate(days=1, pattern=pattern)

    @staticmethod
    def date_calculate(days: int, pattern='%Y-%m-%d'):
        """
        日期计算

        Args:
            days: 日期偏移量, 负数表示向后推
            pattern: 日期格式
        """

        return (datetime.now() - timedelta(days=days)).strftime(pattern)

    @staticmethod
    def date_diff_days(a: str, b: str, pattern='%Y-%m-%d'):
        """
        计算两个日期间隔的天数
        - 正数表示 a 日期在 b 日期之后

        Args:
            a: 日期字符串
            b: 日期字符串
        """

        a_dt = datetime.strptime(a, pattern)
        b_dt = datetime.strptime(b, pattern)

        return (a_dt - b_dt).days

    @staticmethod
    def date_to_timestamp(date: str, pattern='%Y-%m-%d'):
        """
        将日期转为 10 位时间戳

        Args:
            date: 日期字符串
            pattern: 日期格式
        """

        dt = datetime.strptime(date, pattern)
        dt = dt.replace(tzinfo=timezone(timedelta(hours=8)))
        return int(dt.timestamp())

    @staticmethod
    def date_range(begin_date: str, end_date: str, pattern='%Y-%m-%d'):
        """
        根据起始日期和结束日期生成日期列表

        Args:
            begin_date: 起始日期字符串
            end_date: 结束日期字符串
            pattern: 日期格式
        Returns:
            日期列表
        """

        begin_dt, end_dt = [
            datetime.strptime(date, pattern) for date in (begin_date, end_date)
        ]
        diff = (end_dt - begin_dt).days
        date_list = [
            (begin_dt + timedelta(days=i)).strftime(pattern) for i in range(diff + 1)
        ]

        return date_list

    @staticmethod
    def same_url(a: str, b: str):
        """
        检查两个 url 是否域名及路径是否一致

        Args:
            a: 第一个 url
            b: 第二个 url
        Returns:
            是否一致
        """

        a_result = urlparse(a)
        b_result = urlparse(b)

        is_same = a_result.netloc == b_result.netloc and a_result.path == b_result.path

        return is_same

    @staticmethod
    def dict_mapping(data: dict, dict_table: dict[str, str]):
        """
        字典表字段映射

        Args:
            data: 待映射的字典
            dict_table: 字典表
        """

        result = {}
        for text, key in dict_table.items():
            result[text] = data.get(key)

        return result

    @staticmethod
    def dict_format__float(data: dict, fields: list[str] = None, precision: int = 2):
        """
        将字典数据中的指定字段格式化为 float 类型

        Args:
            data: 待格式化的字典
            fields: 需要格式化的字段列表, 如果为 None, 则表示所有字段
            precision: 保留小数位数, 默认 2 位
        Returns:
            格式化后的字典
        """

        _fields = fields if fields and isinstance(fields, list) else data.keys()

        _data = deepcopy(data)
        for field in _fields:
            if field not in _data:
                continue

            value = _data[field]
            if not isinstance(value, (int, float)):
                continue

            _data[field] = value / 10**precision

        return _data

    @staticmethod
    def dict_format__round(data: dict, fields: list[str] = None, precision: int = 2):
        """
        将字典数据中的指定字段作四舍五入处理

        Args:
            data: 待格式化的字典
            fields: 需要格式化的字段列表, 如果为 None, 则表示所有字段
            precision: 保留小数位数, 默认 2 位
        Returns:
            格式化后的字典
        """

        _fields = fields if fields and isinstance(fields, list) else data.keys()

        _data = deepcopy(data)
        for field in _fields:
            if field not in _data:
                continue

            value = _data[field]
            if not isinstance(value, float):
                continue

            _data[field] = round(value, precision)

        return _data

    @staticmethod
    def dict_format__ratio(data: dict, fields: list[str] = None, ratio: int = 2):
        """
        将字典数据中的指定字段转为比率, 例如百分比/千分比等

        Args:
            data: 待格式化的字典
            fields: 需要格式化的字段列表, 如果为 None, 则表示所有字段
            ratio: 比率, 默认 2 及百分比
        Returns:
            格式化后的字典
        """

        _fields = fields if fields and isinstance(fields, list) else data.keys()

        _data = deepcopy(data)
        for field in _fields:
            if field not in _data:
                continue

            value = _data[field]
            if not isinstance(value, (int, float)):
                continue

            _data[field] = value * (10**ratio)

        return _data

    @staticmethod
    def dict_format__strip(
        data: dict,
        fields: list[str] = None,
        prefix: list[str] = None,
        suffix: list[str] = None,
    ):
        """
        格式化字典数据中的指定字段, 去除前后空格及指定前后缀

        Args:
            data: 待格式化的字典
            fields: 需要格式化的字段列表, 如果为 None, 则表示所有字段
            prefix: 需要去除的前缀列表
            suffix: 需要去除的后缀列表
        Returns:
            格式化后的字典
        """

        _fields = fields if fields and isinstance(fields, list) else data.keys()

        _data = deepcopy(data)
        for field in _fields:
            if field not in _data:
                continue

            value = _data[field]
            if not isinstance(value, str):
                continue

            value = value.strip()
            if prefix and isinstance(prefix, list):
                for c in prefix:
                    value = value.lstrip(c)

            if suffix and isinstance(suffix, list):
                for c in suffix:
                    value = value.rstrip(c)

            _data[field] = value

        return _data

    @staticmethod
    def dict_format__number(data: dict, fields: list[str] = None):
        """
        格式化字典数据中的指定字段, 将字符串转为数字

        Args:
            data: 待格式化的字典
            fields: 需要格式化的字段列表, 如果为 None, 则表示所有字段
        Returns:
            格式化后的字典
        """

        _fields = fields if fields and isinstance(fields, list) else data.keys()

        _data = deepcopy(data)
        for field in _fields:
            if field not in _data:
                continue

            value = _data[field]
            if not isinstance(value, str):
                continue

            try:
                value = value.replace(',', '')
                value = float(value) if '.' in value else int(value)
            except ValueError:
                continue

            _data[field] = value

        return _data
