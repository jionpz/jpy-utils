"""
HTTP请求工具
"""

import requests
from typing import Dict, Any, Optional


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