"""
jpy-utils 安装配置文件
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="jpy-utils",
    version="0.1.0",
    author="Your Name",
    author_email="your-email@example.com",
    description="一个个人Python工具函数仓库，包含日常开发中常用的实用工具函数",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/jpy-utils",
    project_urls={
        "Bug Tracker": "https://github.com/your-username/jpy-utils/issues",
        "Documentation": "https://github.com/your-username/jpy-utils/blob/main/README.md",
        "Source Code": "https://github.com/your-username/jpy-utils",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
        "visualization": [
            "plotly>=5.0.0",
        ],
        "system": [
            "psutil>=5.8.0",
        ],
    },
    keywords="utils, tools, python, utilities, helper",
    include_package_data=True,
    zip_safe=False,
)