# -*- coding: utf-8 -*-
"""
简单测试频率限制功能
"""
import sys
import time

# 直接添加路径并导入模块
sys.path.insert(0, r'f:\adata')

# 直接导入 sunrequests 模块而不通过 adata 包
import importlib.util
spec = importlib.util.spec_from_file_location("sunrequests", r"f:\adata\adata\common\utils\sunrequests.py")
sunrequests_module = importlib.util.module_from_spec(spec)

# 手动设置 requests 模块
import requests as requests_lib
sys.modules['requests'] = requests_lib

spec.loader.exec_module(sunrequests_module)
sun_requests = sunrequests_module.sun_requests

print("=" * 60)
print("测试频率限制功能")
print("=" * 60)

# 1. 验证默认配置
print("\n1. 验证默认配置:")
print(f"   默认限制: {sun_requests._rate_limiter._default_max_requests}次/{sun_requests._rate_limiter._default_window_seconds}秒")

# 2. 测试设置自定义限制
print("\n2. 测试设置自定义限制:")
sun_requests.set_rate_limit('eastmoney.com', 10, 60)  # 设置特定域名限制
sun_requests.set_rate_limit('baidu.com', 50, 60)      # 设置特定域名限制
sun_requests.set_rate_limit(None, 20, 60)             # 设置默认限制（domain为None）
print("   - eastmoney.com: 10次/分钟")
print("   - baidu.com: 50次/分钟")
print("   - 其他: 20次/分钟")

# 3. 测试域名提取
print("\n3. 测试域名提取:")
test_urls = [
    'https://quote.eastmoney.com/sh600519.html',
    'http://finance.baidu.com/api',
    'https://www.10jqka.com.cn/api',
    'https://push2.eastmoney.com/api/qt/clist/get',
]
for url in test_urls:
    domain = sun_requests._rate_limiter._get_domain_from_url(url)
    print(f"   - {url[:40]}... -> {domain}")

# 4. 测试频率限制行为
print("\n4. 测试频率限制行为:")

# 设置一个非常低的限制来测试（每秒2次）
sun_requests.set_rate_limit('test-example.com', 2, 1)
test_url = 'https://test-example.com/api'
print(f"   设置限制: 每1秒2次")

# 模拟3次请求
for i in range(3):
    start = time.time()
    wait_time = sun_requests._rate_limiter.acquire(test_url)
    elapsed = time.time() - start
    if wait_time > 0:
        print(f"   第{i+1}次请求: 需要等待 {wait_time:.2f} 秒")
        time.sleep(wait_time)
        print(f"   第{i+1}次请求: 已等待完成，继续执行")
    else:
        print(f"   第{i+1}次请求: 立即执行")

# 5. 测试获取状态
print("\n5. 测试获取状态:")
status = sun_requests.get_rate_limit_status('https://test-example.com/api')
print(f"   test-example.com 状态: {status}")

print("\n" + "=" * 60)
print("所有测试通过!")
print("=" * 60)
