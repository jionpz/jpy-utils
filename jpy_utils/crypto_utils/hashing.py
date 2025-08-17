"""
哈希工具
"""

import hashlib
from typing import Union


def md5_hash(text: Union[str, bytes]) -> str:
    """
    计算MD5哈希值
    
    Args:
        text (Union[str, bytes]): 要哈希的文本或字节
    
    Returns:
        str: MD5哈希值（十六进制）
    
    Examples:
        >>> md5_hash('hello world')
        '5d41402abc4b2a76b9719d911017c592'
    """
    if isinstance(text, str):
        text = text.encode('utf-8')
    return hashlib.md5(text).hexdigest()


def sha256_hash(text: Union[str, bytes]) -> str:
    """
    计算SHA256哈希值
    
    Args:
        text (Union[str, bytes]): 要哈希的文本或字节
    
    Returns:
        str: SHA256哈希值（十六进制）
    
    Examples:
        >>> sha256_hash('hello world')
        'b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9'
    """
    if isinstance(text, str):
        text = text.encode('utf-8')
    return hashlib.sha256(text).hexdigest()


def sha1_hash(text: Union[str, bytes]) -> str:
    """
    计算SHA1哈希值
    
    Args:
        text (Union[str, bytes]): 要哈希的文本或字节
    
    Returns:
        str: SHA1哈希值（十六进制）
    
    Examples:
        >>> sha1_hash('hello world')
        '2aae6c35c94fcfb415dbe95f408b9ce91ee846ed'
    """
    if isinstance(text, str):
        text = text.encode('utf-8')
    return hashlib.sha1(text).hexdigest()


def hash_with_salt(text: str, salt: str) -> str:
    """
    使用盐值进行哈希
    
    Args:
        text (str): 要哈希的文本
        salt (str): 盐值
    
    Returns:
        str: 加盐哈希值
    
    Examples:
        >>> hashed = hash_with_salt('password', 'salt123')
        'a1b2c3d4...'
    """
    return sha256_hash(text + salt)