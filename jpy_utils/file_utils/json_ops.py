"""
JSON文件操作工具
"""

import json
from pathlib import Path
from typing import Any, Dict, Union


def read_json(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    读取JSON文件
    
    Args:
        file_path (Union[str, Path]): JSON文件路径
    
    Returns:
        Dict[str, Any]: JSON数据
    
    Raises:
        FileNotFoundError: 文件不存在
        json.JSONDecodeError: JSON格式错误
    
    Examples:
        >>> data = read_json('config.json')
        {'key': 'value'}
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(data: Dict[str, Any], file_path: Union[str, Path], indent: int = 4) -> None:
    """
    写入JSON文件
    
    Args:
        data (Dict[str, Any]): 要写入的数据
        file_path (Union[str, Path]): 输出文件路径
        indent (int, optional): 缩进空格数. Defaults to 4.
    
    Examples:
        >>> write_json({'key': 'value'}, 'output.json')
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)