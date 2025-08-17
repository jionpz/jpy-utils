"""
文件信息获取工具
"""

import os
from pathlib import Path
from typing import List, Union


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