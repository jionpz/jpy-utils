"""
文本处理工具
"""

import re


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