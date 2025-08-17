"""
日期时间转换工具
"""

from datetime import datetime
from typing import Union


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