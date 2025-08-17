"""
可视化模块使用示例

演示如何使用 jpy_utils.visualization 模块进行时间序列数据可视化
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 导入可视化模块
from jpy_utils.visualization import (
    plot_timeseries,
    plot_multiple_timeseries,
    create_interactive_plot,
    plot_ms_timeseries,
    TimeRangeSelector
)

def generate_sample_data():
    """生成示例时间序列数据"""
    # 生成日期序列
    start_date = datetime(2023, 1, 1)
    end_date = datetime(2023, 12, 31)
    dates = pd.date_range(start_date, end_date, freq='D')
    
    # 生成多个时间序列
    np.random.seed(42)  # 固定随机种子，确保结果可重复
    
    # 股票A：呈上升趋势
    stock_a = 100 + np.cumsum(np.random.randn(len(dates)) * 2 + 0.1)
    
    # 股票B：波动较大
    stock_b = 150 + np.cumsum(np.random.randn(len(dates)) * 3)
    
    # 股票C：季节性变化
    stock_c = 120 + 20 * np.sin(np.arange(len(dates)) * 2 * np.pi / 365) + np.cumsum(np.random.randn(len(dates)) * 1.5)
    
    return dates, stock_a, stock_b, stock_c

def example_1_single_timeseries():
    """示例1：单条时间序列图"""
    print("=== 示例1：单条时间序列图 ===")
    
    dates, stock_a, _, _ = generate_sample_data()
    
    # 创建单条时间序列图
    fig = plot_timeseries(
        x_data=dates,
        y_data=stock_a,
        title="股票A价格走势",
        x_label="日期",
        y_label="价格 ($)",
        line_color="#FF6B6B",
        show_points=False
    )
    
    # 可以调用 fig.show() 来显示图表
    # fig.show()
    
    # 保存为HTML文件
    fig.write_html("example_single_timeseries.html")
    print("单条时间序列图已保存为 example_single_timeseries.html")

def example_2_multiple_timeseries():
    """示例2：多条时间序列对比图"""
    print("\n=== 示例2：多条时间序列对比图 ===")
    
    dates, stock_a, stock_b, stock_c = generate_sample_data()
    
    # 准备多条时间序列数据
    data_dict = {
        '股票A': {'x': dates, 'y': stock_a},
        '股票B': {'x': dates, 'y': stock_b},
        '股票C': {'x': dates, 'y': stock_c}
    }
    
    # 创建多条时间序列图
    fig = plot_multiple_timeseries(
        data_dict=data_dict,
        title="三只股票价格对比",
        x_label="日期",
        y_label="价格 ($)",
        colors=['#FF6B6B', '#4ECDC4', '#45B7D1'],
        show_points=False
    )
    
    fig.write_html("example_multiple_timeseries.html")
    print("多条时间序列图已保存为 example_multiple_timeseries.html")

def example_3_interactive_plot():
    """示例3：交互式时间序列图"""
    print("\n=== 示例3：交互式时间序列图 ===")
    
    dates, stock_a, stock_b, stock_c = generate_sample_data()
    
    data_dict = {
        '股票A': {'x': dates, 'y': stock_a},
        '股票B': {'x': dates, 'y': stock_b},
        '股票C': {'x': dates, 'y': stock_c}
    }
    
    # 创建交互式图表
    fig = create_interactive_plot(
        data_dict=data_dict,
        title="交互式股票价格图表",
        x_label="日期",
        y_label="价格 ($)",
        enable_zoom=True,
        enable_pan=True,
        enable_select=True
    )
    
    fig.write_html("example_interactive_plot.html")
    print("交互式时间序列图已保存为 example_interactive_plot.html")

def example_4_millisecond_timeseries():
    """示例4：毫秒级时间序列图"""
    print("\n=== 示例4：毫秒级时间序列图 ===")
    
    # 生成毫秒级时间戳数据（模拟实时数据）
    timestamps_ms = list(range(0, 5000, 50))  # 0到5秒，每50ms一个点
    
    # 生成模拟的传感器数据
    np.random.seed(42)
    values = 50 + 10 * np.sin(np.array(timestamps_ms) / 1000 * 2 * np.pi) + np.random.randn(len(timestamps_ms)) * 2
    
    # 创建毫秒级时间序列图
    fig = plot_ms_timeseries(
        timestamps_ms=timestamps_ms,
        values=values,
        title="传感器实时数据（毫秒级）",
        y_label="传感器读数",
        line_color="#9B59B6",
        show_points=True
    )
    
    fig.write_html("example_ms_timeseries.html")
    print("毫秒级时间序列图已保存为 example_ms_timeseries.html")

def example_5_time_range_selector():
    """示例5：时间范围选择器"""
    print("\n=== 示例5：时间范围选择器 ===")
    
    # 创建时间范围选择器
    selector = TimeRangeSelector('2023-01-01', '2023-12-31')
    
    # 获取指定日期范围
    start, end = selector.get_date_range('2023-06-01', '2023-06-30')
    print(f"指定范围: {start.date()} 到 {end.date()}")
    
    # 获取最近30天
    start, end = selector.get_last_n_days(30)
    print(f"最近30天: {start.date()} 到 {end.date()}")
    
    # 获取指定月份
    start, end = selector.get_month_range(2023, 6)
    print(f"2023年6月: {start.date()} 到 {end.date()}")
    
    # 创建时间选择器小部件
    widget = selector.create_time_selector_widget()
    widget.write_html("example_time_selector.html")
    print("时间选择器小部件已保存为 example_time_selector.html")

def example_6_filtered_data_visualization():
    """示例6：使用时间范围选择器过滤数据进行可视化"""
    print("\n=== 示例6：过滤数据可视化 ===")
    
    dates, stock_a, stock_b, stock_c = generate_sample_data()
    
    # 创建时间范围选择器
    selector = TimeRangeSelector('2023-01-01', '2023-12-31')
    
    # 获取第二季度数据
    q2_start, q2_end = selector.get_date_range('2023-04-01', '2023-06-30')
    
    # 过滤数据
    mask = (dates >= q2_start) & (dates <= q2_end)
    filtered_dates = dates[mask]
    filtered_stock_a = stock_a[mask]
    filtered_stock_b = stock_b[mask]
    filtered_stock_c = stock_c[mask]
    
    # 可视化过滤后的数据
    data_dict = {
        '股票A': {'x': filtered_dates, 'y': filtered_stock_a},
        '股票B': {'x': filtered_dates, 'y': filtered_stock_b},
        '股票C': {'x': filtered_dates, 'y': filtered_stock_c}
    }
    
    fig = plot_multiple_timeseries(
        data_dict=data_dict,
        title="2023年第二季度股票价格走势",
        x_label="日期",
        y_label="价格 ($)"
    )
    
    fig.write_html("example_filtered_data.html")
    print("过滤数据可视化已保存为 example_filtered_data.html")

def main():
    """运行所有示例"""
    print("jpy_utils 可视化模块示例演示")
    print("=" * 50)
    
    try:
        example_1_single_timeseries()
        example_2_multiple_timeseries()
        example_3_interactive_plot()
        example_4_millisecond_timeseries()
        example_5_time_range_selector()
        example_6_filtered_data_visualization()
        
        print("\n" + "=" * 50)
        print("所有示例运行完成！")
        print("生成的HTML文件可以在浏览器中打开查看图表。")
        print("\n功能特点：")
        print("- 鼠标悬停显示具体数值")
        print("- 支持缩放和平移")
        print("- 时间范围选择器")
        print("- 多条折线对比")
        print("- 毫秒级时间序列支持")
        
    except ImportError as e:
        print(f"导入错误: {e}")
        print("请确保已安装所需依赖: pip install plotly pandas numpy")
    except Exception as e:
        print(f"运行错误: {e}")

if __name__ == "__main__":
    main()