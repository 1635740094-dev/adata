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
import urllib.parse

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


class SunRequests(object):
    def __init__(self, sun_proxy: SunProxy = None) -> None:
        super().__init__()
        self.sun_proxy = sun_proxy
        self.rate_limiter = RateLimiter()

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
        # 1. 解析域名并检查频率限制
        domain = urllib.parse.urlparse(url).netloc
        self.rate_limiter.check_rate_limit(domain)
        
        # 2. 获取设置代理
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
