#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KUKA 机器人轨迹数据高级分析

本脚本提供KUKA机器人的高级数据分析功能，包括：
- 速度精度深度分析
- 力矩和负载分析
- 异常检测和聚类分析
- 3D轨迹可视化
- 预测性维护建议

使用说明：
1. 修改 ANALYSIS_AXIS 变量来分析不同的轴 (1-6)
2. 修改数据库配置 DB_CONFIG 
3. 运行脚本进行高级分析

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
from mpl_toolkits.mplot3d import Axes3D

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
from scipy.signal import find_peaks, correlate
try:
    from scipy.signal import savgol_filter
    SAVGOL_AVAILABLE = True
except ImportError:
    SAVGOL_AVAILABLE = False
    
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans, DBSCAN
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
    'host': 'localhost',
    'port': 5432,
    'database': 'robot_db',
    'username': 'your_username',
    'password': 'your_password'
}

# =============================================================================
# 数据生成和工具函数
# =============================================================================

def generate_advanced_mock_data(n_samples=1000, n_robots=1, random_seed=42):
    """
    生成高级模拟KUKA机器人数据，包含更真实的运动模式和异常情况
    """
    np.random.seed(random_seed)
    
    print(f"🎭 生成 {n_samples} 个数据点的高级模拟KUKA机器人数据...")
    
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
    
    # 笛卡尔速度
    df['cart_vel_act'] = np.abs(50 + 30 * np.sin(t * 0.05) + np.random.normal(0, 5, n_samples))
    
    # 关节轴位置 - 基于真实的KUKA机器人运动学
    joint_ranges = [(-170, 170), (-190, 45), (-120, 156), (-185, 185), (-120, 120), (-350, 350)]
    
    for i in range(1, 7):  # 6轴机器人
        center = (joint_ranges[i-1][0] + joint_ranges[i-1][1]) / 2
        amplitude = (joint_ranges[i-1][1] - joint_ranges[i-1][0]) / 6
        
        # 添加一些异常情况
        anomaly_mask = np.random.random(n_samples) < 0.05  # 5%的异常数据
        normal_pos = center + amplitude * np.sin(t * 0.02 * i + i) + np.random.normal(0, 1, n_samples)
        anomaly_pos = normal_pos + np.random.normal(0, 10, n_samples) * anomaly_mask
        
        df[f'axis_pos_act{i}'] = np.where(anomaly_mask, anomaly_pos, normal_pos)
        
        # 为每个轴生成详细信息
        base_pos = df[f'axis_pos_act{i}']
        
        # 位置控制
        df[f'sollposition_{i}'] = base_pos + np.random.normal(0, 0.05, n_samples)
        df[f'istposition_{i}'] = base_pos
        df[f'positionsschleppfehler_{i}'] = df[f'sollposition_{i}'] - df[f'istposition_{i}']
        
        # 速度控制
        velocity_base = np.gradient(base_pos, t)
        df[f'sollgeschwindigkeit_{i}'] = velocity_base + np.random.normal(0, 0.5, n_samples)
        df[f'istgeschwindigkeit_{i}'] = velocity_base + np.random.normal(0, 0.3, n_samples)
        df[f'geschwindigkeitsdifferenz_{i}'] = df[f'sollgeschwindigkeit_{i}'] - df[f'istgeschwindigkeit_{i}']
        
        # 力矩控制 - 添加负载变化
        load_factor = 1 + 0.5 * np.sin(t * 0.01 * i)  # 周期性负载变化
        df[f'sollmoment_{i}'] = np.random.normal(0, 3, n_samples) * load_factor
        df[f'istmoment_{i}'] = df[f'sollmoment_{i}'] + np.random.normal(0, 0.1, n_samples)
        
        # 温度模拟 - 考虑负载和环境影响
        base_temp = 35 + i * 2
        load_effect = np.abs(df[f'istmoment_{i}']) * 0.5
        ambient_temp = 25 + 5 * np.sin(t * 0.001)  # 环境温度变化
        df[f'motortemperatur_{i}'] = base_temp + load_effect + ambient_temp + np.random.normal(0, 2, n_samples)
        
        # 电流模拟 - 与力矩和温度相关
        base_current = 1.5 + df[f'istmoment_{i}'] * 0.3
        temp_effect = (df[f'motortemperatur_{i}'] - 40) * 0.01  # 温度对电流的影响
        df[f'iststrom_{i}'] = np.abs(base_current + temp_effect + np.random.normal(0, 0.2, n_samples))
    
    # 时间戳
    df['created_at'] = pd.Timestamp.now()
    
    print("✅ 高级模拟数据生成完成")
    return df

def get_axis_columns(df, axis_num):
    """获取指定轴的所有相关列名"""
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
# 高级分析函数
# =============================================================================

def analyze_velocity_precision(df, axis_num):
    """
    速度精度深度分析
    """
    print(f"⚡ 轴{axis_num}速度精度深度分析")
    print("=" * 60)
    
    soll_vel_col = f'sollgeschwindigkeit_{axis_num}'
    ist_vel_col = f'istgeschwindigkeit_{axis_num}'
    vel_diff_col = f'geschwindigkeitsdifferenz_{axis_num}'
    
    if all(col in df.columns for col in [soll_vel_col, ist_vel_col]):
        # 1. 计算速度差分析
        calculated_vel_diff = df[soll_vel_col] - df[ist_vel_col]
        df[f'calculated_vel_diff_{axis_num}'] = calculated_vel_diff
        
        print(f"\n🧮 计算的速度差统计 (目标速度 - 实际速度):")
        print(f"   平均速度差: {calculated_vel_diff.mean():.6f}°/s")
        print(f"   速度差标准差: {calculated_vel_diff.std():.6f}°/s")
        print(f"   最大绝对速度差: {calculated_vel_diff.abs().max():.6f}°/s")
        print(f"   RMS速度差: {np.sqrt((calculated_vel_diff**2).mean()):.6f}°/s")
        
        # 2. 速度跟踪延迟分析
        if 'zeit' in df.columns and len(df) > 50:
            soll_vel_norm = (df[soll_vel_col] - df[soll_vel_col].mean()) / (df[soll_vel_col].std() + 1e-6)
            ist_vel_norm = (df[ist_vel_col] - df[ist_vel_col].mean()) / (df[ist_vel_col].std() + 1e-6)
            
            correlation = correlate(ist_vel_norm, soll_vel_norm, mode='full')
            delay_samples = np.argmax(correlation) - len(soll_vel_norm) + 1
            
            if len(df) > 1:
                time_step = (df['zeit'].iloc[-1] - df['zeit'].iloc[0]) / (len(df) - 1)
                delay_time = delay_samples * time_step
                print(f"\n⏱️ 速度跟踪延迟分析:")
                print(f"   估计延迟: {delay_time:.6f}秒 ({delay_samples}个采样点)")
        
        # 3. 速度精度可视化
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        
        # 目标速度vs实际速度
        axes[0,0].plot(df['zeit'], df[soll_vel_col], label='目标速度', linewidth=2, alpha=0.8)
        axes[0,0].plot(df['zeit'], df[ist_vel_col], label='实际速度', linewidth=2, alpha=0.8)
        axes[0,0].set_title(f'轴{axis_num} 速度跟踪')
        axes[0,0].set_xlabel('时间 (s)')
        axes[0,0].set_ylabel('速度 (°/s)')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        
        # 速度差时间序列
        axes[0,1].plot(df['zeit'], calculated_vel_diff, linewidth=1.5, alpha=0.8, color='red')
        axes[0,1].set_title(f'轴{axis_num} 速度差时间序列')
        axes[0,1].set_xlabel('时间 (s)')
        axes[0,1].set_ylabel('速度差 (°/s)')
        axes[0,1].grid(True, alpha=0.3)
        axes[0,1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        
        # 速度差分布直方图
        axes[0,2].hist(calculated_vel_diff, bins=50, alpha=0.7, density=True, color='red')
        axes[0,2].set_title(f'轴{axis_num} 速度差分布')
        axes[0,2].set_xlabel('速度差 (°/s)')
        axes[0,2].set_ylabel('密度')
        axes[0,2].grid(True, alpha=0.3)
        
        # 速度响应特性散点图
        axes[1,0].scatter(df[soll_vel_col], df[ist_vel_col], alpha=0.6, s=20)
        min_vel = min(df[soll_vel_col].min(), df[ist_vel_col].min())
        max_vel = max(df[soll_vel_col].max(), df[ist_vel_col].max())
        axes[1,0].plot([min_vel, max_vel], [min_vel, max_vel], 'r--', label='理想响应线')
        axes[1,0].set_title(f'轴{axis_num} 速度响应特性')
        axes[1,0].set_xlabel('目标速度 (°/s)')
        axes[1,0].set_ylabel('实际速度 (°/s)')
        axes[1,0].legend()
        axes[1,0].grid(True, alpha=0.3)
        
        # 速度变化率分析
        vel_acceleration = np.gradient(df[ist_vel_col], df['zeit'])
        axes[1,1].plot(df['zeit'], vel_acceleration, linewidth=1.5, alpha=0.8, color='green')
        axes[1,1].set_title(f'轴{axis_num} 速度变化率')
        axes[1,1].set_xlabel('时间 (s)')
        axes[1,1].set_ylabel('加速度 (°/s²)')
        axes[1,1].grid(True, alpha=0.3)
        
        # 速度稳定性分析
        window_size = min(50, len(df) // 10)
        if window_size > 5:
            rolling_std = df[ist_vel_col].rolling(window=window_size).std()
            axes[1,2].plot(df['zeit'], rolling_std, linewidth=2, alpha=0.8, color='purple')
            axes[1,2].set_title(f'轴{axis_num} 速度稳定性 (滚动标准差)')
            axes[1,2].set_xlabel('时间 (s)')
            axes[1,2].set_ylabel('速度标准差 (°/s)')
            axes[1,2].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
        
        # 4. 速度控制性能等级评估
        rms_vel_error = np.sqrt((calculated_vel_diff**2).mean())
        max_abs_vel_error = calculated_vel_diff.abs().max()
        
        print(f"\n📏 轴{axis_num}速度控制性能等级评估:")
        if rms_vel_error < 1.0:
            print(f"   速度控制等级: 优秀 (RMS < 1.0°/s)")
        elif rms_vel_error < 5.0:
            print(f"   速度控制等级: 良好 (RMS < 5.0°/s)")
        elif rms_vel_error < 10.0:
            print(f"   速度控制等级: 一般 (RMS < 10.0°/s)")
        else:
            print(f"   速度控制等级: 需要改进 (RMS ≥ 10.0°/s)")
        
        # 5. 速度稳定性分析
        vel_stability = df[ist_vel_col].std() / (abs(df[ist_vel_col].mean()) + 1e-6)
        print(f"\n📊 轴{axis_num}速度稳定性分析:")
        print(f"   速度变异系数: {vel_stability:.4f}")
        if vel_stability < 0.1:
            print("   速度稳定性: 优秀")
        elif vel_stability < 0.3:
            print("   速度稳定性: 良好") 
        else:
            print("   速度稳定性: 需要改进")
        
        print("=" * 60)
        
    else:
        print(f"❌ 轴{axis_num}缺少速度数据，无法进行速度精度分析")

def analyze_torque_load(df, axis_num):
    """
    力矩和负载深度分析
    """
    print(f"🔄 轴{axis_num}力矩和负载深度分析")
    print("=" * 60)
    
    soll_moment_col = f'sollmoment_{axis_num}'
    ist_moment_col = f'istmoment_{axis_num}'
    current_col = f'iststrom_{axis_num}'
    
    if all(col in df.columns for col in [soll_moment_col, ist_moment_col]):
        # 计算力矩误差
        moment_error = df[soll_moment_col] - df[ist_moment_col]
        df[f'moment_error_{axis_num}'] = moment_error
        
        print(f"\n📊 轴{axis_num}力矩统计信息:")
        print(f"   平均目标力矩: {df[soll_moment_col].mean():.4f} Nm")
        print(f"   平均实际力矩: {df[ist_moment_col].mean():.4f} Nm")
        print(f"   力矩误差RMS: {np.sqrt((moment_error**2).mean()):.4f} Nm")
        print(f"   最大绝对力矩误差: {moment_error.abs().max():.4f} Nm")
        
        # 可视化分析
        fig, axes = plt.subplots(2, 3, figsize=(20, 12))
        
        # 力矩跟踪
        axes[0,0].plot(df['zeit'], df[soll_moment_col], label='目标力矩', linewidth=2, alpha=0.8)
        axes[0,0].plot(df['zeit'], df[ist_moment_col], label='实际力矩', linewidth=2, alpha=0.8)
        axes[0,0].set_title(f'轴{axis_num} 力矩跟踪')
        axes[0,0].set_xlabel('时间 (s)')
        axes[0,0].set_ylabel('力矩 (Nm)')
        axes[0,0].legend()
        axes[0,0].grid(True, alpha=0.3)
        
        # 力矩误差时间序列
        axes[0,1].plot(df['zeit'], moment_error, linewidth=2, alpha=0.8, color='red')
        axes[0,1].set_title(f'轴{axis_num} 力矩误差')
        axes[0,1].set_xlabel('时间 (s)')
        axes[0,1].set_ylabel('力矩误差 (Nm)')
        axes[0,1].grid(True, alpha=0.3)
        axes[0,1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
        
        # 力矩分布
        axes[0,2].hist(df[ist_moment_col], bins=50, alpha=0.7, edgecolor='black')
        axes[0,2].set_title(f'轴{axis_num} 实际力矩分布')
        axes[0,2].set_xlabel('力矩 (Nm)')
        axes[0,2].set_ylabel('频次')
        axes[0,2].grid(True, alpha=0.3)
        
        # 负载分析
        moment_abs = df[ist_moment_col].abs()
        print(f"\n🏋️ 轴{axis_num}负载分析:")
        print(f"   平均负载: {moment_abs.mean():.4f} Nm")
        print(f"   峰值负载: {moment_abs.max():.4f} Nm")
        print(f"   负载变异系数: {moment_abs.std() / (moment_abs.mean() + 1e-6):.4f}")
        
        # 负载时间序列
        axes[1,0].plot(df['zeit'], moment_abs, linewidth=2, alpha=0.8, color='orange')
        axes[1,0].set_title(f'轴{axis_num} 负载时间序列')
        axes[1,0].set_xlabel('时间 (s)')
        axes[1,0].set_ylabel('绝对力矩 (Nm)')
        axes[1,0].grid(True, alpha=0.3)
        
        # 力矩vs电流关系（如果有电流数据）
        if current_col in df.columns:
            axes[1,1].scatter(df[ist_moment_col], df[current_col], alpha=0.6, s=20)
            axes[1,1].set_title(f'轴{axis_num} 力矩 vs 电流关系')
            axes[1,1].set_xlabel('实际力矩 (Nm)')
            axes[1,1].set_ylabel('电流 (A)')
            axes[1,1].grid(True, alpha=0.3)
            
            # 计算相关系数
            moment_current_corr = df[ist_moment_col].corr(df[current_col])
            axes[1,1].text(0.05, 0.95, f'相关系数: {moment_current_corr:.3f}', 
                          transform=axes[1,1].transAxes, verticalalignment='top',
                          bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            print(f"   力矩-电流相关系数: {moment_current_corr:.4f}")
        else:
            # 力矩误差分布
            axes[1,1].hist(moment_error, bins=50, alpha=0.7, edgecolor='black', color='red')
            axes[1,1].set_title(f'轴{axis_num} 力矩误差分布')
            axes[1,1].set_xlabel('力矩误差 (Nm)')
            axes[1,1].set_ylabel('频次')
            axes[1,1].grid(True, alpha=0.3)
        
        # 负载频谱分析
        if len(df) > 10:
            from scipy.fft import fft, fftfreq
            moment_fft = fft(moment_abs - moment_abs.mean())
            freqs = fftfreq(len(moment_abs), d=(df['zeit'].iloc[1] - df['zeit'].iloc[0]))
            
            # 只显示正频率部分
            positive_freqs = freqs[:len(freqs)//2]
            magnitude = np.abs(moment_fft[:len(freqs)//2])
            
            axes[1,2].plot(positive_freqs, magnitude)
            axes[1,2].set_title(f'轴{axis_num} 负载频谱分析')
            axes[1,2].set_xlabel('频率 (Hz)')
            axes[1,2].set_ylabel('幅值')
            axes[1,2].grid(True, alpha=0.3)
            axes[1,2].set_xlim(0, min(1.0, positive_freqs.max()))  # 限制显示范围
        
        plt.tight_layout()
        plt.show()
        
        # 负载等级评估
        peak_load_ratio = moment_abs.max() / (moment_abs.mean() + 1e-6)
        print(f"\n📊 轴{axis_num}负载等级评估:")
        if peak_load_ratio < 2.0:
            print("   负载特性: 稳定负载")
        elif peak_load_ratio < 5.0:
            print("   负载特性: 中等变化负载")
        else:
            print("   负载特性: 高变化负载")
        
        print("=" * 60)
        
    else:
        print(f"❌ 轴{axis_num}缺少力矩数据")

def detect_anomalies(df, axis_num=None):
    """
    异常检测分析
    """
    print("🚨 异常检测分析")
    print("=" * 60)
    
    # 选择关键特征进行异常检测
    feature_cols = []
    
    if axis_num:
        # 单轴分析
        axis_cols = get_axis_columns(df, axis_num)
        feature_cols = [col for col in axis_cols.values() if col in df.columns]
        print(f"   分析轴{axis_num}的异常情况")
    else:
        # 多轴分析
        # 添加笛卡尔坐标
        cartesian_cols = ['x_act', 'y_act', 'z_act']
        feature_cols.extend([col for col in cartesian_cols if col in df.columns])
        
        # 添加速度
        if 'cart_vel_act' in df.columns:
            feature_cols.append('cart_vel_act')
        
        # 添加温度数据
        temp_cols = [col for col in df.columns if 'motortemperatur' in col]
        feature_cols.extend(temp_cols[:3])  # 选择前3个轴的温度
        
        # 添加电流数据
        current_cols = [col for col in df.columns if 'iststrom' in col]
        feature_cols.extend(current_cols[:3])  # 选择前3个轴的电流
        
        print(f"   分析多轴系统异常情况")
    
    if len(feature_cols) >= 3:
        # 准备数据
        X = df[feature_cols].dropna()
        
        if len(X) > 10:  # 确保有足够的数据
            # 标准化数据
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # 异常检测
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            anomaly_labels = iso_forest.fit_predict(X_scaled)
            
            # 添加异常标签到原始数据
            df_analysis = df.loc[X.index].copy()
            df_analysis['anomaly'] = anomaly_labels
            df_analysis['anomaly_score'] = iso_forest.score_samples(X_scaled)
            
            # 统计异常点
            n_anomalies = (anomaly_labels == -1).sum()
            anomaly_rate = n_anomalies / len(anomaly_labels) * 100
            
            print(f"\n📊 异常检测结果:")
            print(f"   总样本数: {len(anomaly_labels)}")
            print(f"   异常点数量: {n_anomalies}")
            print(f"   异常率: {anomaly_rate:.2f}%")
            
            # 可视化异常检测结果
            if 'x_act' in df.columns and 'y_act' in df.columns:
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
                
                # 在轨迹图上标记异常点
                normal_data = df_analysis[df_analysis['anomaly'] == 1]
                anomaly_data = df_analysis[df_analysis['anomaly'] == -1]
                
                ax1.scatter(normal_data['x_act'], normal_data['y_act'], 
                           c='blue', alpha=0.6, s=10, label='正常点')
                ax1.scatter(anomaly_data['x_act'], anomaly_data['y_act'], 
                           c='red', alpha=0.8, s=20, label='异常点')
                ax1.set_xlabel('X轴位置 (mm)')
                ax1.set_ylabel('Y轴位置 (mm)')
                ax1.set_title('🎯 轨迹中的异常点检测')
                ax1.legend()
                ax1.grid(True, alpha=0.3)
                
                # 异常分数分布
                ax2.hist(df_analysis['anomaly_score'], bins=50, alpha=0.7, edgecolor='black')
                ax2.axvline(x=df_analysis[df_analysis['anomaly'] == -1]['anomaly_score'].max(), 
                           color='red', linestyle='--', label='异常阈值')
                ax2.set_xlabel('异常分数')
                ax2.set_ylabel('频次')
                ax2.set_title('📊 异常分数分布')
                ax2.legend()
                ax2.grid(True, alpha=0.3)
                
                plt.tight_layout()
                plt.show()
            
            # 显示最异常的几个点的详细信息
            top_anomalies = df_analysis[df_analysis['anomaly'] == -1].nsmallest(5, 'anomaly_score')
            if not top_anomalies.empty:
                print(f"\n🔍 最异常的5个数据点:")
                display_cols = ['zeit'] + feature_cols[:5] + ['anomaly_score']
                available_display_cols = [col for col in display_cols if col in top_anomalies.columns]
                print(top_anomalies[available_display_cols].round(3))
            
            print("=" * 60)
            return df_analysis
        else:
            print("❌ 数据量不足，无法进行异常检测")
            return df
    else:
        print("❌ 缺少足够的特征数据进行异常检测")
        return df

def create_3d_trajectory_visualization(df):
    """
    创建3D轨迹可视化
    """
    print("🎨 3D轨迹可视化")
    print("=" * 60)
    
    if all(col in df.columns for col in ['x_act', 'y_act', 'z_act']):
        if PLOTLY_AVAILABLE:
            # 使用Plotly创建交互式3D图
            fig = go.Figure(data=go.Scatter3d(
                x=df['x_act'],
                y=df['y_act'],
                z=df['z_act'],
                mode='markers+lines',
                marker=dict(
                    size=3,
                    color=df['zeit'],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="时间 (s)")
                ),
                line=dict(
                    color='darkblue',
                    width=2
                ),
                name='机器人轨迹'
            ))
            
            fig.update_layout(
                title='KUKA机器人3D轨迹',
                scene=dict(
                    xaxis_title='X轴位置 (mm)',
                    yaxis_title='Y轴位置 (mm)',
                    zaxis_title='Z轴位置 (mm)'
                ),
                width=800,
                height=600
            )
            
            fig.show()
            
        else:
            # 使用matplotlib创建3D图
            fig = plt.figure(figsize=(12, 9))
            ax = fig.add_subplot(111, projection='3d')
            
            # 绘制3D轨迹
            scatter = ax.scatter(df['x_act'], df['y_act'], df['z_act'], 
                               c=df['zeit'], cmap='viridis', s=20, alpha=0.7)
            ax.plot(df['x_act'], df['y_act'], df['z_act'], 
                   color='darkblue', linewidth=1, alpha=0.5)
            
            ax.set_xlabel('X轴位置 (mm)')
            ax.set_ylabel('Y轴位置 (mm)')
            ax.set_zlabel('Z轴位置 (mm)')
            ax.set_title('KUKA机器人3D轨迹')
            
            # 添加颜色条
            cbar = plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=20)
            cbar.set_label('时间 (s)')
            
            plt.tight_layout()
            plt.show()
        
        print("✅ 3D轨迹可视化完成")
    else:
        print("❌ 缺少3D坐标数据")
    
    print("=" * 60)

def generate_maintenance_recommendations(df, axis_num):
    """
    生成预测性维护建议
    """
    print(f"🔧 轴{axis_num}预测性维护建议")
    print("=" * 60)
    
    recommendations = []
    priority_scores = []
    
    # 温度分析
    temp_col = f'motortemperatur_{axis_num}'
    if temp_col in df.columns:
        avg_temp = df[temp_col].mean()
        max_temp = df[temp_col].max()
        temp_trend = np.polyfit(range(len(df)), df[temp_col], 1)[0]  # 温度趋势
        
        if max_temp > 80:
            recommendations.append("🔥 紧急：电机温度过高，立即检查散热系统和润滑状态")
            priority_scores.append(10)
        elif max_temp > 70:
            recommendations.append("⚠️ 高优先级：电机温度偏高，建议检查散热风扇和清洁散热器")
            priority_scores.append(8)
        elif avg_temp > 55:
            recommendations.append("💡 中优先级：平均工作温度偏高，建议优化工作负载")
            priority_scores.append(6)
        
        if temp_trend > 0.01:  # 温度上升趋势
            recommendations.append("📈 注意：检测到温度上升趋势，建议监控散热系统性能")
            priority_scores.append(7)
    
    # 电流分析
    current_col = f'iststrom_{axis_num}'
    if current_col in df.columns:
        avg_current = df[current_col].mean()
        max_current = df[current_col].max()
        current_std = df[current_col].std()
        
        if current_std / avg_current > 0.3:  # 电流波动大
            recommendations.append("⚡ 中优先级：电流波动较大，检查机械传动系统和负载稳定性")
            priority_scores.append(6)
        
        if max_current > avg_current + 3 * current_std:
            recommendations.append("🔧 高优先级：检测到异常高电流，可能存在机械阻力或磨损")
            priority_scores.append(8)
    
    # 位置精度分析
    pos_error_col = f'positionsschleppfehler_{axis_num}'
    if pos_error_col in df.columns:
        rms_error = np.sqrt((df[pos_error_col]**2).mean())
        max_error = df[pos_error_col].abs().max()
        
        if rms_error > 0.1:
            recommendations.append("🎯 中优先级：位置精度下降，建议校准轴控制参数")
            priority_scores.append(7)
        
        if max_error > 0.5:
            recommendations.append("📐 高优先级：最大位置误差过大，检查机械间隙和编码器")
            priority_scores.append(8)
    
    # 速度分析
    vel_col = f'istgeschwindigkeit_{axis_num}'
    if vel_col in df.columns:
        vel_stability = df[vel_col].std() / (abs(df[vel_col].mean()) + 1e-6)
        
        if vel_stability > 0.3:
            recommendations.append("🏃 中优先级：速度稳定性较差，检查控制系统参数")
            priority_scores.append(6)
    
    # 力矩分析
    moment_col = f'istmoment_{axis_num}'
    if moment_col in df.columns:
        moment_abs = df[moment_col].abs()
        peak_load_ratio = moment_abs.max() / (moment_abs.mean() + 1e-6)
        
        if peak_load_ratio > 5.0:
            recommendations.append("🏋️ 中优先级：负载变化剧烈，优化运动轨迹和速度曲线")
            priority_scores.append(6)
    
    # 综合健康评分
    if temp_col in df.columns and current_col in df.columns:
        temp_score = max(0, min(10, (80 - df[temp_col].mean()) / 5))  # 温度评分
        current_score = max(0, min(10, 10 - current_std / avg_current * 10))  # 电流稳定性评分
        
        health_score = (temp_score + current_score) / 2
        
        print(f"\n🏥 轴{axis_num}综合健康评分: {health_score:.1f}/10")
        
        if health_score < 4:
            print("   状态: 需要立即维护")
        elif health_score < 6:
            print("   状态: 需要计划维护")
        elif health_score < 8:
            print("   状态: 状态良好，定期检查")
        else:
            print("   状态: 优秀")
    
    # 输出建议
    if recommendations:
        print(f"\n📋 维护建议 (按优先级排序):")
        # 按优先级排序
        sorted_recommendations = sorted(zip(recommendations, priority_scores), 
                                      key=lambda x: x[1], reverse=True)
        
        for i, (rec, score) in enumerate(sorted_recommendations, 1):
            print(f"   {i}. {rec}")
    else:
        print(f"\n✅ 轴{axis_num}状态良好，暂无特殊维护建议")
    
    # 预测性维护时间表
    print(f"\n📅 建议维护时间表:")
    print(f"   日常检查: 每周检查温度和电流趋势")
    print(f"   精度校准: 每月检查位置精度")
    print(f"   深度维护: 每季度全面检查机械部件")
    print(f"   大修保养: 每年更换润滑油和关键磨损件")
    
    print("=" * 60)

def main():
    """
    主分析函数
    """
    print(f"🎯 当前分析轴: 轴{ANALYSIS_AXIS}")
    print(f"📊 样本大小: {SAMPLE_SIZE}")
    
    # 生成高级模拟数据
    df = generate_advanced_mock_data(n_samples=SAMPLE_SIZE, n_robots=1, random_seed=42)
    
    print(f"\n📊 数据来源: 高级模拟数据")
    print(f"📋 数据形状: {df.shape}")
    
    # 显示数据预览
    axis_cols = get_axis_columns(df, ANALYSIS_AXIS)
    print(f"\n🔍 数据预览:")
    preview_cols = ['zeit', 'motion_type'] + list(axis_cols.values())[:8]
    available_cols = [col for col in preview_cols if col in df.columns]
    print(df[available_cols].head())
    
    print("\n" + "=" * 80)
    print("🔬 高级分析开始")
    print("=" * 80)
    
    # 1. 速度精度分析
    analyze_velocity_precision(df, ANALYSIS_AXIS)
    
    # 2. 力矩和负载分析
    analyze_torque_load(df, ANALYSIS_AXIS)
    
    # 3. 异常检测
    df_with_anomalies = detect_anomalies(df, ANALYSIS_AXIS)
    
    # 4. 3D轨迹可视化
    create_3d_trajectory_visualization(df)
    
    # 5. 预测性维护建议
    generate_maintenance_recommendations(df, ANALYSIS_AXIS)
    
    print("\n✅ 高级分析完成")
    print("=" * 80)

if __name__ == "__main__":
    main()