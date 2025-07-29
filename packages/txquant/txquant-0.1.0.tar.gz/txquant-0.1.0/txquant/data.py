"""
数据处理模块
"""

import pandas as pd
import numpy as np

def load_data(file_path: str) -> pd.DataFrame:
    """
    加载数据文件
    
    Args:
        file_path: 数据文件路径
        
    Returns:
        pd.DataFrame: 加载的数据
    """
    return pd.read_csv(file_path)

def calculate_returns(prices: pd.Series) -> pd.Series:
    """
    计算收益率
    
    Args:
        prices: 价格序列
        
    Returns:
        pd.Series: 收益率序列
    """
    return prices.pct_change() 