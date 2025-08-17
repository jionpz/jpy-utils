"""
字符串处理相关的工具函数

提供常用的字符串格式转换、清理、验证等功能。
"""

import re
import random
import string
from typing import Optional


def camel_to_snake(text: str) -> str:
    """
    驼峰命名转下划线命名
    
    Args:
        text (str): 驼峰命名字符串
    
    Returns:
        str: 下划线命名字符串
    
    Examples:
        >>> camel_to_snake('CamelCase')
        'camel_case'
        >>> camel_to_snake('XMLHttpRequest')
        'xml_http_request'
    """
    # 在大写字母前插入下划线
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    # 处理连续大写字母
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_camel(text: str, capitalize_first: bool = False) -> str:
    """
    下划线命名转驼峰命名
    
    Args:
        text (str): 下划线命名字符串
        capitalize_first (bool, optional): 是否首字母大写. Defaults to False.
    
    Returns:
        str: 驼峰命名字符串
    
    Examples:
        >>> snake_to_camel('snake_case')
        'snakeCase'
        >>> snake_to_camel('snake_case', True)
        'SnakeCase'
    """
    components = text.split('_')
    if capitalize_first:
        return ''.join(word.capitalize() for word in components)
    else:
        return components[0] + ''.join(word.capitalize() for word in components[1:])


def clean_text(text: str) -> str:
    """
    清理文本空白字符
    
    Args:
        text (str): 原始文本
    
    Returns:
        str: 清理后的文本
    
    Examples:
        >>> clean_text('  hello   world  ')
        'hello world'
    """
    # 去除首尾空白并将多个空白字符替换为单个空格
    return re.sub(r'\s+', ' ', text.strip())


def truncate_text(text: str, length: int, suffix: str = "...") -> str:
    """
    截断文本
    
    Args:
        text (str): 原始文本
        length (int): 最大长度
        suffix (str, optional): 截断后缀. Defaults to "...".
    
    Returns:
        str: 截断后的文本
    
    Examples:
        >>> truncate_text('This is a long text', 10)
        'This is...'
    """
    if len(text) <= length:
        return text
    return text[:length - len(suffix)] + suffix


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


def remove_html_tags(text: str) -> str:
    """
    移除HTML标签
    
    Args:
        text (str): 包含HTML标签的文本
    
    Returns:
        str: 纯文本
    
    Examples:
        >>> remove_html_tags('<p>Hello <b>world</b>!</p>')
        'Hello world!'
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def extract_numbers(text: str) -> list:
    """
    提取文本中的数字
    
    Args:
        text (str): 原始文本
    
    Returns:
        list: 数字列表
    
    Examples:
        >>> extract_numbers('Price: $12.99, Quantity: 5')
        ['12.99', '5']
    """
    pattern = r'\d+\.?\d*'
    return re.findall(pattern, text)


def slugify(text: str) -> str:
    """
    将文本转换为URL友好的slug格式
    
    Args:
        text (str): 原始文本
    
    Returns:
        str: slug格式文本
    
    Examples:
        >>> slugify('Hello World! This is a Test.')
        'hello-world-this-is-a-test'
    """
    # 转小写并替换空白字符为连字符
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')