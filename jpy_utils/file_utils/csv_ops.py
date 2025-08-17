"""
CSV文件操作工具
"""

import csv
from pathlib import Path
from typing import Any, Dict, List, Union


def read_csv(file_path: Union[str, Path], delimiter: str = ',') -> List[Dict[str, str]]:
    """
    读取CSV文件
    
    Args:
        file_path (Union[str, Path]): CSV文件路径
        delimiter (str, optional): 分隔符. Defaults to ','.
    
    Returns:
        List[Dict[str, str]]: CSV数据列表
    
    Examples:
        >>> data = read_csv('data.csv')
        [{'name': 'Alice', 'age': '25'}]
    """
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        for row in reader:
            data.append(row)
    return data


def write_csv(data: List[Dict[str, Any]], file_path: Union[str, Path], delimiter: str = ',') -> None:
    """
    写入CSV文件
    
    Args:
        data (List[Dict[str, Any]]): 要写入的数据
        file_path (Union[str, Path]): 输出文件路径
        delimiter (str, optional): 分隔符. Defaults to ','.
    
    Examples:
        >>> write_csv([{'name': 'Alice', 'age': 25}], 'output.csv')
    """
    if not data:
        return
    
    fieldnames = data[0].keys()
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter=delimiter)
        writer.writeheader()
        writer.writerows(data)