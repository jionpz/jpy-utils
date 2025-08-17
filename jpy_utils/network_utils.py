"""
网络请求相关的工具函数

提供常用的HTTP请求、文件下载、网络检测等功能。
"""

import json
import requests
from typing import Dict, Any, Optional, Union
from pathlib import Path


def simple_get(url: str, headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> requests.Response:
    """
    简单GET请求
    
    Args:
        url (str): 请求URL
        headers (Optional[Dict[str, str]], optional): 请求头. Defaults to None.
        timeout (int, optional): 超时时间. Defaults to 30.
    
    Returns:
        requests.Response: 响应对象
    
    Raises:
        requests.RequestException: 请求异常
    
    Examples:
        >>> response = simple_get('https://api.github.com/users/octocat')
        >>> response.json()
    """
    return requests.get(url, headers=headers, timeout=timeout)


def simple_post(url: str, data: Optional[Dict[str, Any]] = None, 
               json_data: Optional[Dict[str, Any]] = None,
               headers: Optional[Dict[str, str]] = None, timeout: int = 30) -> requests.Response:
    """
    简单POST请求
    
    Args:
        url (str): 请求URL
        data (Optional[Dict[str, Any]], optional): 表单数据. Defaults to None.
        json_data (Optional[Dict[str, Any]], optional): JSON数据. Defaults to None.
        headers (Optional[Dict[str, str]], optional): 请求头. Defaults to None.
        timeout (int, optional): 超时时间. Defaults to 30.
    
    Returns:
        requests.Response: 响应对象
    
    Examples:
        >>> response = simple_post('https://api.example.com/data', 
        ...                       json_data={'key': 'value'})
    """
    return requests.post(url, data=data, json=json_data, headers=headers, timeout=timeout)


def download_file(url: str, file_path: Union[str, Path], chunk_size: int = 8192) -> None:
    """
    下载文件
    
    Args:
        url (str): 文件URL
        file_path (Union[str, Path]): 保存路径
        chunk_size (int, optional): 分块大小. Defaults to 8192.
    
    Raises:
        requests.RequestException: 下载异常
    
    Examples:
        >>> download_file('https://example.com/file.zip', 'downloads/file.zip')
    """
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)


def check_url_status(url: str, timeout: int = 10) -> int:
    """
    检查URL状态码
    
    Args:
        url (str): 要检查的URL
        timeout (int, optional): 超时时间. Defaults to 10.
    
    Returns:
        int: HTTP状态码，异常时返回-1
    
    Examples:
        >>> status = check_url_status('https://www.google.com')
        200
    """
    try:
        response = requests.head(url, timeout=timeout)
        return response.status_code
    except requests.RequestException:
        return -1


def get_ip_info(ip: Optional[str] = None) -> Dict[str, Any]:
    """
    获取IP信息
    
    Args:
        ip (Optional[str], optional): IP地址，为None时获取本机IP信息. Defaults to None.
    
    Returns:
        Dict[str, Any]: IP信息
    
    Examples:
        >>> info = get_ip_info()
        {'ip': '1.2.3.4', 'country': 'US', 'city': 'New York'}
    """
    try:
        if ip:
            url = f"http://ip-api.com/json/{ip}"
        else:
            url = "http://ip-api.com/json/"
        
        response = requests.get(url, timeout=10)
        return response.json()
    except requests.RequestException:
        return {}


def is_url_accessible(url: str, timeout: int = 10) -> bool:
    """
    检查URL是否可访问
    
    Args:
        url (str): 要检查的URL
        timeout (int, optional): 超时时间. Defaults to 10.
    
    Returns:
        bool: 是否可访问
    
    Examples:
        >>> is_accessible = is_url_accessible('https://www.google.com')
        True
    """
    try:
        response = requests.head(url, timeout=timeout)
        return response.status_code < 400
    except requests.RequestException:
        return False


def get_json_from_url(url: str, headers: Optional[Dict[str, str]] = None, 
                     timeout: int = 30) -> Dict[str, Any]:
    """
    从URL获取JSON数据
    
    Args:
        url (str): JSON API URL
        headers (Optional[Dict[str, str]], optional): 请求头. Defaults to None.
        timeout (int, optional): 超时时间. Defaults to 30.
    
    Returns:
        Dict[str, Any]: JSON数据
    
    Raises:
        requests.RequestException: 请求异常
        json.JSONDecodeError: JSON解析异常
    
    Examples:
        >>> data = get_json_from_url('https://api.github.com/users/octocat')
    """
    response = simple_get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return response.json()


def url_encode_params(params: Dict[str, Any]) -> str:
    """
    URL参数编码
    
    Args:
        params (Dict[str, Any]): 参数字典
    
    Returns:
        str: 编码后的参数字符串
    
    Examples:
        >>> encoded = url_encode_params({'q': 'python programming', 'page': 1})
        'q=python%20programming&page=1'
    """
    from urllib.parse import urlencode
    return urlencode(params)


def parse_url(url: str) -> Dict[str, Any]:
    """
    解析URL组成部分
    
    Args:
        url (str): 要解析的URL
    
    Returns:
        Dict[str, Any]: URL组成部分
    
    Examples:
        >>> parts = parse_url('https://example.com:8080/path?query=value#fragment')
        {'scheme': 'https', 'netloc': 'example.com:8080', ...}
    """
    from urllib.parse import urlparse
    parsed = urlparse(url)
    return {
        'scheme': parsed.scheme,
        'netloc': parsed.netloc,
        'hostname': parsed.hostname,
        'port': parsed.port,
        'path': parsed.path,
        'params': parsed.params,
        'query': parsed.query,
        'fragment': parsed.fragment
    }