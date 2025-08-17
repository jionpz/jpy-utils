"""
日期时间处理相关的工具函数

提供常用的日期时间格式化、转换、计算等功能。
"""

import time
from datetime import datetime, timedelta, date
from typing import Union, List, Optional


def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    格式化日期时间
    
    Args:
        dt (datetime): 日期时间对象
        format_str (str, optional): 格式字符串. Defaults to "%Y-%m-%d %H:%M:%S".
    
    Returns:
        str: 格式化后的日期时间字符串
    
    Examples:
        >>> dt = datetime(2023, 12, 25, 15, 30, 45)
        >>> format_datetime(dt)
        '2023-12-25 15:30:45'
    """
    return dt.strftime(format_str)


def get_timestamp() -> int:
    """
    获取当前时间戳（秒）
    
    Returns:
        int: 当前时间戳
    
    Examples:
        >>> timestamp = get_timestamp()
        1703509845
    """
    return int(time.time())


def get_timestamp_ms() -> int:
    """
    获取当前时间戳（毫秒）
    
    Returns:
        int: 当前时间戳（毫秒）
    
    Examples:
        >>> timestamp = get_timestamp_ms()
        1703509845123
    """
    return int(time.time() * 1000)


def timestamp_to_datetime(timestamp: Union[int, float]) -> datetime:
    """
    时间戳转日期时间
    
    Args:
        timestamp (Union[int, float]): 时间戳（秒）
    
    Returns:
        datetime: 日期时间对象
    
    Examples:
        >>> dt = timestamp_to_datetime(1703509845)
        datetime(2023, 12, 25, 15, 30, 45)
    """
    return datetime.fromtimestamp(timestamp)


def datetime_to_timestamp(dt: datetime) -> int:
    """
    日期时间转时间戳
    
    Args:
        dt (datetime): 日期时间对象
    
    Returns:
        int: 时间戳（秒）
    
    Examples:
        >>> dt = datetime(2023, 12, 25, 15, 30, 45)
        >>> datetime_to_timestamp(dt)
        1703509845
    """
    return int(dt.timestamp())


def get_date_range(start_date: Union[str, date], end_date: Union[str, date]) -> List[date]:
    """
    获取日期范围内的所有日期
    
    Args:
        start_date (Union[str, date]): 开始日期
        end_date (Union[str, date]): 结束日期
    
    Returns:
        List[date]: 日期列表
    
    Examples:
        >>> dates = get_date_range('2023-12-01', '2023-12-03')
        [date(2023, 12, 1), date(2023, 12, 2), date(2023, 12, 3)]
    """
    if isinstance(start_date, str):
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    if isinstance(end_date, str):
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
    
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        date_list.append(current_date)
        current_date += timedelta(days=1)
    
    return date_list


def add_days(dt: Union[datetime, date], days: int) -> Union[datetime, date]:
    """
    日期加减天数
    
    Args:
        dt (Union[datetime, date]): 日期或日期时间
        days (int): 要添加的天数（可为负数）
    
    Returns:
        Union[datetime, date]: 计算后的日期
    
    Examples:
        >>> new_date = add_days(date(2023, 12, 25), 7)
        date(2024, 1, 1)
    """
    return dt + timedelta(days=days)


def add_months(dt: Union[datetime, date], months: int) -> Union[datetime, date]:
    """
    日期加减月份
    
    Args:
        dt (Union[datetime, date]): 日期或日期时间
        months (int): 要添加的月份数（可为负数）
    
    Returns:
        Union[datetime, date]: 计算后的日期
    
    Examples:
        >>> new_date = add_months(date(2023, 12, 25), 2)
        date(2024, 2, 25)
    """
    year = dt.year
    month = dt.month + months
    
    # 处理月份溢出
    while month > 12:
        year += 1
        month -= 12
    while month < 1:
        year -= 1
        month += 12
    
    # 处理日期有效性（如2月31日不存在）
    day = dt.day
    try:
        if isinstance(dt, datetime):
            return dt.replace(year=year, month=month, day=day)
        else:
            return date(year, month, day)
    except ValueError:
        # 如果日期无效，使用该月的最后一天
        import calendar
        last_day = calendar.monthrange(year, month)[1]
        if isinstance(dt, datetime):
            return dt.replace(year=year, month=month, day=last_day)
        else:
            return date(year, month, last_day)


def get_weekday(dt: Union[datetime, date]) -> str:
    """
    获取星期几
    
    Args:
        dt (Union[datetime, date]): 日期或日期时间
    
    Returns:
        str: 星期几（中文）
    
    Examples:
        >>> get_weekday(date(2023, 12, 25))  # 星期一
        '星期一'
    """
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    return weekdays[dt.weekday()]


def is_weekend(dt: Union[datetime, date]) -> bool:
    """
    判断是否为周末
    
    Args:
        dt (Union[datetime, date]): 日期或日期时间
    
    Returns:
        bool: 是否为周末
    
    Examples:
        >>> is_weekend(date(2023, 12, 23))  # 星期六
        True
    """
    return dt.weekday() >= 5


def get_age(birth_date: Union[str, date], reference_date: Optional[date] = None) -> int:
    """
    计算年龄
    
    Args:
        birth_date (Union[str, date]): 出生日期
        reference_date (Optional[date], optional): 参考日期. Defaults to None（今天）.
    
    Returns:
        int: 年龄
    
    Examples:
        >>> age = get_age('1990-05-15')
        33
    """
    if isinstance(birth_date, str):
        birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
    
    if reference_date is None:
        reference_date = date.today()
    
    age = reference_date.year - birth_date.year
    
    # 检查是否已过生日
    if reference_date.month < birth_date.month or \
       (reference_date.month == birth_date.month and reference_date.day < birth_date.day):
        age -= 1
    
    return age