#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KUKA 机器人轨迹数据探索分析

本脚本用于分析KUKA机器人的轨迹数据，通过深入的数据探索和可视化来理解机器人的运行状态、性能表现和潜在问题。

使用说明：
1. 修改 ANALYSIS_AXIS 变量来分析不同的轴 (1-6)
2. 修改数据库配置 DB_CONFIG 
3. 运行脚本进行分析

作者: AI Assistant
日期: 2024
"""

# 数据处理和分析
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings('ignore')
import os
from datetime import datetime

# 可视化库
import matplotlib.pyplot as plt
import seaborn as sns
try:
    import plotly.graph_objects as go
    import plotly.express as px
    from plotly.subplots import make_subplots
    import plotly.io as pio
    pio.templates.default = "plotly_white"
    PLOTLY_AVAILABLE = True
except ImportError:
    print("Plotly not available, using matplotlib only")
    PLOTLY_AVAILABLE = False

# 科学计算和机器学习
from scipy import stats
try:
    from scipy.signal import savgol_filter
    SAVGOL_AVAILABLE = True
except ImportError:
    SAVGOL_AVAILABLE = False
    
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score

# 设置可视化样式
try:
    plt.style.use('seaborn-v0_8')
except:
    try:
        plt.style.use('seaborn')
    except:
        print("警告: seaborn样式不可用，使用默认样式")
        
sns.set_palette("husl")

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 设置图表显示参数
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['figure.dpi'] = 100

print("✅ 所有必要的库已成功导入")

# =============================================================================
# 配置参数
# =============================================================================

# 设置分析参数
ANALYSIS_AXIS = 1  # 当前分析的轴编号 (1-6)，可修改此值来分析不同的轴
SAMPLE_SIZE = 1000  # 数据样本大小

# 数据库连接配置 - 请根据实际情况修改
DB_CONFIG = {
    'host': 'localhost',  # 数据库主机
    'port': 5432,         # 端口号
    'database': 'robot_db',  # 数据库名称
    'username': 'your_username',  # 用户名
    'password': 'your_password'   # 密码
}

# =============================================================================
# 数据库连接和数据加载函数
# =============================================================================

def create_db_engine(config=None):
    """
    创建数据库连接引擎
    """
    if config is None:
        config = DB_CONFIG
    
    try:
        # 支持多种数据库类型
        if 'sqlite' in config.get('database', '').lower():
            connection_string = f"sqlite:///{config['database']}"
        else:
            connection_string = f"postgresql://{config['username']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
        
        # 创建数据库引擎
        engine = create_engine(connection_string, pool_pre_ping=True)
        
        # 测试连接
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        
        print("✅ 数据库连接成功")
        return engine
        
    except Exception as e:
        print(f"❌ 数据库连接失败: {e}")
        print("💡 提示：将使用模拟数据进行演示")
        return None

def generate_mock_data(n_samples=1000, n_robots=3, random_seed=42):
    """
    生成模拟KUKA机器人数据
    """
    np.random.seed(random_seed)
    
    print(f"🎭 生成 {n_samples} 个数据点的模拟KUKA机器人数据...")
    
    # 生成基础数据
    df = pd.DataFrame({
        'id': range(1, n_samples + 1),
        'ins_id': np.random.choice(range(1, n_robots + 1), n_samples),
        'trace_id': np.random.choice(range(1, 21), n_samples),
        'zeit': np.linspace(0, 100, n_samples) + np.random.normal(0, 0.001, n_samples),
        'prog_num': np.random.choice([100, 200, 300, 400], n_samples),
        'point_name': [f'P{i:03d}' for i in np.random.choice(range(1, 101), n_samples)],
        'motion_type': np.random.choice(['LIN', 'PTP', 'CIRC'], n_samples, p=[0.5, 0.3, 0.2]),
    })
    
    # 生成更真实的轨迹数据
    t = df['zeit'].values
    
    # 笛卡尔坐标 - 模拟复杂的3D轨迹
    df['x_act'] = 500 + 100 * np.sin(t * 0.1) + 50 * np.cos(t * 0.05) + np.random.normal(0, 2, n_samples)
    df['y_act'] = 200 + 80 * np.cos(t * 0.08) + 30 * np.sin(t * 0.12) + np.random.normal(0, 1.5, n_samples)
    df['z_act'] = 100 + 40 * np.sin(t * 0.06) + 20 * np.cos(t * 0.15) + np.random.normal(0, 1, n_samples)
    
    # 姿态角度
    df['a_act'] = 10 * np.sin(t * 0.03) + np.random.normal(0, 2, n_samples)
    df['b_act'] = 90 + 20 * np.cos(t * 0.04) + np.random.normal(0, 3, n_samples)
    df['c_act'] = 5 * np.sin(t * 0.07) + np.random.normal(0, 1.5, n_samples)
    
    # 关节轴位置 - 基于真实的KUKA机器人运动学
    joint_ranges = [(-170, 170), (-190, 45), (-120, 156), (-185, 185), (-120, 120), (-350, 350)]
    
    for i in range(1, 7):  # 6轴机器人
        center = (joint_ranges[i-1][0] + joint_ranges[i-1][1]) / 2
        amplitude = (joint_ranges[i-1][1] - joint_ranges[i-1][0]) / 6
        df[f'axis_pos_act{i}'] = center + amplitude * np.sin(t * 0.02 * i + i) + np.random.normal(0, 1, n_samples)
    
    # 笛卡尔速度
    df['cart_vel_act'] = np.abs(50 + 30 * np.sin(t * 0.05) + np.random.normal(0, 5, n_samples))
    
    # 为每个轴生成详细信息
    for axis in range(1, 7):
        base_pos = df[f'axis_pos_act{axis}']
        
        # 位置控制
        df[f'sollposition_{axis}'] = base_pos + np.random.normal(0, 0.05, n_samples)
        df[f'istposition_{axis}'] = base_pos
        df[f'positionsschleppfehler_{axis}'] = df[f'sollposition_{axis}'] - df[f'istposition_{axis}']
        
        # 速度控制
        velocity_base = np.gradient(base_pos, t)
        df[f'sollgeschwindigkeit_{axis}'] = velocity_base + np.random.normal(0, 0.5, n_samples)
        df[f'istgeschwindigkeit_{axis}'] = velocity_base + np.random.normal(0, 0.3, n_samples)
        df[f'geschwindigkeitsdifferenz_{axis}'] = df[f'sollgeschwindigkeit_{axis}'] - df[f'istgeschwindigkeit_{axis}']
        
        # 力矩控制
        df[f'sollmoment_{axis}'] = np.random.normal(0, 3, n_samples)
        df[f'istmoment_{axis}'] = df[f'sollmoment_{axis}'] + np.random.normal(0, 0.1, n_samples)
        
        # 温度模拟 - 考虑负载影响
        base_temp = 35 + axis * 2  # 不同轴的基础温度
        load_effect = np.abs(df[f'istmoment_{axis}']) * 0.5
        df[f'motortemperatur_{axis}'] = base_temp + load_effect + np.random.normal(0, 2, n_samples)
        
        # 电流模拟 - 与力矩相关
        df[f'iststrom_{axis}'] = np.abs(1.5 + df[f'istmoment_{axis}'] * 0.3 + np.random.normal(0, 0.2, n_samples))
    
    # 时间戳
    df['created_at'] = pd.Timestamp.now()
    
    print("✅ 模拟数据生成完成")
    return df

def get_axis_columns(df, axis_num):
    """
    获取指定轴的所有相关列名
    """
    axis_cols = {
        'sollposition': f'sollposition_{axis_num}',
        'istposition': f'istposition_{axis_num}',
        'positionsschleppfehler': f'positionsschleppfehler_{axis_num}',
        'sollgeschwindigkeit': f'sollgeschwindigkeit_{axis_num}',
        'istgeschwindigkeit': f'istgeschwindigkeit_{axis_num}',
        'geschwindigkeitsdifferenz': f'geschwindigkeitsdifferenz_{axis_num}',
        'sollmoment': f'sollmoment_{axis_num}',
        'istmoment': f'istmoment_{axis_num}',
        'motortemperatur': f'motortemperatur_{axis_num}',
        'iststrom': f'iststrom_{axis_num}',
        'axis_pos_act': f'axis_pos_act{axis_num}'
    }
    
    # 只返回在DataFrame中存在的列
    existing_cols = {k: v for k, v in axis_cols.items() if v in df.columns}
    
    return existing_cols

# =============================================================================
# 分析函数
# =============================================================================

def analyze_axis_position(df, axis_num):
    """
    分析指定轴的位置精度
    """
    print(f"🎯 轴{axis_num}位置精度分析")
    print("=" * 60)
    
    soll_pos_col = f'sollposition_{axis_num}'
    ist_pos_col = f'istposition_{axis_num}'
    follow_error_col = f'positionsschleppfehler_{axis_num}'
    
    if all(col in df.columns for col in [soll_pos_col, ist_pos_col]):
        # 计算位置误差
        calculated_error = df[soll_pos_col] - df[ist_pos_col]
        df[f'calculated_pos_error_{axis_num}'] = calculated_error
        
        print(f"\n🧮 计算的位置误差统计 (目标位置 - 实际位置):")
        print(f"   平均误差: {calculated_error.mean():.6f}°")
        print(f"   误差标准差: {calculated_error.std():.6f}°")
        print(f"   最大绝对误差: {calculated_error.abs().max():.6f}°")
        print(f"   RMS误差: {np.sqrt((calculated_error**2).mean()):.6f}°")
        
        # 可视化位置精度
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # 目标位置vs实际位置
        axes[0,0].plot(df['zeit'], df[soll_pos_col], label='目标位置', linewidth=2, alpha=0.8)
        axes[0,0].plot(df['zeit'], df[ist_pos_col], label='实际位置', linewidth=2, alpha=0.8)
        axes[0,0].set_title(f'轴{axis_num} 位置跟踪')
        axes[0,0].set_xlabel('时间 (s)')
        axes[0,0].set_ylabel('位置 (°)')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        
        # 位置误差时间序列
        axes[0,1].plot(df['zeit'], calculated_error, linewidth=1.5, alpha=0.8)
        axes[0,1].set_title(f'轴{axis_num} 位置误差时间序列')
        axes[0,1].set_xlabel('时间 (s)')
        axes[0,1].set_ylabel('误差 (°)')
        axes[0,1].grid(True, alpha=0.3)
        axes[0,1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        
        # 误差分布直方图
        axes[1,0].hist(calculated_error, bins=50, alpha=0.7, density=True)
        axes[1,0].set_title(f'轴{axis_num} 位置误差分布')
        axes[1,0].set_xlabel('误差 (°)')
        axes[1,0].set_ylabel('密度')
        axes[1,0].grid(True, alpha=0.3)
        
        # 绝对位置误差
        axes[1,1].plot(df['zeit'], calculated_error.abs(), linewidth=2)
        axes[1,1].set_title(f'轴{axis_num} 绝对位置误差')
        axes[1,1].set_xlabel('时间 (s)')
        axes[1,1].set_ylabel('绝对误差 (°)')
        axes[1,1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # 精度等级评估
        rms_error = np.sqrt((calculated_error**2).mean())
        print(f"\n📏 轴{axis_num}精度等级评估:")
        if rms_error < 0.01:
            print(f"   精度等级: 优秀 (RMS < 0.01°)")
        elif rms_error < 0.05:
            print(f"   精度等级: 良好 (RMS < 0.05°)")
        elif rms_error < 0.1:
            print(f"   精度等级: 一般 (RMS < 0.1°)")
        else:
            print(f"   精度等级: 需要改进 (RMS ≥ 0.1°)")
        
        print("=" * 60)
    else:
        print(f"❌ 轴{axis_num}缺少位置数据")

def analyze_axis_temperature_current(df, axis_num):
    """
    分析指定轴的温度和电流
    """
    temp_col = f'motortemperatur_{axis_num}'
    current_col = f'iststrom_{axis_num}'
    
    if temp_col in df.columns and current_col in df.columns:
        print(f"🌡️ 轴{axis_num}温度和电流监控分析")
        print("=" * 60)
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
        
        # 电机温度趋势
        ax1.plot(df['zeit'], df[temp_col], linewidth=2, alpha=0.8, color='red', label=f'轴{axis_num}温度')
        ax1.set_title(f'轴{axis_num} 电机温度趋势')
        ax1.set_xlabel('时间 (s)')
        ax1.set_ylabel('温度 (°C)')
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # 添加温度警告线
        ax1.axhline(y=60, color='orange', linestyle='--', alpha=0.7, label='警告温度 (60°C)')
        ax1.axhline(y=80, color='red', linestyle='--', alpha=0.7, label='危险温度 (80°C)')
        
        # 温度统计信息
        temp_mean = df[temp_col].mean()
        temp_max = df[temp_col].max()
        temp_std = df[temp_col].std()
        
        ax1.text(0.02, 0.98, f'平均: {temp_mean:.1f}°C\\n最高: {temp_max:.1f}°C\\n标准差: {temp_std:.1f}°C', 
                 transform=ax1.transAxes, verticalalignment='top', 
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # 电机电流趋势
        ax2.plot(df['zeit'], df[current_col], linewidth=2, alpha=0.8, color='blue', label=f'轴{axis_num}电流')
        ax2.set_title(f'轴{axis_num} 电机电流趋势')
        ax2.set_xlabel('时间 (s)')
        ax2.set_ylabel('电流 (A)')
        ax2.grid(True, alpha=0.3)
        ax2.legend()
        
        # 电流统计信息
        current_mean = df[current_col].mean()
        current_max = df[current_col].max()
        current_std = df[current_col].std()
        
        ax2.text(0.02, 0.98, f'平均: {current_mean:.2f}A\\n最大: {current_max:.2f}A\\n标准差: {current_std:.2f}A', 
                 transform=ax2.transAxes, verticalalignment='top',
                 bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
        # 温度与电流关系分析
        temp_current_corr = df[temp_col].corr(df[current_col])
        print(f"\n🔗 轴{axis_num}温度与电流关系分析:")
        print(f"   相关系数: {temp_current_corr:.4f}")
        
        if abs(temp_current_corr) > 0.7:
            print("   ✅ 温度与电流高度相关，符合预期")
        elif abs(temp_current_corr) > 0.3:
            print("   ⚠️ 温度与电流中度相关")
        else:
            print("   ❌ 温度与电流相关性较低，需要检查")
        
        # 健康状态评估
        print(f"\n🏥 轴{axis_num}健康状态评估:")
        
        if temp_max > 80:
            print("   🔥 温度警告: 电机温度过高，需要立即检查散热系统")
        elif temp_max > 60:
            print("   ⚠️ 温度注意: 电机温度偏高，建议检查负载和散热")
        else:
            print("   ✅ 温度正常: 电机温度在安全范围内")
        
        if current_max > current_mean + 3 * current_std:
            print("   ⚡ 电流异常: 检测到异常高电流，可能存在机械阻力")
        elif current_std / current_mean > 0.5:
            print("   ⚠️ 电流波动: 电流变化较大，建议检查负载稳定性")
        else:
            print("   ✅ 电流正常: 电流消耗稳定")
        
        print("=" * 60)
    else:
        if temp_col in df.columns:
            print(f"⚠️ 只有轴{axis_num}温度数据，缺少电流数据")
        elif current_col in df.columns:
            print(f"⚠️ 只有轴{axis_num}电流数据，缺少温度数据")
        else:
            print(f"❌ 轴{axis_num}缺少温度和电流数据")

def main():
    """
    主分析函数
    """
    print(f"🎯 当前分析轴: 轴{ANALYSIS_AXIS}")
    print(f"📊 样本大小: {SAMPLE_SIZE}")
    
    # 尝试连接数据库
    engine = create_db_engine()
    
    # 加载或生成数据
    try:
        # 尝试从数据库加载数据
        if engine is not None:
            df = pd.read_sql_query(f"SELECT * FROM trace_data LIMIT {SAMPLE_SIZE}", engine)
            data_source = "数据库"
            print(f"✅ 成功从数据库加载 {len(df)} 条记录")
        else:
            raise Exception("数据库连接失败")
            
    except Exception as e:
        print(f"❌ 无法连接到数据库: {e}")
        print("💡 使用模拟数据进行演示...")
        
        # 使用改进的模拟数据生成函数
        df = generate_mock_data(n_samples=SAMPLE_SIZE, n_robots=1, random_seed=42)
        data_source = "模拟数据"
    
    # 验证当前分析轴的数据完整性
    axis_cols = get_axis_columns(df, ANALYSIS_AXIS)
    missing_cols = [col for col in ['sollposition', 'istposition', 'positionsschleppfehler', 
                                    'sollgeschwindigkeit', 'istgeschwindigkeit', 'geschwindigkeitsdifferenz',
                                    'motortemperatur', 'iststrom'] 
                    if f'{col}_{ANALYSIS_AXIS}' not in df.columns]
    
    if missing_cols:
        print(f"⚠️ 轴{ANALYSIS_AXIS}缺少以下数据列: {missing_cols}")
    else:
        print(f"✅ 轴{ANALYSIS_AXIS}数据完整")
    
    print(f"\n📊 数据来源: {data_source}")
    print(f"📈 可用轴数据列: {len(axis_cols)}")
    print(f"📋 数据形状: {df.shape}")
    
    # 显示数据预览
    print(f"\n🔍 数据预览:")
    if len(df) > 0:
        # 只显示与当前分析轴相关的关键列
        preview_cols = ['zeit', 'motion_type'] + list(axis_cols.values())[:8]  # 限制显示列数
        available_cols = [col for col in preview_cols if col in df.columns]
        print(df[available_cols].head())
    else:
        print("❌ 数据为空")
        return
    
    # 数据基础统计分析
    print("\n" + "=" * 60)
    print("📊 KUKA 机器人轨迹数据统计概览")
    print("=" * 60)
    
    # 基础信息
    print(f"\n🔢 数据基础信息:")
    print(f"   总记录数: {len(df):,}")
    print(f"   字段数量: {len(df.columns)}")
    if 'zeit' in df.columns:
        print(f"   时间跨度: {df['zeit'].max() - df['zeit'].min():.2f} 秒")
    
    # 运动类型统计
    if 'motion_type' in df.columns:
        print(f"\n🔄 运动类型分布:")
        motion_counts = df['motion_type'].value_counts()
        for motion_type, count in motion_counts.items():
            print(f"   {motion_type}: {count:,} 条记录 ({count/len(df)*100:.1f}%)")
    
    # 轴专项统计分析
    if axis_cols:
        axis_data = df[[col for col in axis_cols.values() if col in df.columns]].copy()
        
        if not axis_data.empty:
            print(f"\n📈 轴{ANALYSIS_AXIS}详细统计信息:")
            print("=" * 80)
            
            axis_stats = axis_data.describe()
            print(axis_stats.round(4))
            
            # 温度和电流分析
            temp_col = f'motortemperatur_{ANALYSIS_AXIS}'
            current_col = f'iststrom_{ANALYSIS_AXIS}'
            
            if temp_col in df.columns:
                print(f"\n🌡️ 轴{ANALYSIS_AXIS}温度分析:")
                print(f"   平均温度: {df[temp_col].mean():.2f}°C")
                print(f"   最高温度: {df[temp_col].max():.2f}°C")
                print(f"   温度标准差: {df[temp_col].std():.2f}°C")
                
            if current_col in df.columns:
                print(f"\n⚡ 轴{ANALYSIS_AXIS}电流分析:")
                print(f"   平均电流: {df[current_col].mean():.3f}A")
                print(f"   最大电流: {df[current_col].max():.3f}A")
                print(f"   电流标准差: {df[current_col].std():.3f}A")
    
    # 执行详细分析
    print("\n" + "=" * 60)
    print("🔬 详细分析开始")
    print("=" * 60)
    
    # 位置精度分析
    analyze_axis_position(df, ANALYSIS_AXIS)
    
    # 温度和电流监控分析
    analyze_axis_temperature_current(df, ANALYSIS_AXIS)
    
    print("\n✅ 分析完成")
    print("=" * 60)

if __name__ == "__main__":
    main()