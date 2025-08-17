"""
数据处理相关的工具函数

提供常用的数据结构操作、转换、分析等功能。
"""

from typing import Any, Dict, List, Union, Iterator
import copy


def flatten_dict(data: Dict[str, Any], separator: str = '.') -> Dict[str, Any]:
    """
    扁平化嵌套字典
    
    Args:
        data (Dict[str, Any]): 嵌套字典
        separator (str, optional): 键分隔符. Defaults to '.'.
    
    Returns:
        Dict[str, Any]: 扁平化后的字典
    
    Examples:
        >>> flatten_dict({'a': {'b': {'c': 1}}})
        {'a.b.c': 1}
    """
    def _flatten(obj, parent_key='', sep='.'):
        items = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                items.extend(_flatten(v, new_key, sep=sep).items())
        else:
            return {parent_key: obj}
        return dict(items)
    
    return _flatten(data, sep=separator)


def deep_merge_dict(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    深度合并两个字典
    
    Args:
        dict1 (Dict[str, Any]): 第一个字典
        dict2 (Dict[str, Any]): 第二个字典
    
    Returns:
        Dict[str, Any]: 合并后的字典
    
    Examples:
        >>> deep_merge_dict({'a': {'b': 1}}, {'a': {'c': 2}})
        {'a': {'b': 1, 'c': 2}}
    """
    result = copy.deepcopy(dict1)
    
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dict(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    
    return result


def remove_duplicates(data_list: List[Any], key: str = None) -> List[Any]:
    """
    去除列表中的重复项
    
    Args:
        data_list (List[Any]): 原始列表
        key (str, optional): 对于字典列表，指定去重的键. Defaults to None.
    
    Returns:
        List[Any]: 去重后的列表
    
    Examples:
        >>> remove_duplicates([1, 2, 2, 3, 3, 4])
        [1, 2, 3, 4]
        >>> remove_duplicates([{'id': 1}, {'id': 2}, {'id': 1}], 'id')
        [{'id': 1}, {'id': 2}]
    """
    if not data_list:
        return []
    
    if key is None:
        # 对于简单类型，使用集合去重并保持顺序
        seen = set()
        result = []
        for item in data_list:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    else:
        # 对于字典列表，按指定键去重
        seen = set()
        result = []
        for item in data_list:
            if isinstance(item, dict) and key in item:
                key_value = item[key]
                if key_value not in seen:
                    seen.add(key_value)
                    result.append(item)
        return result


def chunk_list(data_list: List[Any], chunk_size: int) -> Iterator[List[Any]]:
    """
    将列表分块
    
    Args:
        data_list (List[Any]): 原始列表
        chunk_size (int): 块大小
    
    Yields:
        Iterator[List[Any]]: 分块后的列表迭代器
    
    Examples:
        >>> list(chunk_list([1, 2, 3, 4, 5], 2))
        [[1, 2], [3, 4], [5]]
    """
    for i in range(0, len(data_list), chunk_size):
        yield data_list[i:i + chunk_size]


def sort_dict_by_value(data_dict: Dict[Any, Any], reverse: bool = False) -> Dict[Any, Any]:
    """
    按值排序字典
    
    Args:
        data_dict (Dict[Any, Any]): 原始字典
        reverse (bool, optional): 是否降序排列. Defaults to False.
    
    Returns:
        Dict[Any, Any]: 排序后的字典
    
    Examples:
        >>> sort_dict_by_value({'a': 3, 'b': 1, 'c': 2})
        {'b': 1, 'c': 2, 'a': 3}
    """
    return dict(sorted(data_dict.items(), key=lambda x: x[1], reverse=reverse))


def group_by(data_list: List[Dict[str, Any]], key: str) -> Dict[Any, List[Dict[str, Any]]]:
    """
    按指定键对字典列表进行分组
    
    Args:
        data_list (List[Dict[str, Any]]): 字典列表
        key (str): 分组键
    
    Returns:
        Dict[Any, List[Dict[str, Any]]]: 分组后的字典
    
    Examples:
        >>> group_by([{'type': 'A', 'value': 1}, {'type': 'B', 'value': 2}, {'type': 'A', 'value': 3}], 'type')
        {'A': [{'type': 'A', 'value': 1}, {'type': 'A', 'value': 3}], 'B': [{'type': 'B', 'value': 2}]}
    """
    result = {}
    for item in data_list:
        if isinstance(item, dict) and key in item:
            group_key = item[key]
            if group_key not in result:
                result[group_key] = []
            result[group_key].append(item)
    return result


def find_in_list(data_list: List[Dict[str, Any]], **kwargs) -> List[Dict[str, Any]]:
    """
    在字典列表中查找匹配条件的项
    
    Args:
        data_list (List[Dict[str, Any]]): 字典列表
        **kwargs: 查找条件
    
    Returns:
        List[Dict[str, Any]]: 匹配的项列表
    
    Examples:
        >>> find_in_list([{'name': 'Alice', 'age': 25}, {'name': 'Bob', 'age': 30}], name='Alice')
        [{'name': 'Alice', 'age': 25}]
    """
    result = []
    for item in data_list:
        if isinstance(item, dict):
            match = True
            for key, value in kwargs.items():
                if key not in item or item[key] != value:
                    match = False
                    break
            if match:
                result.append(item)
    return result


def transpose_list(matrix: List[List[Any]]) -> List[List[Any]]:
    """
    转置二维列表
    
    Args:
        matrix (List[List[Any]]): 二维列表
    
    Returns:
        List[List[Any]]: 转置后的二维列表
    
    Examples:
        >>> transpose_list([[1, 2, 3], [4, 5, 6]])
        [[1, 4], [2, 5], [3, 6]]
    """
    if not matrix or not matrix[0]:
        return []
    return list(map(list, zip(*matrix)))


def calculate_stats(numbers: List[Union[int, float]]) -> Dict[str, float]:
    """
    计算数字列表的统计信息
    
    Args:
        numbers (List[Union[int, float]]): 数字列表
    
    Returns:
        Dict[str, float]: 统计信息（平均值、中位数、最大值、最小值等）
    
    Examples:
        >>> calculate_stats([1, 2, 3, 4, 5])
        {'mean': 3.0, 'median': 3.0, 'min': 1, 'max': 5, 'sum': 15, 'count': 5}
    """
    if not numbers:
        return {}
    
    sorted_numbers = sorted(numbers)
    count = len(numbers)
    
    # 中位数
    if count % 2 == 0:
        median = (sorted_numbers[count // 2 - 1] + sorted_numbers[count // 2]) / 2
    else:
        median = sorted_numbers[count // 2]
    
    return {
        'mean': sum(numbers) / count,
        'median': median,
        'min': min(numbers),
        'max': max(numbers),
        'sum': sum(numbers),
        'count': count
    }


def filter_dict(data_dict: Dict[str, Any], condition) -> Dict[str, Any]:
    """
    根据条件过滤字典
    
    Args:
        data_dict (Dict[str, Any]): 原始字典
        condition: 过滤条件函数
    
    Returns:
        Dict[str, Any]: 过滤后的字典
    
    Examples:
        >>> filter_dict({'a': 1, 'b': 2, 'c': 3}, lambda k, v: v > 1)
        {'b': 2, 'c': 3}
    """
    return {k: v for k, v in data_dict.items() if condition(k, v)}