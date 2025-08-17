"""
文件操作相关的工具函数

提供常用的文件读写、目录操作等功能。
"""

import os
import json
import csv
from pathlib import Path
from typing import Any, Dict, List, Union


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


def get_file_size(file_path: Union[str, Path]) -> int:
    """
    获取文件大小（字节）
    
    Args:
        file_path (Union[str, Path]): 文件路径
    
    Returns:
        int: 文件大小（字节）
    
    Raises:
        FileNotFoundError: 文件不存在
    
    Examples:
        >>> size = get_file_size('example.txt')
        1024
    """
    return os.path.getsize(file_path)


def create_directory(dir_path: Union[str, Path], exist_ok: bool = True) -> None:
    """
    创建目录
    
    Args:
        dir_path (Union[str, Path]): 目录路径
        exist_ok (bool, optional): 如果目录已存在是否报错. Defaults to True.
    
    Examples:
        >>> create_directory('new_folder')
    """
    Path(dir_path).mkdir(parents=True, exist_ok=exist_ok)


def list_files(dir_path: Union[str, Path], pattern: str = "*") -> List[Path]:
    """
    列出目录下的文件
    
    Args:
        dir_path (Union[str, Path]): 目录路径
        pattern (str, optional): 文件模式. Defaults to "*".
    
    Returns:
        List[Path]: 文件路径列表
    
    Examples:
        >>> files = list_files('.', '*.py')
        [Path('main.py'), Path('utils.py')]
    """
    path = Path(dir_path)
    return list(path.glob(pattern))


def copy_file(src_path: Union[str, Path], dst_path: Union[str, Path]) -> None:
    """
    复制文件
    
    Args:
        src_path (Union[str, Path]): 源文件路径
        dst_path (Union[str, Path]): 目标文件路径
    
    Examples:
        >>> copy_file('source.txt', 'backup.txt')
    """
    import shutil
    shutil.copy2(src_path, dst_path)


def delete_file(file_path: Union[str, Path]) -> None:
    """
    删除文件
    
    Args:
        file_path (Union[str, Path]): 文件路径
    
    Examples:
        >>> delete_file('temp.txt')
    """
    Path(file_path).unlink(missing_ok=True)