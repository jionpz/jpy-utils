# 轴{ANALYSIS_AXIS}力矩和负载分析
soll_moment_col = f'sollmoment_{ANALYSIS_AXIS}'
ist_moment_col = f'istmoment_{ANALYSIS_AXIS}'

if all(col in df.columns for col in [soll_moment_col, ist_moment_col]):
    print(f"🔄 轴{ANALYSIS_AXIS}力矩和负载分析")
    print("=" * 60)
    
    # 计算力矩误差
    moment_error = df[soll_moment_col] - df[ist_moment_col]
    df[f'moment_error_{ANALYSIS_AXIS}'] = moment_error
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    # 力矩跟踪
    axes[0,0].plot(df['zeit'], df[soll_moment_col], label='目标力矩', linewidth=2, alpha=0.8)
    axes[0,0].plot(df['zeit'], df[ist_moment_col], label='实际力矩', linewidth=2, alpha=0.8)
    axes[0,0].set_title(f'轴{ANALYSIS_AXIS} 力矩跟踪')
    axes[0,0].set_xlabel('时间 (s)')
    axes[0,0].set_ylabel('力矩 (Nm)')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    
    # 力矩误差时间序列
    axes[0,1].plot(df['zeit'], moment_error, linewidth=2, alpha=0.8, color='red')
    axes[0,1].set_title(f'轴{ANALYSIS_AXIS} 力矩误差')
    axes[0,1].set_xlabel('时间 (s)')
    axes[0,1].set_ylabel('力矩误差 (Nm)')
    axes[0,1].grid(True, alpha=0.3)
    axes[0,1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    # 力矩分布
    axes[1,0].hist(df[ist_moment_col], bins=50, alpha=0.7, edgecolor='black')
    axes[1,0].set_title(f'轴{ANALYSIS_AXIS} 实际力矩分布')
    axes[1,0].set_xlabel('力矩 (Nm)')
    axes[1,0].set_ylabel('频次')
    axes[1,0].grid(True, alpha=0.3)
    
    # 力矩vs电流关系（如果有电流数据）
    current_col = f'iststrom_{ANALYSIS_AXIS}'
    if current_col in df.columns:
        axes[1,1].scatter(df[ist_moment_col], df[current_col], alpha=0.6, s=20)
        axes[1,1].set_title(f'轴{ANALYSIS_AXIS} 力矩 vs 电流关系')
        axes[1,1].set_xlabel('实际力矩 (Nm)')
        axes[1,1].set_ylabel('电流 (A)')
        axes[1,1].grid(True, alpha=0.3)
        
        # 计算相关系数
        moment_current_corr = df[ist_moment_col].corr(df[current_col])
        axes[1,1].text(0.05, 0.95, f'相关系数: {moment_current_corr:.3f}', 
                      transform=axes[1,1].transAxes, verticalalignment='top',
                      bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    else:
        # 力矩误差分布
        axes[1,1].hist(moment_error, bins=50, alpha=0.7, edgecolor='black', color='red')
        axes[1,1].set_title(f'轴{ANALYSIS_AXIS} 力矩误差分布')
        axes[1,1].set_xlabel('力矩误差 (Nm)')
        axes[1,1].set_ylabel('频次')
        axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # 力矩统计信息
    print(f"\n📊 轴{ANALYSIS_AXIS}力矩统计信息:")
    print(f"   平均目标力矩: {df[soll_moment_col].mean():.4f} Nm")
    print(f"   平均实际力矩: {df[ist_moment_col].mean():.4f} Nm")
    print(f"   力矩误差RMS: {np.sqrt((moment_error**2).mean()):.4f} Nm")
    print(f"   最大绝对力矩误差: {moment_error.abs().max():.4f} Nm")
    
    # 负载分析
    moment_abs = df[ist_moment_col].abs()
    print(f"\n🏋️ 轴{ANALYSIS_AXIS}负载分析:")
    print(f"   平均负载: {moment_abs.mean():.4f} Nm")
    print(f"   峰值负载: {moment_abs.max():.4f} Nm")
    print(f"   负载变异系数: {moment_abs.std() / (moment_abs.mean() + 1e-6):.4f}")
    
    # 负载等级评估
    peak_load_ratio = moment_abs.max() / (moment_abs.mean() + 1e-6)
    if peak_load_ratio < 2.0:
        print("   负载特性: 稳定负载")
    elif peak_load_ratio < 5.0:
        print("   负载特性: 中等变化负载")
    else:
        print("   负载特性: 高变化负载")
    
    print("=" * 60)
    
else:
    print(f"❌ 轴{ANALYSIS_AXIS}缺少力矩数据")# 轴{ANALYSIS_AXIS}速度精度深度分析
axis_cols = get_axis_columns(df, ANALYSIS_AXIS)

# 检查必要的速度数据是否存在
soll_vel_col = f'sollgeschwindigkeit_{ANALYSIS_AXIS}'
ist_vel_col = f'istgeschwindigkeit_{ANALYSIS_AXIS}'
vel_diff_col = f'geschwindigkeitsdifferenz_{ANALYSIS_AXIS}'

if all(col in df.columns for col in [soll_vel_col, ist_vel_col]):
    print(f"⚡ 轴{ANALYSIS_AXIS}速度精度分析")
    print("=" * 60)
    
    # 1. 采集的速度差分析
    if vel_diff_col in df.columns:
        collected_vel_diff = df[vel_diff_col]
        print(f"\n📊 采集的速度差统计:")
        print(f"   平均速度差: {collected_vel_diff.mean():.6f}°/s")
        print(f"   速度差标准差: {collected_vel_diff.std():.6f}°/s")
        print(f"   最大绝对速度差: {collected_vel_diff.abs().max():.6f}°/s")
        print(f"   RMS速度差: {np.sqrt((collected_vel_diff**2).mean()):.6f}°/s")
    
    # 2. 计算的速度差分析
    calculated_vel_diff = df[soll_vel_col] - df[ist_vel_col]
    df[f'calculated_vel_diff_{ANALYSIS_AXIS}'] = calculated_vel_diff
    
    print(f"\n🧮 计算的速度差统计 (目标速度 - 实际速度):")
    print(f"   平均速度差: {calculated_vel_diff.mean():.6f}°/s")
    print(f"   速度差标准差: {calculated_vel_diff.std():.6f}°/s")
    print(f"   最大绝对速度差: {calculated_vel_diff.abs().max():.6f}°/s")
    print(f"   RMS速度差: {np.sqrt((calculated_vel_diff**2).mean()):.6f}°/s")
    
    # 3. 两种速度差的对比分析
    if vel_diff_col in df.columns:
        vel_error_diff = collected_vel_diff - calculated_vel_diff
        vel_correlation = collected_vel_diff.corr(calculated_vel_diff)
        
        print(f"\n🔍 两种速度差对比分析:")
        print(f"   速度差相关系数: {vel_correlation:.4f}")
        print(f"   速度差差值均值: {vel_error_diff.mean():.6f}°/s")
        print(f"   速度差差值标准差: {vel_error_diff.std():.6f}°/s")
        
        if abs(vel_correlation) > 0.8:
            print("   ✅ 两种速度差高度相关，数据一致性良好")
        elif abs(vel_correlation) > 0.5:
            print("   ⚠️ 两种速度差中度相关，可能存在系统性差异")
        else:
            print("   ❌ 两种速度差相关性较低，需要检查数据质量")
    
    # 4. 速度跟踪性能分析
    # 计算速度跟踪延迟
    if 'zeit' in df.columns:
        # 使用互相关分析速度跟踪延迟
        from scipy.signal import correlate
        
        soll_vel_norm = (df[soll_vel_col] - df[soll_vel_col].mean()) / df[soll_vel_col].std()
        ist_vel_norm = (df[ist_vel_col] - df[ist_vel_col].mean()) / df[ist_vel_col].std()
        
        correlation = correlate(ist_vel_norm, soll_vel_norm, mode='full')
        delay_samples = np.argmax(correlation) - len(soll_vel_norm) + 1
        
        if len(df) > 1:
            time_step = (df['zeit'].iloc[-1] - df['zeit'].iloc[0]) / (len(df) - 1)
            delay_time = delay_samples * time_step
            print(f"\n⏱️ 速度跟踪延迟分析:")
            print(f"   估计延迟: {delay_time:.6f}秒 ({delay_samples}个采样点)")
    
    # 5. 速度精度可视化
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 子图1: 目标速度vs实际速度
    axes[0,0].plot(df['zeit'], df[soll_vel_col], label='目标速度', linewidth=2, alpha=0.8)
    axes[0,0].plot(df['zeit'], df[ist_vel_col], label='实际速度', linewidth=2, alpha=0.8)
    axes[0,0].set_title(f'轴{ANALYSIS_AXIS} 速度跟踪')
    axes[0,0].set_xlabel('时间 (s)')
    axes[0,0].set_ylabel('速度 (°/s)')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    
    # 子图2: 速度差时间序列
    if vel_diff_col in df.columns:
        axes[0,1].plot(df['zeit'], collected_vel_diff, label='采集速度差', linewidth=1.5, alpha=0.8)
    axes[0,1].plot(df['zeit'], calculated_vel_diff, label='计算速度差', linewidth=1.5, alpha=0.8)
    axes[0,1].set_title(f'轴{ANALYSIS_AXIS} 速度差时间序列')
    axes[0,1].set_xlabel('时间 (s)')
    axes[0,1].set_ylabel('速度差 (°/s)')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    axes[0,1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    # 子图3: 速度差分布直方图
    axes[1,0].hist(calculated_vel_diff, bins=50, alpha=0.7, label='计算速度差', density=True)
    if vel_diff_col in df.columns:
        axes[1,0].hist(collected_vel_diff, bins=50, alpha=0.7, label='采集速度差', density=True)
    axes[1,0].set_title(f'轴{ANALYSIS_AXIS} 速度差分布')
    axes[1,0].set_xlabel('速度差 (°/s)')
    axes[1,0].set_ylabel('密度')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)
    
    # 子图4: 速度差相关性散点图或速度响应分析
    if vel_diff_col in df.columns:
        axes[1,1].scatter(collected_vel_diff, calculated_vel_diff, alpha=0.6, s=20)
        axes[1,1].plot([collected_vel_diff.min(), collected_vel_diff.max()], 
                      [collected_vel_diff.min(), collected_vel_diff.max()], 
                      'r--', label='理想相关线')
        axes[1,1].set_title(f'轴{ANALYSIS_AXIS} 两种速度差相关性')
        axes[1,1].set_xlabel('采集速度差 (°/s)')
        axes[1,1].set_ylabel('计算速度差 (°/s)')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)
    else:
        # 速度响应特性分析
        axes[1,1].scatter(df[soll_vel_col], df[ist_vel_col], alpha=0.6, s=20)
        min_vel = min(df[soll_vel_col].min(), df[ist_vel_col].min())
        max_vel = max(df[soll_vel_col].max(), df[ist_vel_col].max())
        axes[1,1].plot([min_vel, max_vel], [min_vel, max_vel], 'r--', label='理想响应线')
        axes[1,1].set_title(f'轴{ANALYSIS_AXIS} 速度响应特性')
        axes[1,1].set_xlabel('目标速度 (°/s)')
        axes[1,1].set_ylabel('实际速度 (°/s)')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # 6. 速度控制性能等级评估
    rms_vel_error = np.sqrt((calculated_vel_diff**2).mean())
    max_abs_vel_error = calculated_vel_diff.abs().max()
    
    print(f"\n📏 轴{ANALYSIS_AXIS}速度控制性能等级评估:")
    if rms_vel_error < 1.0:
        print(f"   速度控制等级: 优秀 (RMS < 1.0°/s)")
    elif rms_vel_error < 5.0:
        print(f"   速度控制等级: 良好 (RMS < 5.0°/s)")
    elif rms_vel_error < 10.0:
        print(f"   速度控制等级: 一般 (RMS < 10.0°/s)")
    else:
        print(f"   速度控制等级: 需要改进 (RMS ≥ 10.0°/s)")
    
    # 7. 速度稳定性分析
    vel_stability = df[ist_vel_col].std() / (df[ist_vel_col].mean() + 1e-6)  # 避免除零
    print(f"\n📊 轴{ANALYSIS_AXIS}速度稳定性分析:")
    print(f"   速度变异系数: {vel_stability:.4f}")
    if vel_stability < 0.1:
        print("   速度稳定性: 优秀")
    elif vel_stability < 0.3:
        print("   速度稳定性: 良好") 
    else:
        print("   速度稳定性: 需要改进")
    
    print("=" * 60)
    
else:
    print(f"❌ 轴{ANALYSIS_AXIS}缺少速度数据，无法进行速度精度分析")## 6. 总结

### 本次分析总结

通过本次KUKA机器人轨迹数据探索分析，我们完成了以下工作：

1. **数据加载与预处理**
   - 建立了数据库连接和数据加载框架
   - 实现了数据类型转换和基础清理
   - 提供了模拟数据生成功能用于演示

2. **基础统计分析**
   - 分析了数据的基本特征和分布
   - 统计了机器人实例、轨迹记录、运动类型等信息
   - 对各类数值字段进行了详细的描述性统计

3. **可视化探索**
   - 3D轨迹可视化展示了机器人的运动路径
   - 关节轴性能分析揭示了各轴的工作状态
   - 速度和加速度分析提供了运动特性洞察
   - 温度和电流监控帮助评估设备健康状态

4. **高级分析**
   - 异常检测识别了潜在的问题数据点
   - 运动模式聚类发现了不同的工作模式
   - 为后续的预测性维护提供了基础

5. **质量评估与优化建议**
   - 全面评估了数据质量
   - 提供了针对性的性能优化建议
   - 给出了预防性维护指导

### 后续工作建议

1. **深入分析**
   - 建立更精确的故障预测模型
   - 分析不同工况下的性能差异
   - 研究轨迹优化算法

2. **实时监控**
   - 建立实时数据监控仪表板
   - 设置关键指标的报警阈值
   - 实现自动化的异常检测

3. **持续优化**
   - 根据分析结果调整控制参数
   - 优化运动轨迹和速度曲线
   - 制定更精准的维护计划

---

**📝 注意事项：**
- 本分析基于提供的数据表结构进行设计
- 实际使用时请根据具体的数据库配置调整连接参数
- 建议定期运行此分析以监控机器人性能趋势
- 对于生产环境，建议增加更多的安全检查和错误处理# 性能优化建议\nprint(\"=\"*60)\nprint(\"🚀 KUKA机器人性能优化建议\")\nprint(\"=\"*60)\n\n# 1. 运动性能分析\nprint(\"\\n📈 1. 运动性能优化:\")\n\n# 速度分析\nif 'cart_vel_act' in df.columns:\n    avg_speed = df['cart_vel_act'].mean()\n    max_speed = df['cart_vel_act'].max()\n    speed_utilization = avg_speed / max_speed * 100\n    \n    print(f\"   当前平均速度: {avg_speed:.2f} mm/s\")\n    print(f\"   最大记录速度: {max_speed:.2f} mm/s\")\n    print(f\"   速度利用率: {speed_utilization:.1f}%\")\n    \n    if speed_utilization < 60:\n        print(\"   💡 建议: 考虑提高运动速度以提升效率\")\n    elif speed_utilization > 90:\n        print(\"   ⚠️  注意: 速度接近极限，注意安全余量\")\n\n# 加速度分析\nif 'cart_acc' in df.columns:\n    avg_acc = df['cart_acc'].abs().mean()\n    max_acc = df['cart_acc'].abs().max()\n    \n    print(f\"   平均加速度: {avg_acc:.2f} mm/s²\")\n    print(f\"   最大加速度: {max_acc:.2f} mm/s²\")\n    \n    if max_acc > avg_acc * 10:\n        print(\"   💡 建议: 优化加速度曲线，减少冲击\")\n\n# 2. 轴性能分析\nprint(\"\\n🔧 2. 各轴性能评估:\")\n\nerror_cols = [col for col in df.columns if 'schleppfehler' in col]\nif error_cols:\n    print(\"   位置跟随误差分析:\")\n    for col in error_cols[:6]:\n        axis_num = col.split('_')[-1]\n        rms_error = np.sqrt((df[col]**2).mean())\n        max_error = df[col].abs().max()\n        \n        print(f\"     轴{axis_num} - RMS误差: {rms_error:.4f}, 最大误差: {max_error:.4f}\")\n        \n        if rms_error > 0.1:  # 假设0.1为警告阈值\n            print(f\"     ⚠️  轴{axis_num}跟随误差较大，建议调整PID参数\")\n\n# 3. 热管理分析\nprint(\"\\n🌡️ 3. 热管理优化:\")\n\ntemp_cols = [col for col in df.columns if 'temperatur' in col]\nif temp_cols:\n    for col in temp_cols[:6]:\n        axis_num = col.split('_')[-1]\n        avg_temp = df[col].mean()\n        max_temp = df[col].max()\n        \n        print(f\"   轴{axis_num} - 平均温度: {avg_temp:.1f}°C, 最高温度: {max_temp:.1f}°C\")\n        \n        if max_temp > 70:\n            print(f\"   🔥 警告: 轴{axis_num}温度过高，建议检查散热系统\")\n        elif avg_temp > 55:\n            print(f\"   💡 建议: 轴{axis_num}工作温度偏高，考虑优化负载\")\n\n# 4. 能效分析\nprint(\"\\n⚡ 4. 能效优化:\")\n\ncurrent_cols = [col for col in df.columns if 'strom' in col]\nif current_cols:\n    total_current = df[current_cols].sum(axis=1).mean()\n    peak_current = df[current_cols].sum(axis=1).max()\n    \n    print(f\"   平均总电流: {total_current:.2f}A\")\n    print(f\"   峰值总电流: {peak_current:.2f}A\")\n    print(f\"   电流利用率: {total_current/peak_current*100:.1f}%\")\n    \n    # 检查各轴电流平衡\n    current_std = df[current_cols].std(axis=1).mean()\n    if current_std > total_current * 0.3:\n        print(\"   💡 建议: 各轴负载不均衡，考虑优化轨迹规划\")\n\n# 5. 维护建议\nprint(\"\\n🔧 5. 预防性维护建议:\")\n\n# 基于温度的维护建议\nif temp_cols:\n    high_temp_axes = []\n    for col in temp_cols:\n        axis_num = col.split('_')[-1]\n        if df[col].max() > 65:\n            high_temp_axes.append(axis_num)\n    \n    if high_temp_axes:\n        print(f\"   🔧 建议优先检查轴 {', '.join(high_temp_axes)} 的润滑和散热\")\n\n# 基于误差的维护建议\nif error_cols:\n    high_error_axes = []\n    for col in error_cols:\n        axis_num = col.split('_')[-1]\n        if np.sqrt((df[col]**2).mean()) > 0.1:\n            high_error_axes.append(axis_num)\n    \n    if high_error_axes:\n        print(f\"   🎯 建议校准轴 {', '.join(high_error_axes)} 的控制参数\")\n\nprint(\"\\n✅ 性能优化建议生成完成\")\nprint(\"=\"*60)"### 5.2 性能优化建议# 数据质量评估报告
print(\"=\"*60)\nprint(\"📋 KUKA机器人轨迹数据质量评估报告\")\nprint(\"=\"*60)\n\n# 1. 数据完整性\nprint(\"\\n📊 1. 数据完整性分析:\")\ntotal_fields = len(df.columns)\nmissing_data = df.isnull().sum()\nfields_with_missing = (missing_data > 0).sum()\nprint(f\"   总字段数: {total_fields}\")\nprint(f\"   有缺失值的字段数: {fields_with_missing}\")\nprint(f\"   数据完整性: {(total_fields - fields_with_missing) / total_fields * 100:.1f}%\")\n\nif fields_with_missing > 0:\n    print(f\"\\n   缺失值最严重的字段:\")\n    top_missing = missing_data[missing_data > 0].sort_values(ascending=False).head(5)\n    for field, count in top_missing.items():\n        print(f\"     {field}: {count} ({count/len(df)*100:.1f}%)\")\n\n# 2. 数据一致性\nprint(\"\\n🔍 2. 数据一致性检查:\")\n\n# 检查时间序列连续性\nif 'zeit' in df.columns:\n    time_diffs = df['zeit'].diff().dropna()\n    time_gaps = time_diffs[time_diffs > time_diffs.quantile(0.95)]\n    print(f\"   时间序列连续性: {len(time_gaps)} 个异常时间间隔\")\n    print(f\"   平均采样间隔: {time_diffs.median():.6f} 秒\")\n\n# 检查位置数据合理性\nposition_cols = ['x_act', 'y_act', 'z_act']\nposition_issues = 0\nfor col in position_cols:\n    if col in df.columns:\n        extreme_values = df[col].abs() > 10000  # 假设超过10米为异常\n        if extreme_values.any():\n            position_issues += extreme_values.sum()\n            \nprint(f\"   位置数据异常值: {position_issues} 个极值点\")\n\n# 3. 传感器数据质量\nprint(\"\\n🌡️ 3. 传感器数据质量:\")\n\n# 温度数据检查\ntemp_cols = [col for col in df.columns if 'temperatur' in col]\nif temp_cols:\n    temp_data = df[temp_cols]\n    temp_outliers = ((temp_data < 0) | (temp_data > 100)).sum().sum()\n    print(f\"   温度传感器异常值: {temp_outliers} 个 (范围: 0-100°C)\")\n    print(f\"   平均工作温度: {temp_data.mean().mean():.1f}°C\")\n\n# 电流数据检查\ncurrent_cols = [col for col in df.columns if 'strom' in col]\nif current_cols:\n    current_data = df[current_cols]\n    current_outliers = (current_data < 0).sum().sum()\n    print(f\"   电流传感器异常值: {current_outliers} 个负值\")\n    print(f\"   平均工作电流: {current_data.mean().mean():.2f}A\")\n\n# 4. 数据建议\nprint(\"\\n💡 4. 数据质量改进建议:\")\n\nif fields_with_missing > total_fields * 0.1:\n    print(\"   ⚠️  缺失值较多，建议检查数据采集系统\")\n\nif position_issues > len(df) * 0.05:\n    print(\"   ⚠️  位置数据存在异常，建议校准坐标系统\")\n\nif 'zeit' in df.columns and len(time_gaps) > 0:\n    print(\"   ⚠️  时间序列存在间隔，建议检查采样频率设置\")\n\nif temp_cols and temp_outliers > 0:\n    print(\"   ⚠️  温度传感器数据异常，建议检查传感器状态\")\n\nprint(\"\\n✅ 数据质量评估完成\")\nprint(\"=\"*60)"## 5. 结论与建议

### 5.1 数据质量评估# 基于运动特征的聚类分析
clustering_features = []

# 添加笛卡尔坐标
if all(col in df.columns for col in ['x_act', 'y_act', 'z_act']):\n    clustering_features.extend(['x_act', 'y_act', 'z_act'])\n\n# 添加速度\nif 'cart_vel_act' in df.columns:\n    clustering_features.append('cart_vel_act')\n\n# 添加关节角度\naxis_pos_cols = [col for col in df.columns if col.startswith('axis_pos_act')]\nclustering_features.extend(axis_pos_cols[:3])  # 选择前3个轴\n\nif len(clustering_features) >= 3:\n    # 准备聚类数据\n    X_cluster = df[clustering_features].dropna()\n    \n    if len(X_cluster) > 50:  # 确保有足够的数据进行聚类\n        # 数据标准化\n        scaler = StandardScaler()\n        X_scaled = scaler.fit_transform(X_cluster)\n        \n        # K-means聚类\n        n_clusters = 5  # 假设有5种运动模式\n        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)\n        cluster_labels = kmeans.fit_predict(X_scaled)\n        \n        # 添加聚类标签\n        df_cluster = df.loc[X_cluster.index].copy()\n        df_cluster['cluster'] = cluster_labels\n        \n        print(f\"🎭 运动模式聚类结果:\")\n        cluster_counts = pd.Series(cluster_labels).value_counts().sort_index()\n        for cluster_id, count in cluster_counts.items():\n            print(f\"   模式 {cluster_id}: {count} 个数据点 ({count/len(cluster_labels)*100:.1f}%)\")\n        \n        # 可视化聚类结果\n        if 'x_act' in df.columns and 'y_act' in df.columns:\n            fig, axes = plt.subplots(1, 2, figsize=(16, 6))\n            \n            # 在轨迹图上显示聚类结果\n            colors = plt.cm.Set3(np.linspace(0, 1, n_clusters))\n            for cluster_id in range(n_clusters):\n                cluster_data = df_cluster[df_cluster['cluster'] == cluster_id]\n                axes[0].scatter(cluster_data['x_act'], cluster_data['y_act'], \n                              c=[colors[cluster_id]], alpha=0.7, s=15, \n                              label=f'模式 {cluster_id}')\n            \n            axes[0].set_xlabel('X轴位置 (mm)')\n            axes[0].set_ylabel('Y轴位置 (mm)')\n            axes[0].set_title('🎯 运动模式聚类 - 轨迹视图')\n            axes[0].legend()\n            axes[0].grid(True, alpha=0.3)\n            \n            # 时间序列聚类视图\n            if 'zeit' in df.columns:\n                for cluster_id in range(n_clusters):\n                    cluster_data = df_cluster[df_cluster['cluster'] == cluster_id]\n                    axes[1].scatter(cluster_data['zeit'], cluster_data['cart_vel_act'] if 'cart_vel_act' in df.columns else cluster_data['x_act'], \n                                  c=[colors[cluster_id]], alpha=0.7, s=10, \n                                  label=f'模式 {cluster_id}')\n                \n                axes[1].set_xlabel('时间 (s)')\n                axes[1].set_ylabel('速度 (mm/s)' if 'cart_vel_act' in df.columns else 'X位置 (mm)')\n                axes[1].set_title('📈 运动模式聚类 - 时间序列视图')\n                axes[1].legend()\n                axes[1].grid(True, alpha=0.3)\n            \n            plt.tight_layout()\n            plt.show()\n        \n        # 分析每个聚类的特征\n        print(f\"\\n📊 各运动模式特征统计:\")\n        for cluster_id in range(n_clusters):\n            cluster_data = df_cluster[df_cluster['cluster'] == cluster_id]\n            print(f\"\\n   模式 {cluster_id}:\")\n            \n            if 'cart_vel_act' in cluster_data.columns:\n                print(f\"     平均速度: {cluster_data['cart_vel_act'].mean():.2f} mm/s\")\n                print(f\"     速度范围: {cluster_data['cart_vel_act'].min():.2f} - {cluster_data['cart_vel_act'].max():.2f} mm/s\")\n            \n            if 'motion_type' in cluster_data.columns:\n                motion_dist = cluster_data['motion_type'].value_counts()\n                print(f\"     主要运动类型: {motion_dist.index[0]} ({motion_dist.iloc[0]/len(cluster_data)*100:.1f}%)\")\n    else:\n        print(\"❌ 数据量不足，无法进行聚类分析\")\nelse:\n    print(\"❌ 缺少足够的特征数据进行聚类分析\")"### 4.2 运动模式聚类分析# 使用Isolation Forest进行异常检测
# 选择关键特征进行异常检测
feature_cols = []

# 添加笛卡尔坐标
cartesian_cols = ['x_act', 'y_act', 'z_act']
feature_cols.extend([col for col in cartesian_cols if col in df.columns])

# 添加速度
if 'cart_vel_act' in df.columns:
    feature_cols.append('cart_vel_act')

# 添加温度数据
temp_cols = [col for col in df.columns if 'temperatur' in col]
feature_cols.extend(temp_cols[:3])  # 选择前3个轴的温度

# 添加电流数据
current_cols = [col for col in df.columns if 'strom' in col]
feature_cols.extend(current_cols[:3])  # 选择前3个轴的电流

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
        
        print(f\"🚨 异常检测结果:\")\n        print(f\"   总样本数: {len(anomaly_labels)}\")\n        print(f\"   异常点数量: {n_anomalies}\")\n        print(f\"   异常率: {anomaly_rate:.2f}%\")\n        \n        # 可视化异常检测结果\n        if 'x_act' in df.columns and 'y_act' in df.columns:\n            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))\n            \n            # 在轨迹图上标记异常点\n            normal_data = df_analysis[df_analysis['anomaly'] == 1]\n            anomaly_data = df_analysis[df_analysis['anomaly'] == -1]\n            \n            ax1.scatter(normal_data['x_act'], normal_data['y_act'], \n                       c='blue', alpha=0.6, s=10, label='正常点')\n            ax1.scatter(anomaly_data['x_act'], anomaly_data['y_act'], \n                       c='red', alpha=0.8, s=20, label='异常点')\n            ax1.set_xlabel('X轴位置 (mm)')\n            ax1.set_ylabel('Y轴位置 (mm)')\n            ax1.set_title('🎯 轨迹中的异常点检测')\n            ax1.legend()\n            ax1.grid(True, alpha=0.3)\n            \n            # 异常分数分布\n            ax2.hist(df_analysis['anomaly_score'], bins=50, alpha=0.7, edgecolor='black')\n            ax2.axvline(x=df_analysis[df_analysis['anomaly'] == -1]['anomaly_score'].max(), \n                       color='red', linestyle='--', label='异常阈值')\n            ax2.set_xlabel('异常分数')\n            ax2.set_ylabel('频次')\n            ax2.set_title('📊 异常分数分布')\n            ax2.legend()\n            ax2.grid(True, alpha=0.3)\n            \n            plt.tight_layout()\n            plt.show()\n        \n        # 显示最异常的几个点的详细信息\n        top_anomalies = df_analysis[df_analysis['anomaly'] == -1].nsmallest(5, 'anomaly_score')\n        if not top_anomalies.empty:\n            print(f\"\\n🔍 最异常的5个数据点:\")\n            print(top_anomalies[['zeit'] + feature_cols + ['anomaly_score']].round(3))\n    else:\n        print(\"❌ 数据量不足，无法进行异常检测\")\nelse:\n    print(\"❌ 缺少足够的特征数据进行异常检测\")"## 4. 高级分析

### 4.1 异常检测分析# 速度分析和加速度计算
if 'cart_vel_act' in df.columns and 'zeit' in df.columns:
    
    # 计算加速度
    df['cart_acc'] = np.gradient(df['cart_vel_act'], df['zeit'])
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    
    # 笛卡尔速度时间序列
    axes[0,0].plot(df['zeit'], df['cart_vel_act'], linewidth=2, alpha=0.8)
    axes[0,0].set_title('📈 笛卡尔速度时间序列')
    axes[0,0].set_xlabel('时间 (s)')
    axes[0,0].set_ylabel('速度 (mm/s)')
    axes[0,0].grid(True, alpha=0.3)
    
    # 笛卡尔加速度时间序列
    axes[0,1].plot(df['zeit'], df['cart_acc'], linewidth=2, alpha=0.8, color='orange')
    axes[0,1].set_title('📊 笛卡尔加速度时间序列')
    axes[0,1].set_xlabel('时间 (s)')
    axes[0,1].set_ylabel('加速度 (mm/s²)')
    axes[0,1].grid(True, alpha=0.3)
    
    # 速度分布直方图
    axes[1,0].hist(df['cart_vel_act'], bins=50, alpha=0.7, edgecolor='black')
    axes[1,0].set_title('🔔 速度分布直方图')
    axes[1,0].set_xlabel('速度 (mm/s)')
    axes[1,0].set_ylabel('频次')
    axes[1,0].grid(True, alpha=0.3)
    
    # 速度vs加速度散点图
    axes[1,1].scatter(df['cart_vel_act'], df['cart_acc'], alpha=0.5, s=10)
    axes[1,1].set_title('⚡ 速度 vs 加速度')
    axes[1,1].set_xlabel('速度 (mm/s)')
    axes[1,1].set_ylabel('加速度 (mm/s²)')
    axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # 速度统计信息
    print(f\"📊 速度统计信息:\")\n    print(f\"   平均速度: {df['cart_vel_act'].mean():.2f} mm/s\")\n    print(f\"   最大速度: {df['cart_vel_act'].max():.2f} mm/s\")\n    print(f\"   速度标准差: {df['cart_vel_act'].std():.2f} mm/s\")\n    print(f\"   平均加速度: {df['cart_acc'].mean():.2f} mm/s²\")\n    print(f\"   最大加速度: {df['cart_acc'].abs().max():.2f} mm/s²\")\n    \nelse:\n    print(\"❌ 缺少速度数据\")"### 3.3 速度和加速度分析# 电机温度和电流监控
temp_cols = [col for col in df.columns if 'temperatur' in col]
current_cols = [col for col in df.columns if 'strom' in col]

if temp_cols and current_cols:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    
    # 电机温度趋势
    for col in temp_cols[:6]:  # 最多显示6个轴
        axis_num = col.split('_')[-1]
        ax1.plot(df['zeit'], df[col], label=f'轴{axis_num}', linewidth=2, alpha=0.8)
    
    ax1.set_title('🌡️ 各轴电机温度趋势')
    ax1.set_xlabel('时间 (s)')
    ax1.set_ylabel('温度 (°C)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # 添加温度警告线
    ax1.axhline(y=60, color='orange', linestyle='--', alpha=0.7, label='警告温度 (60°C)')
    ax1.axhline(y=80, color='red', linestyle='--', alpha=0.7, label='危险温度 (80°C)')
    
    # 电机电流趋势
    for col in current_cols[:6]:  # 最多显示6个轴
        axis_num = col.split('_')[-1]
        ax2.plot(df['zeit'], df[col], label=f'轴{axis_num}', linewidth=2, alpha=0.8)
    
    ax2.set_title('⚡ 各轴电机电流趋势')
    ax2.set_xlabel('时间 (s)')
    ax2.set_ylabel('电流 (A)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    plt.tight_layout()
    plt.show()
    
else:
    print("❌ 缺少电机温度或电流数据")# 轴{ANALYSIS_AXIS}温度和电流监控分析
temp_col = f'motortemperatur_{ANALYSIS_AXIS}'
current_col = f'iststrom_{ANALYSIS_AXIS}'

if temp_col in df.columns and current_col in df.columns:
    print(f"🌡️ 轴{ANALYSIS_AXIS}温度和电流监控分析")
    print("=" * 60)
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 10))
    
    # 电机温度趋势
    ax1.plot(df['zeit'], df[temp_col], linewidth=2, alpha=0.8, color='red', label=f'轴{ANALYSIS_AXIS}温度')
    ax1.set_title(f'轴{ANALYSIS_AXIS} 电机温度趋势')
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
    
    ax1.text(0.02, 0.98, f'平均: {temp_mean:.1f}°C\n最高: {temp_max:.1f}°C\n标准差: {temp_std:.1f}°C', 
             transform=ax1.transAxes, verticalalignment='top', 
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # 电机电流趋势
    ax2.plot(df['zeit'], df[current_col], linewidth=2, alpha=0.8, color='blue', label=f'轴{ANALYSIS_AXIS}电流')
    ax2.set_title(f'轴{ANALYSIS_AXIS} 电机电流趋势')
    ax2.set_xlabel('时间 (s)')
    ax2.set_ylabel('电流 (A)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # 电流统计信息
    current_mean = df[current_col].mean()
    current_max = df[current_col].max()
    current_std = df[current_col].std()
    
    ax2.text(0.02, 0.98, f'平均: {current_mean:.2f}A\n最大: {current_max:.2f}A\n标准差: {current_std:.2f}A', 
             transform=ax2.transAxes, verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.show()
    
    # 温度与电流关系分析
    temp_current_corr = df[temp_col].corr(df[current_col])
    print(f"\n🔗 轴{ANALYSIS_AXIS}温度与电流关系分析:")
    print(f"   相关系数: {temp_current_corr:.4f}")
    
    if abs(temp_current_corr) > 0.7:
        print("   ✅ 温度与电流高度相关，符合预期")
    elif abs(temp_current_corr) > 0.3:
        print("   ⚠️ 温度与电流中度相关")
    else:
        print("   ❌ 温度与电流相关性较低，需要检查")
    
    # 健康状态评估
    print(f"\n🏥 轴{ANALYSIS_AXIS}健康状态评估:")
    
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
    
elif temp_col in df.columns:
    print(f"⚠️ 只有轴{ANALYSIS_AXIS}温度数据，缺少电流数据")
elif current_col in df.columns:
    print(f"⚠️ 只有轴{ANALYSIS_AXIS}电流数据，缺少温度数据")
else:
    print(f"❌ 轴{ANALYSIS_AXIS}缺少温度和电流数据")### 3.2 关节轴性能分析# XY平面轨迹投影
if all(col in df.columns for col in ['x_act', 'y_act']):
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # XY平面投影
    if 'ins_id' in df.columns:
        for ins_id in sorted(df['ins_id'].unique()):
            robot_data = df[df['ins_id'] == ins_id]
            axes[0].plot(robot_data['x_act'], robot_data['y_act'], 
                        label=f'机器人 {ins_id}', linewidth=2, alpha=0.7)
    else:
        axes[0].plot(df['x_act'], df['y_act'], linewidth=2, alpha=0.7)
    
    axes[0].set_xlabel('X轴位置 (mm)')
    axes[0].set_ylabel('Y轴位置 (mm)')
    axes[0].set_title('XY平面轨迹投影')
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()
    axes[0].axis('equal')
    
    # 时间序列轨迹
    if 'zeit' in df.columns:
        axes[1].plot(df['zeit'], df['x_act'], label='X轴', linewidth=2)
        axes[1].plot(df['zeit'], df['y_act'], label='Y轴', linewidth=2)
        if 'z_act' in df.columns:
            axes[1].plot(df['zeit'], df['z_act'], label='Z轴', linewidth=2)
        
        axes[1].set_xlabel('时间 (s)')
        axes[1].set_ylabel('位置 (mm)')
        axes[1].set_title('笛卡尔坐标时间序列')
        axes[1].grid(True, alpha=0.3)
        axes[1].legend()
    
    plt.tight_layout()
    plt.show()
    
else:
    print("❌ 缺少笛卡尔坐标数据，无法绘制轨迹投影图")# 轴{ANALYSIS_AXIS}位置精度深度分析
axis_cols = get_axis_columns(df, ANALYSIS_AXIS)

# 检查必要的位置数据是否存在
soll_pos_col = f'sollposition_{ANALYSIS_AXIS}'
ist_pos_col = f'istposition_{ANALYSIS_AXIS}'
follow_error_col = f'positionsschleppfehler_{ANALYSIS_AXIS}'

if all(col in df.columns for col in [soll_pos_col, ist_pos_col]):
    print(f"🎯 轴{ANALYSIS_AXIS}位置精度分析")
    print("=" * 60)
    
    # 1. 采集的位置跟随误差分析
    if follow_error_col in df.columns:
        collected_error = df[follow_error_col]
        print(f"\n📊 采集的位置跟随误差统计:")
        print(f"   平均误差: {collected_error.mean():.6f}°")
        print(f"   误差标准差: {collected_error.std():.6f}°")
        print(f"   最大绝对误差: {collected_error.abs().max():.6f}°")
        print(f"   RMS误差: {np.sqrt((collected_error**2).mean()):.6f}°")
    
    # 2. 计算的位置误差分析
    calculated_error = df[soll_pos_col] - df[ist_pos_col]
    df[f'calculated_pos_error_{ANALYSIS_AXIS}'] = calculated_error
    
    print(f"\n🧮 计算的位置误差统计 (目标位置 - 实际位置):")
    print(f"   平均误差: {calculated_error.mean():.6f}°")
    print(f"   误差标准差: {calculated_error.std():.6f}°")
    print(f"   最大绝对误差: {calculated_error.abs().max():.6f}°")
    print(f"   RMS误差: {np.sqrt((calculated_error**2).mean()):.6f}°")
    
    # 3. 两种误差的对比分析
    if follow_error_col in df.columns:
        error_diff = collected_error - calculated_error
        correlation = collected_error.corr(calculated_error)
        
        print(f"\n🔍 两种误差对比分析:")
        print(f"   误差相关系数: {correlation:.4f}")
        print(f"   误差差值均值: {error_diff.mean():.6f}°")
        print(f"   误差差值标准差: {error_diff.std():.6f}°")
        
        if abs(correlation) > 0.8:
            print("   ✅ 两种误差高度相关，数据一致性良好")
        elif abs(correlation) > 0.5:
            print("   ⚠️ 两种误差中度相关，可能存在系统性差异")
        else:
            print("   ❌ 两种误差相关性较低，需要检查数据质量")
    
    # 4. 位置精度可视化
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 子图1: 目标位置vs实际位置
    axes[0,0].plot(df['zeit'], df[soll_pos_col], label='目标位置', linewidth=2, alpha=0.8)
    axes[0,0].plot(df['zeit'], df[ist_pos_col], label='实际位置', linewidth=2, alpha=0.8)
    axes[0,0].set_title(f'轴{ANALYSIS_AXIS} 位置跟踪')
    axes[0,0].set_xlabel('时间 (s)')
    axes[0,0].set_ylabel('位置 (°)')
    axes[0,0].legend()
    axes[0,0].grid(True, alpha=0.3)
    
    # 子图2: 位置误差时间序列
    if follow_error_col in df.columns:
        axes[0,1].plot(df['zeit'], collected_error, label='采集跟随误差', linewidth=1.5, alpha=0.8)
    axes[0,1].plot(df['zeit'], calculated_error, label='计算位置误差', linewidth=1.5, alpha=0.8)
    axes[0,1].set_title(f'轴{ANALYSIS_AXIS} 位置误差时间序列')
    axes[0,1].set_xlabel('时间 (s)')
    axes[0,1].set_ylabel('误差 (°)')
    axes[0,1].legend()
    axes[0,1].grid(True, alpha=0.3)
    axes[0,1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
    
    # 子图3: 误差分布直方图
    axes[1,0].hist(calculated_error, bins=50, alpha=0.7, label='计算误差', density=True)
    if follow_error_col in df.columns:
        axes[1,0].hist(collected_error, bins=50, alpha=0.7, label='采集误差', density=True)
    axes[1,0].set_title(f'轴{ANALYSIS_AXIS} 位置误差分布')
    axes[1,0].set_xlabel('误差 (°)')
    axes[1,0].set_ylabel('密度')
    axes[1,0].legend()
    axes[1,0].grid(True, alpha=0.3)
    
    # 子图4: 误差相关性散点图
    if follow_error_col in df.columns:
        axes[1,1].scatter(collected_error, calculated_error, alpha=0.6, s=20)
        axes[1,1].plot([collected_error.min(), collected_error.max()], 
                      [collected_error.min(), collected_error.max()], 
                      'r--', label='理想相关线')
        axes[1,1].set_title(f'轴{ANALYSIS_AXIS} 两种误差相关性')
        axes[1,1].set_xlabel('采集跟随误差 (°)')
        axes[1,1].set_ylabel('计算位置误差 (°)')
        axes[1,1].legend()
        axes[1,1].grid(True, alpha=0.3)
    else:
        axes[1,1].plot(df['zeit'], calculated_error.abs(), linewidth=2)
        axes[1,1].set_title(f'轴{ANALYSIS_AXIS} 绝对位置误差')
        axes[1,1].set_xlabel('时间 (s)')
        axes[1,1].set_ylabel('绝对误差 (°)')
        axes[1,1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    # 5. 精度等级评估
    max_abs_error = calculated_error.abs().max()
    rms_error = np.sqrt((calculated_error**2).mean())
    
    print(f"\n📏 轴{ANALYSIS_AXIS}精度等级评估:")
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
    print(f"❌ 轴{ANALYSIS_AXIS}缺少位置数据，无法进行精度分析")## 3. 数据可视化探索

### 3.1 运动轨迹可视化# 轴{ANALYSIS_AXIS}专项统计分析
axis_cols = get_axis_columns(df, ANALYSIS_AXIS)

print(f"📈 轴{ANALYSIS_AXIS}详细统计信息:")
print("=" * 80)

if axis_cols:
    # 获取当前轴的所有相关数据
    axis_data = df[[col for col in axis_cols.values() if col in df.columns]].copy()
    
    if not axis_data.empty:
        print(f"\n🔧 轴{ANALYSIS_AXIS}基本统计:")
        axis_stats = axis_data.describe()
        print(axis_stats.round(4))
        
        # 位置相关分析
        pos_cols = [col for col in axis_cols.values() if 'position' in col]
        if pos_cols:
            print(f"\n📍 轴{ANALYSIS_AXIS}位置数据分析:")
            for col in pos_cols:
                if col in df.columns:
                    col_type = col.split('_')[0]  # sollposition, istposition, etc.
                    print(f"   {col_type}: 均值={df[col].mean():.4f}°, 标准差={df[col].std():.4f}°, 范围=[{df[col].min():.4f}, {df[col].max():.4f}]°")
        
        # 速度相关分析  
        vel_cols = [col for col in axis_cols.values() if 'geschwindigkeit' in col]
        if vel_cols:
            print(f"\n⚡ 轴{ANALYSIS_AXIS}速度数据分析:")
            for col in vel_cols:
                if col in df.columns:
                    col_type = col.split('_')[0]  # sollgeschwindigkeit, istgeschwindigkeit, etc.
                    print(f"   {col_type}: 均值={df[col].mean():.4f}°/s, 标准差={df[col].std():.4f}°/s, 范围=[{df[col].min():.4f}, {df[col].max():.4f}]°/s")
        
        # 力矩分析
        moment_cols = [col for col in axis_cols.values() if 'moment' in col]
        if moment_cols:
            print(f"\n🔄 轴{ANALYSIS_AXIS}力矩数据分析:")
            for col in moment_cols:
                if col in df.columns:
                    col_type = col.split('_')[0]  # sollmoment, istmoment
                    print(f"   {col_type}: 均值={df[col].mean():.4f}Nm, 标准差={df[col].std():.4f}Nm, 范围=[{df[col].min():.4f}, {df[col].max():.4f}]Nm")
        
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
    
    else:
        print(f"❌ 轴{ANALYSIS_AXIS}数据为空")
else:
    print(f"❌ 未找到轴{ANALYSIS_AXIS}的相关数据列")

print("=" * 80)### 2.2 数值字段统计分析# 数据基础统计信息
print("=" * 60)
print("📊 KUKA 机器人轨迹数据统计概览")
print("=" * 60)

# 基础信息
print(f"\n🔢 数据基础信息:")
print(f"   总记录数: {len(df):,}")
print(f"   字段数量: {len(df.columns)}")
print(f"   时间跨度: {df['zeit'].max() - df['zeit'].min():.2f} 秒")

# 机器人实例统计
if 'ins_id' in df.columns:
    print(f"\n🤖 机器人实例分布:")
    ins_counts = df['ins_id'].value_counts().sort_index()
    for ins_id, count in ins_counts.items():
        print(f"   机器人 {ins_id}: {count:,} 条记录 ({count/len(df)*100:.1f}%)")

# 轨迹记录统计
if 'trace_id' in df.columns:
    print(f"\n📍 轨迹记录分布:")
    trace_counts = df['trace_id'].value_counts().sort_index()
    print(f"   轨迹总数: {len(trace_counts)}")
    print(f"   平均每轨迹记录数: {trace_counts.mean():.0f}")
    print(f"   轨迹记录数范围: {trace_counts.min()} - {trace_counts.max()}")

# 运动类型统计
if 'motion_type' in df.columns:
    print(f"\n🔄 运动类型分布:")
    motion_counts = df['motion_type'].value_counts()
    for motion_type, count in motion_counts.items():
        print(f"   {motion_type}: {count:,} 条记录 ({count/len(df)*100:.1f}%)")

# 程序编号统计
if 'prog_num' in df.columns:
    print(f"\n💻 程序编号分布:")
    prog_counts = df['prog_num'].value_counts().sort_index()
    print(f"   程序总数: {len(prog_counts)}")
    for prog_num, count in list(prog_counts.items())[:5]:  # 显示前5个
        print(f"   程序 {prog_num}: {count:,} 条记录")
    if len(prog_counts) > 5:
        print(f"   ... 还有 {len(prog_counts)-5} 个程序")

print("=" * 60)## 2. 数据基础统计分析

### 2.1 整体数据概览# 设置分析参数
ANALYSIS_AXIS = 1  # 当前分析的轴编号 (1-6)，可修改此值来分析不同的轴
SAMPLE_SIZE = 1000  # 数据样本大小

print(f"🎯 当前分析轴: 轴{ANALYSIS_AXIS}")
print(f"📊 样本大小: {SAMPLE_SIZE}")

# 加载或生成数据
try:
    df = load_trace_data(engine, limit=SAMPLE_SIZE)
    if df is not None:
        print(f"\n📋 数据基本信息:")
        print(f"   - 数据形状: {df.shape}")
        print(f"   - 内存使用: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        print(f"   - 缺失值总数: {df.isnull().sum().sum()}")
        data_source = "数据库"
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

# 显示数据预览
print(f"\n🔍 数据预览:")
if len(df) > 0:
    # 只显示与当前分析轴相关的关键列
    preview_cols = ['zeit', 'motion_type'] + list(axis_cols.values())[:8]  # 限制显示列数
    available_cols = [col for col in preview_cols if col in df.columns]
    display(df[available_cols].head())
else:
    print("❌ 数据为空")### 加载示例数据

加载一个小样本数据进行初步探索。def load_trace_data(engine, limit=None, ins_id=None, trace_id=None, time_range=None):
    """
    从数据库加载KUKA机器人轨迹数据
    
    Parameters:
    -----------
    engine : SQLAlchemy engine
        数据库连接引擎
    limit : int, optional
        限制返回的记录数量
    ins_id : int, optional
        指定机器人实例ID
    trace_id : int, optional
        指定轨迹记录ID
    time_range : tuple, optional
        时间范围 (start_time, end_time)
    
    Returns:
    --------
    pandas.DataFrame or None
        加载的轨迹数据，失败时返回None
    """
    
    if engine is None:
        print("❌ 数据库引擎未初始化，无法加载数据")
        return None
    
    # 构建SQL查询
    query = "SELECT * FROM trace_data"
    conditions = []
    
    if ins_id is not None:
        conditions.append(f"ins_id = {ins_id}")
    
    if trace_id is not None:
        conditions.append(f"trace_id = {trace_id}")
    
    if time_range is not None:
        conditions.append(f"zeit BETWEEN {time_range[0]} AND {time_range[1]}")
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += " ORDER BY zeit ASC"
    
    if limit is not None:
        query += f" LIMIT {limit}"
    
    try:
        # 执行查询并返回DataFrame
        df = pd.read_sql_query(query, engine)
        
        if df.empty:
            print("⚠️ 查询结果为空")
            return None
        
        # 数据类型转换
        numeric_columns = [col for col in df.columns if col not in ['point_name', 'motion_type', 'created_at']]
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')
        
        # 时间戳处理
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        
        print(f"✅ 成功加载 {len(df)} 条轨迹数据记录")
        if 'zeit' in df.columns:
            print(f"📊 数据时间范围: {df['zeit'].min():.6f} - {df['zeit'].max():.6f} 秒")
        
        return df
        
    except Exception as e:
        print(f"❌ 数据加载失败: {e}")
        return None

def generate_mock_data(n_samples=1000, n_robots=3, random_seed=42):
    """
    生成模拟KUKA机器人数据
    
    Parameters:
    -----------
    n_samples : int
        生成的数据点数量
    n_robots : int
        机器人数量
    random_seed : int
        随机种子
    
    Returns:
    --------
    pandas.DataFrame
        模拟的机器人数据
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
    
    Parameters:
    -----------
    df : pandas.DataFrame
        轨迹数据DataFrame
    axis_num : int
        轴编号 (1-7)
    
    Returns:
    --------
    dict
        包含该轴所有相关列名的字典
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

def validate_data_quality(df):
    """
    验证数据质量
    
    Parameters:
    -----------
    df : pandas.DataFrame
        要验证的数据
    
    Returns:
    --------
    dict
        数据质量报告
    """
    report = {
        'total_records': len(df),
        'total_columns': len(df.columns),
        'missing_values': df.isnull().sum().sum(),
        'duplicate_records': df.duplicated().sum(),
        'data_types': df.dtypes.value_counts().to_dict(),
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
    }
    
    # 检查数值列的异常值
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outliers = {}
    
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outlier_mask = (df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))
        outliers[col] = outlier_mask.sum()
    
    report['outliers'] = outliers
    
    return report

print("✅ 数据加载和处理函数定义完成")### 数据加载函数

定义数据加载和预处理的辅助函数。# 数据库连接配置 - 请根据实际情况修改
DB_CONFIG = {
    'host': 'localhost',  # 数据库主机
    'port': 5432,         # 端口号
    'database': 'robot_db',  # 数据库名称
    'username': 'your_username',  # 用户名
    'password': 'your_password'   # 密码
}

def create_db_engine(config=None):
    """
    创建数据库连接引擎
    
    Parameters:
    -----------
    config : dict, optional
        数据库配置字典，如果为None则使用默认配置
    
    Returns:
    --------
    engine : SQLAlchemy engine or None
        数据库引擎对象，连接失败时返回None
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

# 尝试连接数据库
engine = create_db_engine()### 数据库连接配置

配置数据库连接参数，连接到包含KUKA机器人数据的数据库。# 数据处理和分析
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
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.io as pio

# 科学计算和机器学习
from scipy import stats
from scipy.signal import savgol_filter
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
pio.templates.default = "plotly_white"

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 设置图表显示参数
plt.rcParams['figure.figsize'] = (12, 8)
plt.rcParams['figure.dpi'] = 100

print("✅ 所有必要的库已成功导入")## 📋 使用说明

### 🎯 单轴分析模式

本notebook已优化为**单轴分析模式**，专注于对KUKA机器人单个轴的深入分析。

### 🔧 如何切换分析轴

要分析不同的轴，只需修改第一个代码单元格中的 `ANALYSIS_AXIS` 变量：

```python
ANALYSIS_AXIS = 1  # 修改此值来分析不同的轴 (1-6)
```

### 📊 分析内容

针对选定的轴，notebook将提供以下分析：

1. **位置精度分析**
   - 采集的位置跟随误差 vs 计算的位置误差对比
   - 位置跟踪性能评估
   - 精度等级评定

2. **速度精度分析**  
   - 采集的速度差 vs 计算的速度差对比
   - 速度跟踪延迟分析
   - 速度控制性能评估

3. **温度和电流监控**
   - 电机温度趋势分析
   - 电流消耗模式分析
   - 健康状态评估

4. **力矩和负载分析**
   - 力矩跟踪性能
   - 负载特性分析
   - 力矩与电流关系

### ⚠️ 注意事项

- 每次只分析一个轴，避免多轴对比的复杂性
- 通过修改 `ANALYSIS_AXIS` 变量可以快速切换分析目标
- 所有可视化和统计都针对当前选定的轴

---

## 1. 环境设置与数据加载

### 导入必要的库# KUKA 机器人轨迹数据探索分析

## 项目概述

本notebook用于分析KUKA机器人的轨迹数据，通过深入的数据探索和可视化来理解机器人的运行状态、性能表现和潜在问题。

## 数据表结构说明

### trace_data 表结构
KUKA机器人轨迹数据表包含以下主要数据类别：

#### 1. 基础信息字段
- **zeit**: 时间戳 (NUMERIC(15,6))
- **prog_num**: 程序编号 (NUMERIC(15,6))
- **point_name**: 点位名称 (VARCHAR(255))
- **motion_type**: 运动类型 (VARCHAR(100))

#### 2. 笛卡尔坐标系位置
- **x_act, y_act, z_act**: X/Y/Z轴实际位置
- **a_act, b_act, c_act**: A/B/C轴实际角度

#### 3. 关节轴位置
- **axis_pos_act1~7**: 轴1-7实际位置（支持7轴机器人）

#### 4. 笛卡尔速度
- **cart_vel_act**: 笛卡尔实际速度

#### 5. 各轴详细信息（轴1-7）
每个轴包含以下详细参数：
- **sollposition_X**: 目标位置
- **istposition_X**: 实际位置
- **positionsschleppfehler_X**: 位置跟随误差
- **sollgeschwindigkeit_X**: 目标速度
- **istgeschwindigkeit_X**: 实际速度
- **geschwindigkeitsdifferenz_X**: 速度差
- **sollmoment_X**: 目标力矩
- **istmoment_X**: 实际力矩
- **motortemperatur_X**: 电机温度
- **iststrom_X**: 实际电流

## 分析目标

### 主要分析方向：

1. **运动轨迹分析**
   - 3D轨迹可视化
   - 运动模式识别
   - 路径规划效率评估

2. **性能监控分析**
   - 各轴位置精度分析
   - 速度与加速度特性
   - 跟随误差分析

3. **健康状态监控**
   - 电机温度趋势
   - 电流消耗模式
   - 力矩负载分析

4. **异常检测**
   - 异常值识别
   - 性能退化检测
   - 故障预测模型

5. **优化建议**
   - 运动参数优化
   - 维护建议
   - 性能提升方案

---

## 数据探索流程

本notebook将按以下步骤进行数据探索：
1. 数据加载与预处理
2. 基础统计分析
3. 可视化探索
4. 深度分析
5. 结论与建议