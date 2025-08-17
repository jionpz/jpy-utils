"""
字符串验证工具
"""

import re


def is_email(email: str) -> bool:
    """
    验证邮箱格式
    
    Args:
        email (str): 邮箱地址
    
    Returns:
        bool: 是否为有效邮箱
    
    Examples:
        >>> is_email('test@example.com')
        True
        >>> is_email('invalid-email')
        False
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))