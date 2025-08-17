"""
字符串生成工具
"""

import random
import string
from typing import Optional


def generate_random_string(length: int, chars: Optional[str] = None) -> str:
    """
    生成随机字符串
    
    Args:
        length (int): 字符串长度
        chars (Optional[str], optional): 字符集. Defaults to None.
    
    Returns:
        str: 随机字符串
    
    Examples:
        >>> random_str = generate_random_string(8)
        'aBc123Xy'
    """
    if chars is None:
        chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))