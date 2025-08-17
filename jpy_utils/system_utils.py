"""
系统操作相关的工具函数

提供系统信息获取、内存监控、磁盘监控、命令执行等功能。
"""

import os
import platform
import subprocess
import psutil
from typing import Dict, Any, Optional, List, Union


def get_system_info() -> Dict[str, Any]:
    """
    获取系统信息
    
    Returns:
        Dict[str, Any]: 系统信息字典
    
    Examples:
        >>> info = get_system_info()
        {'platform': 'Linux', 'version': '5.4.0', 'architecture': 'x86_64', ...}
    """
    return {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'platform_release': platform.release(),
        'architecture': platform.machine(),
        'processor': platform.processor(),
        'python_version': platform.python_version(),
        'hostname': platform.node(),
        'cpu_count': os.cpu_count(),
        'current_user': os.getenv('USER', os.getenv('USERNAME', 'unknown'))
    }


def get_memory_usage() -> Dict[str, Union[int, float]]:
    """
    获取内存使用情况
    
    Returns:
        Dict[str, Union[int, float]]: 内存使用信息
    
    Examples:
        >>> memory = get_memory_usage()
        {'total': 8589934592, 'available': 4294967296, 'percent': 50.0, ...}
    """
    memory = psutil.virtual_memory()
    return {
        'total': memory.total,
        'available': memory.available,
        'used': memory.used,
        'free': memory.free,
        'percent': memory.percent,
        'total_gb': round(memory.total / (1024**3), 2),
        'available_gb': round(memory.available / (1024**3), 2),
        'used_gb': round(memory.used / (1024**3), 2)
    }


def get_disk_usage(path: str = "/") -> Dict[str, Union[int, float]]:
    """
    获取磁盘使用情况
    
    Args:
        path (str, optional): 磁盘路径. Defaults to "/".
    
    Returns:
        Dict[str, Union[int, float]]: 磁盘使用信息
    
    Examples:
        >>> disk = get_disk_usage('/')
        {'total': 1000000000, 'used': 500000000, 'free': 500000000, ...}
    """
    disk = psutil.disk_usage(path)
    return {
        'total': disk.total,
        'used': disk.used,
        'free': disk.free,
        'percent': round((disk.used / disk.total) * 100, 2),
        'total_gb': round(disk.total / (1024**3), 2),
        'used_gb': round(disk.used / (1024**3), 2),
        'free_gb': round(disk.free / (1024**3), 2)
    }


def run_command(command: Union[str, List[str]], timeout: Optional[int] = None, 
               capture_output: bool = True) -> Dict[str, Any]:
    """
    执行系统命令
    
    Args:
        command (Union[str, List[str]]): 要执行的命令
        timeout (Optional[int], optional): 超时时间（秒）. Defaults to None.
        capture_output (bool, optional): 是否捕获输出. Defaults to True.
    
    Returns:
        Dict[str, Any]: 执行结果
    
    Examples:
        >>> result = run_command('ls -la')
        {'returncode': 0, 'stdout': '...', 'stderr': '', 'success': True}
    """
    try:
        if isinstance(command, str):
            # 对于字符串命令，使用shell=True
            result = subprocess.run(
                command,
                shell=True,
                capture_output=capture_output,
                text=True,
                timeout=timeout
            )
        else:
            # 对于列表命令，不使用shell
            result = subprocess.run(
                command,
                capture_output=capture_output,
                text=True,
                timeout=timeout
            )
        
        return {
            'returncode': result.returncode,
            'stdout': result.stdout if capture_output else '',
            'stderr': result.stderr if capture_output else '',
            'success': result.returncode == 0
        }
    
    except subprocess.TimeoutExpired:
        return {
            'returncode': -1,
            'stdout': '',
            'stderr': 'Command timed out',
            'success': False
        }
    except Exception as e:
        return {
            'returncode': -1,
            'stdout': '',
            'stderr': str(e),
            'success': False
        }


def get_env_var(var_name: str, default: Any = None) -> Any:
    """
    获取环境变量
    
    Args:
        var_name (str): 环境变量名
        default (Any, optional): 默认值. Defaults to None.
    
    Returns:
        Any: 环境变量值或默认值
    
    Examples:
        >>> path = get_env_var('PATH')
        '/usr/bin:/bin:/usr/sbin:/sbin'
        >>> custom_var = get_env_var('MY_VAR', 'default_value')
        'default_value'
    """
    return os.getenv(var_name, default)


def set_env_var(var_name: str, value: str) -> None:
    """
    设置环境变量
    
    Args:
        var_name (str): 环境变量名
        value (str): 环境变量值
    
    Examples:
        >>> set_env_var('MY_VAR', 'my_value')
    """
    os.environ[var_name] = value


def get_cpu_usage(interval: float = 1.0) -> float:
    """
    获取CPU使用率
    
    Args:
        interval (float, optional): 采样间隔（秒）. Defaults to 1.0.
    
    Returns:
        float: CPU使用率百分比
    
    Examples:
        >>> cpu_percent = get_cpu_usage()
        25.6
    """
    return psutil.cpu_percent(interval=interval)


def get_network_info() -> Dict[str, Any]:
    """
    获取网络接口信息
    
    Returns:
        Dict[str, Any]: 网络接口信息
    
    Examples:
        >>> network = get_network_info()
        {'interfaces': {'eth0': {'ip': '192.168.1.100', ...}}}
    """
    interfaces = {}
    
    for interface_name, addresses in psutil.net_if_addrs().items():
        interface_info = {
            'addresses': [],
            'is_up': interface_name in psutil.net_if_stats()
        }
        
        for addr in addresses:
            if addr.family.name == 'AF_INET':  # IPv4
                interface_info['addresses'].append({
                    'type': 'IPv4',
                    'address': addr.address,
                    'netmask': addr.netmask,
                    'broadcast': addr.broadcast
                })
            elif addr.family.name == 'AF_INET6':  # IPv6
                interface_info['addresses'].append({
                    'type': 'IPv6',
                    'address': addr.address,
                    'netmask': addr.netmask
                })
        
        interfaces[interface_name] = interface_info
    
    return {'interfaces': interfaces}


def get_process_info(pid: Optional[int] = None) -> Dict[str, Any]:
    """
    获取进程信息
    
    Args:
        pid (Optional[int], optional): 进程ID，为None时返回当前进程信息. Defaults to None.
    
    Returns:
        Dict[str, Any]: 进程信息
    
    Examples:
        >>> proc_info = get_process_info()
        {'pid': 1234, 'name': 'python', 'memory_percent': 2.5, ...}
    """
    try:
        if pid is None:
            process = psutil.Process()
        else:
            process = psutil.Process(pid)
        
        return {
            'pid': process.pid,
            'name': process.name(),
            'status': process.status(),
            'memory_percent': process.memory_percent(),
            'cpu_percent': process.cpu_percent(),
            'create_time': process.create_time(),
            'num_threads': process.num_threads(),
            'username': process.username() if hasattr(process, 'username') else 'unknown'
        }
    except psutil.NoSuchProcess:
        return {'error': f'Process with PID {pid} not found'}
    except Exception as e:
        return {'error': str(e)}


def kill_process(pid: int, force: bool = False) -> Dict[str, Any]:
    """
    终止进程
    
    Args:
        pid (int): 进程ID
        force (bool, optional): 是否强制终止. Defaults to False.
    
    Returns:
        Dict[str, Any]: 操作结果
    
    Examples:
        >>> result = kill_process(1234)
        {'success': True, 'message': 'Process terminated'}
    """
    try:
        process = psutil.Process(pid)
        
        if force:
            process.kill()
            message = "Process killed forcefully"
        else:
            process.terminate()
            message = "Process terminated gracefully"
        
        return {'success': True, 'message': message}
    
    except psutil.NoSuchProcess:
        return {'success': False, 'message': f'Process with PID {pid} not found'}
    except psutil.AccessDenied:
        return {'success': False, 'message': 'Access denied'}
    except Exception as e:
        return {'success': False, 'message': str(e)}


def get_running_processes() -> List[Dict[str, Any]]:
    """
    获取正在运行的进程列表
    
    Returns:
        List[Dict[str, Any]]: 进程信息列表
    
    Examples:
        >>> processes = get_running_processes()
        [{'pid': 1, 'name': 'systemd', 'memory_percent': 0.1}, ...]
    """
    processes = []
    
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent', 'cpu_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    return processes


def is_admin() -> bool:
    """
    检查是否具有管理员权限
    
    Returns:
        bool: 是否为管理员
    
    Examples:
        >>> is_admin()
        False
    """
    try:
        return os.getuid() == 0
    except AttributeError:
        # Windows系统
        import ctypes
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False