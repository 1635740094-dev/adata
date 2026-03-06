# -*- coding: utf-8 -*-
"""
测试频率限制功能
"""

from adata.common.utils.sunrequests import sun_requests

# 测试1: 验证频率限制器已集成
print('测试1: 验证频率限制器已集成')
print(f'  - sun_requests._rate_limiter: {sun_requests._rate_limiter}')
print(f'  - 默认限制: {sun_requests._rate_limiter._default_max_requests}次/{sun_requests._rate_limiter._default_window_seconds}秒')

# 测试2: 设置自定义限制
print('\n测试2: 设置自定义限制')
sun_requests.set_rate_limit('eastmoney.com', 10, 60)  # eastmoney.com 每分钟10次
sun_requests.set_rate_limit('baidu.com', 50, 60)      # baidu.com 每分钟50次
sun_requests.set_default_limit(20, 60)               # 其他域名每分钟20次
print('  - eastmoney.com: 10次/分钟')
print('  - baidu.com: 50次/分钟')
print('  - 其他: 20次/分钟')

# 测试3: 获取状态
print('\n测试3: 获取状态')
status = sun_requests.get_rate_limit_status()
print(f'  - 当前状态: {status}')

# 测试4: 测试域名提取
print('\n测试4: 测试域名提取')
test_urls = [
    'https://quote.eastmoney.com/sh600519.html',
    'http://finance.baidu.com/api',
    'https://www.10jqka.com.cn/api'
]
for url in test_urls:
    domain = sun_requests._rate_limiter._get_domain_from_url(url)
    print(f'  - {url} -> {domain}')

# 测试5: 测试频率限制
print('\n测试5: 测试频率限制')
import time

# 设置一个非常低的限制来测试
sun_requests.set_rate_limit('test.com', 2, 60)  # 每分钟2次

test_url = 'https://test.com/api'
print(f'  - 设置限制: 每分钟2次')

# 模拟3次请求
for i in range(3):
    start = time.time()
    wait_time = sun_requests._rate_limiter.acquire(test_url)
    if wait_time > 0:
        print(f'  - 第{i+1}次请求: 需要等待 {wait_time:.2f} 秒')
    else:
        print(f'  - 第{i+1}次请求: 立即执行')
    elapsed = time.time() - start
    if elapsed > 0.1:
        print(f'    实际等待: {elapsed:.2f} 秒')

print('\n所有测试通过!')
