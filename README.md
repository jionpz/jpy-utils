# jpy-utils

一个个人Python工具函数仓库，包含日常开发中常用的实用工具函数。

## 📋 目录

- [安装](#安装)
- [使用方法](#使用方法)
- [模块说明](#模块说明)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

## 🚀 安装

### 克隆仓库
```bash
git clone https://github.com/your-username/jpy-utils.git
cd jpy-utils
```

### 安装依赖
```bash
pip install -r requirements.txt
```

### 开发环境安装
```bash
pip install -e .
```

## 📖 使用方法

### 快速开始

```python
from jpy_utils import file_utils, string_utils, date_utils

# 文件操作示例
file_utils.read_json('config.json')
file_utils.write_csv(data, 'output.csv')

# 字符串处理示例
string_utils.camel_to_snake('CamelCase')  # 'camel_case'
string_utils.clean_text('  hello world  ')  # 'hello world'

# 日期处理示例
date_utils.format_datetime(datetime.now())
date_utils.get_timestamp()
```

## 📦 模块说明

### 🗂️ file_utils
文件操作相关的工具函数
- `read_json(file_path)` - 读取JSON文件
- `write_json(data, file_path)` - 写入JSON文件
- `read_csv(file_path)` - 读取CSV文件
- `write_csv(data, file_path)` - 写入CSV文件
- `get_file_size(file_path)` - 获取文件大小
- `create_directory(dir_path)` - 创建目录

### 🔤 string_utils
字符串处理相关的工具函数
- `camel_to_snake(text)` - 驼峰转下划线
- `snake_to_camel(text)` - 下划线转驼峰
- `clean_text(text)` - 清理文本空白字符
- `truncate_text(text, length)` - 截断文本
- `generate_random_string(length)` - 生成随机字符串
- `is_email(email)` - 验证邮箱格式

### 📅 date_utils
日期时间处理相关的工具函数
- `format_datetime(dt, format_str)` - 格式化日期时间
- `get_timestamp()` - 获取当前时间戳
- `timestamp_to_datetime(timestamp)` - 时间戳转日期时间
- `datetime_to_timestamp(dt)` - 日期时间转时间戳
- `get_date_range(start_date, end_date)` - 获取日期范围
- `add_days(dt, days)` - 日期加减天数

### 🌐 network_utils
网络请求相关的工具函数
- `simple_get(url, headers)` - 简单GET请求
- `simple_post(url, data, headers)` - 简单POST请求
- `download_file(url, file_path)` - 下载文件
- `check_url_status(url)` - 检查URL状态
- `get_ip_info()` - 获取IP信息

### 🔐 crypto_utils
加密解密相关的工具函数
- `md5_hash(text)` - MD5哈希
- `sha256_hash(text)` - SHA256哈希
- `base64_encode(text)` - Base64编码
- `base64_decode(text)` - Base64解码
- `generate_uuid()` - 生成UUID

### 📊 data_utils
数据处理相关的工具函数
- `flatten_dict(data)` - 扁平化字典
- `deep_merge_dict(dict1, dict2)` - 深度合并字典
- `remove_duplicates(data_list)` - 去除重复项
- `chunk_list(data_list, chunk_size)` - 分块列表
- `sort_dict_by_value(data_dict)` - 按值排序字典

### 🔧 system_utils
系统操作相关的工具函数
- `get_system_info()` - 获取系统信息
- `get_memory_usage()` - 获取内存使用情况
- `get_disk_usage(path)` - 获取磁盘使用情况
- `run_command(command)` - 执行系统命令
- `get_env_var(var_name, default)` - 获取环境变量

### 🎨 color_utils
颜色处理相关的工具函数
- `hex_to_rgb(hex_color)` - 16进制转RGB
- `rgb_to_hex(r, g, b)` - RGB转16进制
- `random_color()` - 生成随机颜色
- `color_distance(color1, color2)` - 计算颜色距离

## 📁 项目结构

```
jpy-utils/
├── jpy_utils/              # 主包目录
│   ├── __init__.py
│   ├── file_utils.py       # 文件操作工具
│   ├── string_utils.py     # 字符串处理工具
│   ├── date_utils.py       # 日期时间工具
│   ├── network_utils.py    # 网络请求工具
│   ├── crypto_utils.py     # 加密解密工具
│   ├── data_utils.py       # 数据处理工具
│   ├── system_utils.py     # 系统操作工具
│   └── color_utils.py      # 颜色处理工具
├── tests/                  # 测试目录
│   ├── __init__.py
│   ├── test_file_utils.py
│   ├── test_string_utils.py
│   └── ...
├── examples/               # 示例目录
│   ├── basic_usage.py
│   └── advanced_usage.py
├── docs/                   # 文档目录
├── requirements.txt        # 依赖文件
├── setup.py               # 安装配置
├── pytest.ini            # 测试配置
└── README.md              # 说明文档
```

## 🧪 测试

运行所有测试：
```bash
pytest
```

运行特定模块测试：
```bash
pytest tests/test_string_utils.py -v
```

运行测试覆盖率：
```bash
pytest --cov=jpy_utils
```

## 📝 开发指南

### 添加新的工具函数

1. 在相应的模块文件中添加函数
2. 添加详细的文档字符串
3. 编写相应的单元测试
4. 更新README文档

### 代码风格

- 使用 [Black](https://github.com/psf/black) 进行代码格式化
- 使用 [flake8](https://flake8.pycqa.org/) 进行代码检查
- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 编码规范

```bash
# 格式化代码
black jpy_utils/

# 代码检查
flake8 jpy_utils/
```

### 函数编写规范

```python
def function_name(param1: type, param2: type = default) -> return_type:
    """
    函数的简短描述
    
    Args:
        param1 (type): 参数1的描述
        param2 (type, optional): 参数2的描述. Defaults to default.
    
    Returns:
        return_type: 返回值的描述
    
    Raises:
        ExceptionType: 异常的描述
    
    Examples:
        >>> function_name('test', 123)
        'expected_result'
    """
    # 函数实现
    pass
```

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 这个仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的修改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开一个 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🔗 相关链接

- [Python官方文档](https://docs.python.org/3/)
- [PEP 8编码规范](https://www.python.org/dev/peps/pep-0008/)
- [pytest测试框架](https://pytest.org/)

## 📧 联系方式

如果您有任何问题或建议，请通过以下方式联系：

- 创建 [Issue](https://github.com/your-username/jpy-utils/issues)
- 发送邮件至: your-email@example.com

---

⭐ 如果这个项目对您有帮助，请给它一个星标！
