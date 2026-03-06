# -*- coding: utf-8 -*-
"""
测试频率限制功能
"""

import os
import sys
import time

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from adata.common.utils import requests


def test_rate_limit():
    """测试频率限制功能"""
    print("开始测试频率限制...")
    start_time = time.time()
    
    # 测试默认限制（30次/分钟）
    print("\n测试默认频率限制（30次/分钟）:")
    for i in range(35):
        res = requests.request('get', 'https://www.baidu.com')
        print(f'请求 {i+1} 完成，状态码: {res.status_code}，耗时: {time.time() - start_time:.2f} 秒')
    
    # 测试自定义限制
    print("\n测试自定义频率限制（5次/10秒）:")
    requests.set_rate_limit('www.baidu.com', max_requests=5, time_window=10)
    start_time = time.time()
    for i in range(8):
        res = requests.request('get', 'https://www.baidu.com')
        print(f'请求 {i+1} 完成，状态码: {res.status_code}，耗时: {time.time() - start_time:.2f} 秒')


if __name__ == "__main__":
    test_rate_limit()
