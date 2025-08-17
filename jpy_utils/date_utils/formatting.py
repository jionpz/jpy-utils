"""
日期时间格式化工具
"""

import time
from datetime import datetime


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