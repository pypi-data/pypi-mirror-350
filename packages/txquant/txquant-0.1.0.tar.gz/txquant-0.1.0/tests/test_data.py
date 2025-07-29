"""
测试数据处理模块
"""

import pytest
import pandas as pd
import numpy as np
from txquant.data import calculate_returns

def test_calculate_returns():
    # 创建测试数据
    prices = pd.Series([100, 110, 99, 121])
    expected_returns = pd.Series([np.nan, 0.1, -0.1, 0.222222])
    
    # 计算收益率
    actual_returns = calculate_returns(prices)
    
    # 验证结果
    pd.testing.assert_series_equal(
        actual_returns,
        expected_returns,
        check_names=False,
        check_index=False
    ) 