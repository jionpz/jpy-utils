"""
加密解密相关的工具函数

提供常用的哈希、编码、UUID生成等功能。
"""

import hashlib
import base64
import uuid
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


def base64_encode(text: Union[str, bytes]) -> str:
    """
    Base64编码
    
    Args:
        text (Union[str, bytes]): 要编码的文本或字节
    
    Returns:
        str: Base64编码后的字符串
    
    Examples:
        >>> base64_encode('hello world')
        'aGVsbG8gd29ybGQ='
    """
    if isinstance(text, str):
        text = text.encode('utf-8')
    return base64.b64encode(text).decode('utf-8')


def base64_decode(encoded_text: str) -> str:
    """
    Base64解码
    
    Args:
        encoded_text (str): Base64编码的字符串
    
    Returns:
        str: 解码后的字符串
    
    Raises:
        ValueError: Base64格式错误
    
    Examples:
        >>> base64_decode('aGVsbG8gd29ybGQ=')
        'hello world'
    """
    try:
        decoded_bytes = base64.b64decode(encoded_text)
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Invalid base64 string: {e}")


def generate_uuid() -> str:
    """
    生成UUID
    
    Returns:
        str: UUID字符串
    
    Examples:
        >>> uuid_str = generate_uuid()
        '123e4567-e89b-12d3-a456-426614174000'
    """
    return str(uuid.uuid4())


def generate_uuid_short() -> str:
    """
    生成短UUID（去除连字符）
    
    Returns:
        str: 短UUID字符串
    
    Examples:
        >>> short_uuid = generate_uuid_short()
        '123e4567e89b12d3a456426614174000'
    """
    return str(uuid.uuid4()).replace('-', '')


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


def simple_encrypt(text: str, shift: int = 3) -> str:
    """
    简单凯撒密码加密
    
    Args:
        text (str): 要加密的文本
        shift (int, optional): 位移量. Defaults to 3.
    
    Returns:
        str: 加密后的文本
    
    Examples:
        >>> simple_encrypt('hello', 3)
        'khoor'
    """
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
        else:
            result += char
    return result


def simple_decrypt(text: str, shift: int = 3) -> str:
    """
    简单凯撒密码解密
    
    Args:
        text (str): 要解密的文本
        shift (int, optional): 位移量. Defaults to 3.
    
    Returns:
        str: 解密后的文本
    
    Examples:
        >>> simple_decrypt('khoor', 3)
        'hello'
    """
    return simple_encrypt(text, -shift)


def generate_salt(length: int = 16) -> str:
    """
    生成随机盐值
    
    Args:
        length (int, optional): 盐值长度. Defaults to 16.
    
    Returns:
        str: 随机盐值（十六进制）
    
    Examples:
        >>> salt = generate_salt(8)
        'a1b2c3d4e5f6g7h8'
    """
    import secrets
    return secrets.token_hex(length)


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