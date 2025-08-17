"""
颜色处理相关的工具函数

提供RGB、HEX、HSL等颜色格式转换和颜色分析功能。
"""

import random
import colorsys
from typing import Tuple, Union, List


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    16进制颜色转RGB
    
    Args:
        hex_color (str): 16进制颜色值（如 "#FF0000" 或 "FF0000"）
    
    Returns:
        Tuple[int, int, int]: RGB值元组
    
    Raises:
        ValueError: 无效的16进制颜色格式
    
    Examples:
        >>> hex_to_rgb("#FF0000")
        (255, 0, 0)
        >>> hex_to_rgb("00FF00")
        (0, 255, 0)
    """
    # 移除可能的 # 前缀
    hex_color = hex_color.lstrip('#')
    
    # 验证长度
    if len(hex_color) != 6:
        raise ValueError(f"Invalid hex color format: {hex_color}")
    
    try:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        raise ValueError(f"Invalid hex color format: {hex_color}")


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    RGB转16进制颜色
    
    Args:
        r (int): 红色值 (0-255)
        g (int): 绿色值 (0-255)
        b (int): 蓝色值 (0-255)
    
    Returns:
        str: 16进制颜色值
    
    Raises:
        ValueError: RGB值超出有效范围
    
    Examples:
        >>> rgb_to_hex(255, 0, 0)
        '#FF0000'
        >>> rgb_to_hex(0, 255, 0)
        '#00FF00'
    """
    # 验证RGB值范围
    for value, name in [(r, 'red'), (g, 'green'), (b, 'blue')]:
        if not 0 <= value <= 255:
            raise ValueError(f"Invalid {name} value: {value}. Must be 0-255.")
    
    return f"#{r:02X}{g:02X}{b:02X}"


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """
    RGB转HSL
    
    Args:
        r (int): 红色值 (0-255)
        g (int): 绿色值 (0-255)
        b (int): 蓝色值 (0-255)
    
    Returns:
        Tuple[int, int, int]: HSL值元组 (H: 0-360, S: 0-100, L: 0-100)
    
    Examples:
        >>> rgb_to_hsl(255, 0, 0)
        (0, 100, 50)
    """
    r, g, b = r/255.0, g/255.0, b/255.0
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    
    # 转换为标准HSL格式
    h = int(h * 360)
    s = int(s * 100)
    l = int(l * 100)
    
    return (h, s, l)


def hsl_to_rgb(h: int, s: int, l: int) -> Tuple[int, int, int]:
    """
    HSL转RGB
    
    Args:
        h (int): 色调 (0-360)
        s (int): 饱和度 (0-100)
        l (int): 亮度 (0-100)
    
    Returns:
        Tuple[int, int, int]: RGB值元组
    
    Examples:
        >>> hsl_to_rgb(0, 100, 50)
        (255, 0, 0)
    """
    h = h / 360.0
    s = s / 100.0
    l = l / 100.0
    
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    
    return (int(r * 255), int(g * 255), int(b * 255))


def random_color(format_type: str = "hex") -> Union[str, Tuple[int, int, int]]:
    """
    生成随机颜色
    
    Args:
        format_type (str, optional): 返回格式 ("hex", "rgb", "hsl"). Defaults to "hex".
    
    Returns:
        Union[str, Tuple[int, int, int]]: 随机颜色值
    
    Examples:
        >>> random_color("hex")
        '#A3B5C7'
        >>> random_color("rgb")
        (163, 181, 199)
    """
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    
    if format_type.lower() == "hex":
        return rgb_to_hex(r, g, b)
    elif format_type.lower() == "rgb":
        return (r, g, b)
    elif format_type.lower() == "hsl":
        return rgb_to_hsl(r, g, b)
    else:
        raise ValueError(f"Unsupported format: {format_type}")


def color_distance(color1: Union[str, Tuple[int, int, int]], 
                  color2: Union[str, Tuple[int, int, int]]) -> float:
    """
    计算两个颜色之间的欧几里得距离
    
    Args:
        color1 (Union[str, Tuple[int, int, int]]): 第一个颜色
        color2 (Union[str, Tuple[int, int, int]]): 第二个颜色
    
    Returns:
        float: 颜色距离
    
    Examples:
        >>> color_distance("#FF0000", "#00FF00")
        360.62
        >>> color_distance((255, 0, 0), (0, 255, 0))
        360.62
    """
    # 转换为RGB格式
    if isinstance(color1, str):
        r1, g1, b1 = hex_to_rgb(color1)
    else:
        r1, g1, b1 = color1
    
    if isinstance(color2, str):
        r2, g2, b2 = hex_to_rgb(color2)
    else:
        r2, g2, b2 = color2
    
    # 计算欧几里得距离
    return ((r2 - r1) ** 2 + (g2 - g1) ** 2 + (b2 - b1) ** 2) ** 0.5


def lighten_color(color: Union[str, Tuple[int, int, int]], amount: float = 0.1) -> Union[str, Tuple[int, int, int]]:
    """
    使颜色变亮
    
    Args:
        color (Union[str, Tuple[int, int, int]]): 原始颜色
        amount (float, optional): 变亮程度 (0.0-1.0). Defaults to 0.1.
    
    Returns:
        Union[str, Tuple[int, int, int]]: 变亮后的颜色（与输入格式相同）
    
    Examples:
        >>> lighten_color("#808080", 0.2)
        '#A3A3A3'
        >>> lighten_color((128, 128, 128), 0.2)
        (163, 163, 163)
    """
    is_hex = isinstance(color, str)
    
    if is_hex:
        r, g, b = hex_to_rgb(color)
    else:
        r, g, b = color
    
    # 转换为HSL，增加亮度
    h, s, l = rgb_to_hsl(r, g, b)
    l = min(100, l + int(amount * 100))
    
    # 转回RGB
    new_r, new_g, new_b = hsl_to_rgb(h, s, l)
    
    if is_hex:
        return rgb_to_hex(new_r, new_g, new_b)
    else:
        return (new_r, new_g, new_b)


def darken_color(color: Union[str, Tuple[int, int, int]], amount: float = 0.1) -> Union[str, Tuple[int, int, int]]:
    """
    使颜色变暗
    
    Args:
        color (Union[str, Tuple[int, int, int]]): 原始颜色
        amount (float, optional): 变暗程度 (0.0-1.0). Defaults to 0.1.
    
    Returns:
        Union[str, Tuple[int, int, int]]: 变暗后的颜色（与输入格式相同）
    
    Examples:
        >>> darken_color("#808080", 0.2)
        '#4D4D4D'
        >>> darken_color((128, 128, 128), 0.2)
        (77, 77, 77)
    """
    is_hex = isinstance(color, str)
    
    if is_hex:
        r, g, b = hex_to_rgb(color)
    else:
        r, g, b = color
    
    # 转换为HSL，减少亮度
    h, s, l = rgb_to_hsl(r, g, b)
    l = max(0, l - int(amount * 100))
    
    # 转回RGB
    new_r, new_g, new_b = hsl_to_rgb(h, s, l)
    
    if is_hex:
        return rgb_to_hex(new_r, new_g, new_b)
    else:
        return (new_r, new_g, new_b)


def get_complementary_color(color: Union[str, Tuple[int, int, int]]) -> Union[str, Tuple[int, int, int]]:
    """
    获取互补色
    
    Args:
        color (Union[str, Tuple[int, int, int]]): 原始颜色
    
    Returns:
        Union[str, Tuple[int, int, int]]: 互补色（与输入格式相同）
    
    Examples:
        >>> get_complementary_color("#FF0000")
        '#00FFFF'
        >>> get_complementary_color((255, 0, 0))
        (0, 255, 255)
    """
    is_hex = isinstance(color, str)
    
    if is_hex:
        r, g, b = hex_to_rgb(color)
    else:
        r, g, b = color
    
    # 转换为HSL，色调偏移180度
    h, s, l = rgb_to_hsl(r, g, b)
    h = (h + 180) % 360
    
    # 转回RGB
    new_r, new_g, new_b = hsl_to_rgb(h, s, l)
    
    if is_hex:
        return rgb_to_hex(new_r, new_g, new_b)
    else:
        return (new_r, new_g, new_b)


def generate_color_palette(base_color: Union[str, Tuple[int, int, int]], 
                          count: int = 5, variation: str = "analogous") -> List[Union[str, Tuple[int, int, int]]]:
    """
    基于基础颜色生成调色板
    
    Args:
        base_color (Union[str, Tuple[int, int, int]]): 基础颜色
        count (int, optional): 颜色数量. Defaults to 5.
        variation (str, optional): 变化类型 ("analogous", "monochromatic", "triadic"). Defaults to "analogous".
    
    Returns:
        List[Union[str, Tuple[int, int, int]]]: 调色板
    
    Examples:
        >>> generate_color_palette("#FF0000", 3, "analogous")
        ['#FF0000', '#FF8000', '#FFFF00']
    """
    is_hex = isinstance(base_color, str)
    
    if is_hex:
        r, g, b = hex_to_rgb(base_color)
    else:
        r, g, b = base_color
    
    h, s, l = rgb_to_hsl(r, g, b)
    palette = []
    
    if variation == "analogous":
        # 相邻色：色调在±30度范围内变化
        step = 60 / (count - 1) if count > 1 else 0
        for i in range(count):
            new_h = (h - 30 + i * step) % 360
            new_r, new_g, new_b = hsl_to_rgb(new_h, s, l)
            if is_hex:
                palette.append(rgb_to_hex(new_r, new_g, new_b))
            else:
                palette.append((new_r, new_g, new_b))
    
    elif variation == "monochromatic":
        # 单色：改变亮度和饱和度
        for i in range(count):
            factor = i / (count - 1) if count > 1 else 0
            new_s = max(10, min(100, s + (factor - 0.5) * 40))
            new_l = max(10, min(90, l + (factor - 0.5) * 40))
            new_r, new_g, new_b = hsl_to_rgb(h, int(new_s), int(new_l))
            if is_hex:
                palette.append(rgb_to_hex(new_r, new_g, new_b))
            else:
                palette.append((new_r, new_g, new_b))
    
    elif variation == "triadic":
        # 三色：120度间隔
        angles = [0, 120, 240]
        for i in range(min(count, 3)):
            new_h = (h + angles[i]) % 360
            new_r, new_g, new_b = hsl_to_rgb(new_h, s, l)
            if is_hex:
                palette.append(rgb_to_hex(new_r, new_g, new_b))
            else:
                palette.append((new_r, new_g, new_b))
        
        # 如果需要更多颜色，添加变体
        while len(palette) < count:
            base_idx = len(palette) % 3
            factor = (len(palette) // 3 + 1) * 0.2
            base_h = (h + angles[base_idx]) % 360
            new_l = max(10, min(90, l + factor * 40))
            new_r, new_g, new_b = hsl_to_rgb(base_h, s, int(new_l))
            if is_hex:
                palette.append(rgb_to_hex(new_r, new_g, new_b))
            else:
                palette.append((new_r, new_g, new_b))
    
    return palette


def is_dark_color(color: Union[str, Tuple[int, int, int]], threshold: int = 128) -> bool:
    """
    判断颜色是否为深色
    
    Args:
        color (Union[str, Tuple[int, int, int]]): 颜色值
        threshold (int, optional): 亮度阈值. Defaults to 128.
    
    Returns:
        bool: 是否为深色
    
    Examples:
        >>> is_dark_color("#000000")
        True
        >>> is_dark_color("#FFFFFF")
        False
    """
    if isinstance(color, str):
        r, g, b = hex_to_rgb(color)
    else:
        r, g, b = color
    
    # 计算感知亮度
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return luminance < threshold