"""
字符串大小写转换工具
"""

import re


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