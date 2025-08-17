#!/bin/bash

# KUKA机器人轨迹数据分析系统 - 依赖安装脚本

echo "🚀 开始安装KUKA机器人轨迹数据分析系统依赖..."

# 更新包管理器
echo "📦 更新包管理器..."
sudo apt-get update -y

# 安装Python和pip
echo "🐍 安装Python和pip..."
sudo apt-get install -y python3 python3-pip python3-dev

# 安装基础科学计算包
echo "🔢 安装基础科学计算包..."
pip3 install --user numpy pandas scipy scikit-learn

# 安装可视化包
echo "📊 安装可视化包..."
pip3 install --user matplotlib seaborn plotly

# 安装数据库连接包
echo "🗄️ 安装数据库连接包..."
pip3 install --user sqlalchemy psycopg2-binary

# 安装Jupyter相关包
echo "📓 安装Jupyter相关包..."
pip3 install --user jupyter notebook ipywidgets

# 验证安装
echo "✅ 验证安装..."
python3 -c "
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import scipy
print('✅ 所有必要的包已成功安装')
print(f'   - Pandas: {pd.__version__}')
print(f'   - NumPy: {np.__version__}')
print(f'   - Scikit-learn: {sklearn.__version__}')
"

echo "🎉 安装完成！"
echo ""
echo "📋 使用说明："
echo "1. 运行Python分析脚本："
echo "   python3 kuka_advanced_analysis.py"
echo ""
echo "2. 启动Jupyter Notebook："
echo "   jupyter notebook"
echo ""
echo "3. 修改分析参数："
echo "   编辑脚本中的 ANALYSIS_AXIS 变量来分析不同的轴"