# -*- coding: utf-8 -*-
"""
代理:https://jahttp.zhimaruanjian.com/getapi/

@desc: adata 请求工具类
@author: 1nchaos
@time:2023/3/30
@log: 封装请求次数
@log: 2026/03/05: 添加频率限制功能
"""

import threading
import time
 HEAD
from urllib.parse import urlparse
from collections import defaultdict, deque

import urllib.parse
9ce4090857c539647fe2ec3f5b989ac553be7b30

import requests


class SunProxy(object):
    _data = {}
    _instance_lock = threading.Lock()

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(SunProxy, "_instance"):
            with SunProxy._instance_lock:
                if not hasattr(SunProxy, "_instance"):
                    SunProxy._instance = object.__new__(cls)

    @classmethod
    def set(cls, key, value):
        cls._data[key] = value

    @classmethod
    def get(cls, key):
        return cls._data.get(key)

    @classmethod
    def delete(cls, key):
        if key in cls._data:
            del cls._data[key]


<<<<<<< HEAD
class RateLimiter:
    """
    基于域名的频率限制器
    默认每分钟每个域名最多30次请求
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init()
        return cls._instance

    def _init(self):
        # 每个域名的请求时间队列 {domain: deque([timestamp, ...])}
        self._domain_requests = defaultdict(deque)
        # 每个域名的限制配置 {domain: {'max_requests': int, 'window_seconds': int}}
        self._domain_limits = {}
        # 默认限制: 每分钟30次
        self._default_max_requests = 30
        self._default_window_seconds = 60
        self._config_lock = threading.Lock()

    def set_limit(self, domain: str, max_requests: int = 30, window_seconds: int = 60):
        """
        设置指定域名的频率限制
        :param domain: 域名，如 'eastmoney.com'
        :param max_requests: 在窗口时间内最大请求次数
        :param window_seconds: 时间窗口（秒）
        """
        with self._config_lock:
            self._domain_limits[domain] = {
                'max_requests': max_requests,
                'window_seconds': window_seconds
            }

    def set_default_limit(self, max_requests: int = 30, window_seconds: int = 60):
        """
        设置默认的频率限制
        :param max_requests: 在窗口时间内最大请求次数
        :param window_seconds: 时间窗口（秒）
        """
        self._default_max_requests = max_requests
        self._default_window_seconds = window_seconds

    def _get_domain_from_url(self, url: str) -> str:
        """从URL中提取域名"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            # 移除端口号
            if ':' in domain:
                domain = domain.split(':')[0]
            return domain
        except Exception:
            return url.lower()

    def _get_limit(self, domain: str) -> tuple:
        """获取域名的限制配置"""
        with self._config_lock:
            if domain in self._domain_limits:
                config = self._domain_limits[domain]
                return config['max_requests'], config['window_seconds']
        return self._default_max_requests, self._default_window_seconds

    def acquire(self, url: str) -> float:
        """
        获取请求许可，如果超限则等待
        :param url: 请求的URL
        :return: 实际等待的时间（秒）
        """
        domain = self._get_domain_from_url(url)
        max_requests, window_seconds = self._get_limit(domain)

        with self._config_lock:
            now = time.time()
            requests_queue = self._domain_requests[domain]

            # 清理过期的请求记录
            while requests_queue and requests_queue[0] < now - window_seconds:
                requests_queue.popleft()

            # 检查是否需要等待
            if len(requests_queue) >= max_requests:
                # 需要等待直到最早的请求过期
                wait_time = requests_queue[0] + window_seconds - now
                if wait_time > 0:
                    return wait_time

            # 记录当前请求
            requests_queue.append(now)
            return 0

    def get_status(self, url: str = None) -> dict:
        """
        获取频率限制状态
        :param url: 如果提供URL，则返回该域名的状态；否则返回所有域名的状态
        :return: 状态字典
        """
        with self._config_lock:
            now = time.time()
            if url:
                domain = self._get_domain_from_url(url)
                max_requests, window_seconds = self._get_limit(domain)
                requests_queue = self._domain_requests.get(domain, deque())
                # 清理过期记录
                valid_requests = [t for t in requests_queue if t >= now - window_seconds]
                return {
                    'domain': domain,
                    'current_requests': len(valid_requests),
                    'max_requests': max_requests,
                    'window_seconds': window_seconds,
                    'remaining': max(0, max_requests - len(valid_requests))
                }
            else:
                result = {}
                for domain, requests_queue in self._domain_requests.items():
                    max_requests, window_seconds = self._get_limit(domain)
                    valid_requests = [t for t in requests_queue if t >= now - window_seconds]
                    result[domain] = {
                        'current_requests': len(valid_requests),
                        'max_requests': max_requests,
                        'window_seconds': window_seconds,
                        'remaining': max(0, max_requests - len(valid_requests))
                    }
                return result
=======
class RateLimiter(object):
    """频率限制器"""
    _instance_lock = threading.Lock()
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._instance_lock:
                if not cls._instance:
                    cls._instance = object.__new__(cls)
                    cls._instance._init()
        return cls._instance
    
    def _init(self):
        """初始化频率限制器"""
        self._domain_limits = {}  # 存储每个域名的限制配置
        self._domain_requests = {}  # 存储每个域名的请求记录
        self._lock = threading.Lock()
    
    def set_limit(self, domain, max_requests=30, time_window=60):
        """
        设置域名的频率限制
        :param domain: 域名
        :param max_requests: 最大请求次数，默认30次
        :param time_window: 时间窗口，默认60秒
        """
        with self._lock:
            self._domain_limits[domain] = (max_requests, time_window)
    
    def get_limit(self, domain):
        """
        获取域名的频率限制
        :param domain: 域名
        :return: (max_requests, time_window)
        """
        return self._domain_limits.get(domain, (30, 60))
    
    def check_rate_limit(self, domain):
        """
        检查域名是否超过频率限制
        :param domain: 域名
        :return: True 表示未超过限制，False 表示超过限制
        """
        with self._lock:
            max_requests, time_window = self.get_limit(domain)
            current_time = time.time()
            
            # 初始化该域名的请求记录
            if domain not in self._domain_requests:
                self._domain_requests[domain] = []
            
            # 清理过期的请求记录
            self._domain_requests[domain] = [t for t in self._domain_requests[domain] if current_time - t < time_window]
            
            # 检查是否超过限制
            if len(self._domain_requests[domain]) < max_requests:
                # 记录本次请求
                self._domain_requests[domain].append(current_time)
                return True
            else:
                # 计算需要等待的时间
                oldest_request = self._domain_requests[domain][0]
                wait_time = time_window - (current_time - oldest_request)
                if wait_time > 0:
                    time.sleep(wait_time)
                    # 清理过期记录并重新检查
                    self._domain_requests[domain] = [t for t in self._domain_requests[domain] if current_time - t < time_window]
                    self._domain_requests[domain].append(time.time())
                return True
>>>>>>> 9ce4090857c539647fe2ec3f5b989ac553be7b30


class SunRequests(object):
    def __init__(self, sun_proxy: SunProxy = None) -> None:
        super().__init__()
        self.sun_proxy = sun_proxy
<<<<<<< HEAD
        self._rate_limiter = RateLimiter()

    def set_rate_limit(self, domain: str = None, max_requests: int = 30, window_seconds: int = 60):
        """
        设置频率限制
        :param domain: 域名，如 'eastmoney.com'；如果为None则设置默认限制
        :param max_requests: 在窗口时间内最大请求次数
        :param window_seconds: 时间窗口（秒）
        """
        if domain:
            self._rate_limiter.set_limit(domain, max_requests, window_seconds)
        else:
            self._rate_limiter.set_default_limit(max_requests, window_seconds)

    def get_rate_limit_status(self, url: str = None) -> dict:
        """
        获取频率限制状态
        :param url: 如果提供URL，则返回该域名的状态；否则返回所有域名的状态
        :return: 状态字典
        """
        return self._rate_limiter.get_status(url)
=======
        self.rate_limiter = RateLimiter()
>>>>>>> 9ce4090857c539647fe2ec3f5b989ac553be7b30

    def request(self, method='get', url=None, times=3, retry_wait_time=1588, proxies=None, wait_time=None, **kwargs):
        """
        简单封装的请求，参考requests，增加循环次数和次数之间的等待时间
        :param proxies: 代理配置
        :param method: 请求方法： get；post
        :param url: url
        :param times: 次数，int
        :param retry_wait_time: 重试等待时间，毫秒
        :param wait_time: 等待时间：毫秒；表示每个请求的间隔时间，在请求之前等待sleep，主要用于防止请求太频繁的限制。
        :param kwargs: 其它 requests 参数，用法相同
        :return: res
        """
<<<<<<< HEAD
        # 0. 频率限制检查
        if url:
            rate_limit_wait = self._rate_limiter.acquire(url)
            if rate_limit_wait > 0:
                time.sleep(rate_limit_wait)

        # 1. 获取设置代理
=======
        # 1. 解析域名并检查频率限制
        domain = urllib.parse.urlparse(url).netloc
        self.rate_limiter.check_rate_limit(domain)
        
        # 2. 获取设置代理
>>>>>>> 9ce4090857c539647fe2ec3f5b989ac553be7b30
        proxies = self.__get_proxies(proxies)
        # 3. 请求数据结果
        res = None
        for i in range(times):
            if wait_time:
                time.sleep(wait_time / 1000)
            res = requests.request(method=method, url=url, proxies=proxies, **kwargs)
            if res.status_code in (200, 404):
                return res
            time.sleep(retry_wait_time / 1000)
            if i == times - 1:
                return res
        return res
    
    def set_rate_limit(self, domain, max_requests=30, time_window=60):
        """
        设置域名的频率限制
        :param domain: 域名
        :param max_requests: 最大请求次数，默认30次
        :param time_window: 时间窗口，默认60秒
        """
        self.rate_limiter.set_limit(domain, max_requests, time_window)

    def __get_proxies(self, proxies):
        """
        获取代理配置
        """
        if proxies is None:
            proxies = {}
        is_proxy = SunProxy.get('is_proxy')
        ip = SunProxy.get('ip')
        proxy_url = SunProxy.get('proxy_url')
        if not ip and is_proxy and proxy_url:
            ip = requests.get(url=proxy_url).text.replace('\r\n', '') \
                .replace('\r', '').replace('\n', '').replace('\t', '')
        if is_proxy and ip:
            proxies = {'https': f"http://{ip}", 'http': f"http://{ip}"}
        return proxies


sun_requests = SunRequests()
