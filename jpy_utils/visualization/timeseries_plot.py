"""
时间序列数据可视化工具

提供交互式时间序列折线图和时间范围选择功能。
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from typing import Dict, List, Union, Optional, Tuple, Any
import numpy as np


def plot_timeseries(
    x_data: Union[List, pd.Series, np.ndarray],
    y_data: Union[List, pd.Series, np.ndarray],
    title: str = "时间序列图",
    x_label: str = "时间",
    y_label: str = "数值",
    line_color: str = "#1f77b4",
    show_points: bool = False,
    width: int = 1000,
    height: int = 600
) -> go.Figure:
    """
    创建单条时间序列折线图
    
    Args:
        x_data (Union[List, pd.Series, np.ndarray]): 时间数据（横坐标）
        y_data (Union[List, pd.Series, np.ndarray]): 数值数据（纵坐标）
        title (str, optional): 图表标题. Defaults to "时间序列图".
        x_label (str, optional): 横坐标标签. Defaults to "时间".
        y_label (str, optional): 纵坐标标签. Defaults to "数值".
        line_color (str, optional): 折线颜色. Defaults to "#1f77b4".
        show_points (bool, optional): 是否显示数据点. Defaults to False.
        width (int, optional): 图表宽度. Defaults to 1000.
        height (int, optional): 图表高度. Defaults to 600.
    
    Returns:
        go.Figure: Plotly图表对象
    
    Examples:
        >>> import pandas as pd
        >>> dates = pd.date_range('2023-01-01', periods=100, freq='D')
        >>> values = np.random.randn(100).cumsum()
        >>> fig = plot_timeseries(dates, values, title="股价走势")
        >>> fig.show()
    """
    fig = go.Figure()
    
    # 确定模式
    mode = 'lines+markers' if show_points else 'lines'
    
    fig.add_trace(go.Scatter(
        x=x_data,
        y=y_data,
        mode=mode,
        line=dict(color=line_color, width=2),
        marker=dict(size=4) if show_points else None,
        hovertemplate='<b>时间:</b> %{x}<br><b>数值:</b> %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=16)),
        xaxis_title=x_label,
        yaxis_title=y_label,
        width=width,
        height=height,
        hovermode='x unified',
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # 设置网格
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black'
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black'
    )
    
    return fig


def plot_multiple_timeseries(
    data_dict: Dict[str, Dict[str, Union[List, pd.Series, np.ndarray]]],
    title: str = "多条时间序列对比图",
    x_label: str = "时间",
    y_label: str = "数值",
    colors: Optional[List[str]] = None,
    show_points: bool = False,
    width: int = 1200,
    height: int = 700
) -> go.Figure:
    """
    创建多条时间序列折线图
    
    Args:
        data_dict (Dict[str, Dict[str, Union[List, pd.Series, np.ndarray]]]): 
            数据字典，格式: {'系列名': {'x': x_data, 'y': y_data}}
        title (str, optional): 图表标题. Defaults to "多条时间序列对比图".
        x_label (str, optional): 横坐标标签. Defaults to "时间".
        y_label (str, optional): 纵坐标标签. Defaults to "数值".
        colors (Optional[List[str]], optional): 颜色列表. Defaults to None.
        show_points (bool, optional): 是否显示数据点. Defaults to False.
        width (int, optional): 图表宽度. Defaults to 1200.
        height (int, optional): 图表高度. Defaults to 700.
    
    Returns:
        go.Figure: Plotly图表对象
    
    Examples:
        >>> data = {
        ...     '系列1': {'x': dates1, 'y': values1},
        ...     '系列2': {'x': dates2, 'y': values2}
        ... }
        >>> fig = plot_multiple_timeseries(data, title="多股票对比")
        >>> fig.show()
    """
    if colors is None:
        colors = px.colors.qualitative.Set1
    
    fig = go.Figure()
    
    mode = 'lines+markers' if show_points else 'lines'
    
    for i, (series_name, series_data) in enumerate(data_dict.items()):
        color = colors[i % len(colors)]
        
        fig.add_trace(go.Scatter(
            x=series_data['x'],
            y=series_data['y'],
            mode=mode,
            name=series_name,
            line=dict(color=color, width=2),
            marker=dict(size=4) if show_points else None,
            hovertemplate=f'<b>{series_name}</b><br><b>时间:</b> %{{x}}<br><b>数值:</b> %{{y}}<extra></extra>'
        ))
    
    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=16)),
        xaxis_title=x_label,
        yaxis_title=y_label,
        width=width,
        height=height,
        hovermode='x unified',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # 设置网格
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black'
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black'
    )
    
    return fig


def create_interactive_plot(
    data_dict: Dict[str, Dict[str, Union[List, pd.Series, np.ndarray]]],
    title: str = "交互式时间序列图",
    x_label: str = "时间",
    y_label: str = "数值",
    enable_zoom: bool = True,
    enable_pan: bool = True,
    enable_select: bool = True,
    enable_crossfilter: bool = True,
    width: int = 1200,
    height: int = 700
) -> go.Figure:
    """
    创建具有完整交互功能的时间序列图
    
    Args:
        data_dict (Dict[str, Dict[str, Union[List, pd.Series, np.ndarray]]]): 
            数据字典，格式: {'系列名': {'x': x_data, 'y': y_data}}
        title (str, optional): 图表标题. Defaults to "交互式时间序列图".
        x_label (str, optional): 横坐标标签. Defaults to "时间".
        y_label (str, optional): 纵坐标标签. Defaults to "数值".
        enable_zoom (bool, optional): 启用缩放. Defaults to True.
        enable_pan (bool, optional): 启用平移. Defaults to True.
        enable_select (bool, optional): 启用选择. Defaults to True.
        enable_crossfilter (bool, optional): 启用交叉筛选. Defaults to True.
        width (int, optional): 图表宽度. Defaults to 1200.
        height (int, optional): 图表高度. Defaults to 700.
    
    Returns:
        go.Figure: 交互式Plotly图表对象
    
    Examples:
        >>> fig = create_interactive_plot(data, title="交互式股价图")
        >>> fig.show()
    """
    fig = plot_multiple_timeseries(
        data_dict=data_dict,
        title=title,
        x_label=x_label,
        y_label=y_label,
        width=width,
        height=height
    )
    
    # 配置交互功能
    config = {
        'displayModeBar': True,
        'displaylogo': False,
        'modeBarButtonsToRemove': []
    }
    
    if not enable_zoom:
        config['modeBarButtonsToRemove'].extend(['zoom2d', 'zoomIn2d', 'zoomOut2d', 'autoScale2d'])
    
    if not enable_pan:
        config['modeBarButtonsToRemove'].append('pan2d')
    
    if not enable_select:
        config['modeBarButtonsToRemove'].extend(['select2d', 'lasso2d'])
    
    # 添加范围选择器
    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1天", step="day", stepmode="backward"),
                    dict(count=7, label="7天", step="day", stepmode="backward"),
                    dict(count=30, label="30天", step="day", stepmode="backward"),
                    dict(count=90, label="90天", step="day", stepmode="backward"),
                    dict(step="all", label="全部")
                ])
            ),
            rangeslider=dict(visible=True),
            type="date"
        )
    )
    
    return fig


class TimeRangeSelector:
    """时间范围选择器类"""
    
    def __init__(self, min_date: Union[str, datetime], max_date: Union[str, datetime]):
        """
        初始化时间范围选择器
        
        Args:
            min_date (Union[str, datetime]): 最小日期
            max_date (Union[str, datetime]): 最大日期
        """
        if isinstance(min_date, str):
            self.min_date = pd.to_datetime(min_date)
        else:
            self.min_date = min_date
            
        if isinstance(max_date, str):
            self.max_date = pd.to_datetime(max_date)
        else:
            self.max_date = max_date
    
    def get_date_range(self, start_date: Union[str, datetime], 
                      end_date: Union[str, datetime]) -> Tuple[datetime, datetime]:
        """
        获取指定的日期范围
        
        Args:
            start_date (Union[str, datetime]): 开始日期
            end_date (Union[str, datetime]): 结束日期
        
        Returns:
            Tuple[datetime, datetime]: 开始和结束日期元组
        
        Examples:
            >>> selector = TimeRangeSelector('2023-01-01', '2023-12-31')
            >>> start, end = selector.get_date_range('2023-06-01', '2023-06-30')
        """
        if isinstance(start_date, str):
            start = pd.to_datetime(start_date)
        else:
            start = start_date
            
        if isinstance(end_date, str):
            end = pd.to_datetime(end_date)
        else:
            end = end_date
        
        # 确保日期在有效范围内
        start = max(start, self.min_date)
        end = min(end, self.max_date)
        
        if start > end:
            raise ValueError("开始日期不能大于结束日期")
        
        return start, end
    
    def get_last_n_days(self, n_days: int, end_date: Optional[Union[str, datetime]] = None) -> Tuple[datetime, datetime]:
        """
        获取最近N天的日期范围
        
        Args:
            n_days (int): 天数
            end_date (Optional[Union[str, datetime]], optional): 结束日期. Defaults to None（使用最大日期）.
        
        Returns:
            Tuple[datetime, datetime]: 开始和结束日期元组
        
        Examples:
            >>> start, end = selector.get_last_n_days(30)  # 最近30天
        """
        if end_date is None:
            end = self.max_date
        else:
            if isinstance(end_date, str):
                end = pd.to_datetime(end_date)
            else:
                end = end_date
        
        start = end - timedelta(days=n_days-1)
        start = max(start, self.min_date)
        
        return start, end
    
    def get_month_range(self, year: int, month: int) -> Tuple[datetime, datetime]:
        """
        获取指定月份的日期范围
        
        Args:
            year (int): 年份
            month (int): 月份
        
        Returns:
            Tuple[datetime, datetime]: 该月的开始和结束日期
        
        Examples:
            >>> start, end = selector.get_month_range(2023, 6)  # 2023年6月
        """
        start = datetime(year, month, 1)
        
        # 计算月末日期
        if month == 12:
            end = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end = datetime(year, month + 1, 1) - timedelta(days=1)
        
        # 确保在有效范围内
        start = max(start, self.min_date)
        end = min(end, self.max_date)
        
        return start, end
    
    def create_time_selector_widget(self) -> go.Figure:
        """
        创建时间选择器小部件
        
        Returns:
            go.Figure: 时间选择器图表
        
        Examples:
            >>> widget = selector.create_time_selector_widget()
            >>> widget.show()
        """
        # 创建一个简单的时间轴显示
        date_range = pd.date_range(self.min_date, self.max_date, freq='D')
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=date_range,
            y=[1] * len(date_range),
            mode='markers',
            marker=dict(size=3, color='blue', opacity=0.6),
            hovertemplate='<b>日期:</b> %{x}<extra></extra>',
            showlegend=False
        ))
        
        fig.update_layout(
            title="时间范围选择器",
            xaxis_title="日期",
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            height=150,
            margin=dict(l=50, r=50, t=50, b=50),
            xaxis=dict(
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        
        return fig


def plot_ms_timeseries(
    timestamps_ms: Union[List, np.ndarray],
    values: Union[List, np.ndarray],
    title: str = "毫秒级时间序列图",
    y_label: str = "数值",
    line_color: str = "#1f77b4",
    show_points: bool = False,
    width: int = 1000,
    height: int = 600
) -> go.Figure:
    """
    创建毫秒级时间序列图（横坐标为过去多少毫秒）
    
    Args:
        timestamps_ms (Union[List, np.ndarray]): 毫秒时间戳数据
        values (Union[List, np.ndarray]): 数值数据
        title (str, optional): 图表标题. Defaults to "毫秒级时间序列图".
        y_label (str, optional): 纵坐标标签. Defaults to "数值".
        line_color (str, optional): 折线颜色. Defaults to "#1f77b4".
        show_points (bool, optional): 是否显示数据点. Defaults to False.
        width (int, optional): 图表宽度. Defaults to 1000.
        height (int, optional): 图表高度. Defaults to 600.
    
    Returns:
        go.Figure: Plotly图表对象
    
    Examples:
        >>> timestamps = [0, 100, 200, 300, 400]  # 毫秒
        >>> values = [1, 2, 1.5, 3, 2.5]
        >>> fig = plot_ms_timeseries(timestamps, values)
        >>> fig.show()
    """
    fig = go.Figure()
    
    mode = 'lines+markers' if show_points else 'lines'
    
    fig.add_trace(go.Scatter(
        x=timestamps_ms,
        y=values,
        mode=mode,
        line=dict(color=line_color, width=2),
        marker=dict(size=4) if show_points else None,
        hovertemplate='<b>时间:</b> %{x} ms<br><b>数值:</b> %{y}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, x=0.5, font=dict(size=16)),
        xaxis_title="时间 (ms)",
        yaxis_title=y_label,
        width=width,
        height=height,
        hovermode='x unified',
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # 设置网格
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black'
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='lightgray',
        showline=True,
        linewidth=1,
        linecolor='black'
    )
    
    return fig