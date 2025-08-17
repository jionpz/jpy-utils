"""
加密解密相关的工具函数

提供常用的哈希、编码、UUID生成等功能。
"""

from .hashing import md5_hash, sha256_hash, sha1_hash, hash_with_salt
from .encoding import base64_encode, base64_decode
from .uuid_gen import generate_uuid, generate_uuid_short
from .simple_crypto import simple_encrypt, simple_decrypt
from .salt_gen import generate_salt

__all__ = [
    "md5_hash",
    "sha256_hash",
    "sha1_hash",
    "base64_encode",
    "base64_decode",
    "generate_uuid",
    "generate_uuid_short",
    "simple_encrypt",
    "simple_decrypt",
    "generate_salt",
    "hash_with_salt",
]