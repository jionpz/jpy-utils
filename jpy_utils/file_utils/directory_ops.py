"""
目录和文件操作工具
"""

import shutil
from pathlib import Path
from typing import Union


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


def copy_file(src_path: Union[str, Path], dst_path: Union[str, Path]) -> None:
    """
    复制文件
    
    Args:
        src_path (Union[str, Path]): 源文件路径
        dst_path (Union[str, Path]): 目标文件路径
    
    Examples:
        >>> copy_file('source.txt', 'backup.txt')
    """
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