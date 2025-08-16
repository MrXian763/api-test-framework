import json
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils.logger import logger
from utils.config import config
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

class BaseAPI:
    """基础接口类，封装了请求方法和通用逻辑"""
    
    def __init__(self, base_url=None):
        """初始化API客户端"""
        self.base_url = base_url or config.get("api.base_url")
        self.session = self._create_session()
        self.headers = config.get("api.headers", {})
        self.timeout = config.get("api.timeout", 10)
        
        # 添加默认headers
        if self.headers:
            self.session.headers.update(self.headers)
        
        logger.info(f"初始化API客户端，基础URL: {self.base_url}")
    
    def _create_session(self):
        """创建带重试机制的会话"""
        session = requests.Session()
        
        # 配置重试策略
        retry_strategy = Retry(
            total=config.get("api.retry.total", 3),
            backoff_factor=config.get("api.retry.backoff_factor", 1),
            status_forcelist=config.get("api.retry.status_forcelist", [429, 500, 502, 503, 504])
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        return session
    
    @retry(
        stop=stop_after_attempt(config.get("api.retry.attempts", 2)),
        wait=wait_fixed(config.get("api.retry.wait_seconds", 1)),
        retry=retry_if_exception_type((requests.exceptions.ConnectionError, requests.exceptions.Timeout))
    )
    def _request(self, method, url, **kwargs):
        """
        发送HTTP请求的内部方法
        :param method: 请求方法
        :param url: 请求URL
        :param kwargs: 其他请求参数
        :return: 响应对象
        """
        # 拼接完整URL
        if not url.startswith(("http://", "https://")) and self.base_url:
            full_url = f"{self.base_url.rstrip('/')}/{url.lstrip('/')}"
        else:
            full_url = url
        
        # 设置超时
        kwargs.setdefault("timeout", self.timeout)
        
        # 记录请求信息
        logger.info(f"发送{method.upper()}请求: {full_url}")
        logger.debug(f"请求参数: {json.dumps(kwargs, ensure_ascii=False, indent=2)}")
        
        start_time = time.time()
        try:
            response = self.session.request(method, full_url,** kwargs)
            elapsed = time.time() - start_time
            
            # 记录响应信息
            logger.info(f"收到响应: {response.status_code}, 耗时: {elapsed:.3f}s")
            logger.debug(f"响应头: {json.dumps(dict(response.headers), ensure_ascii=False, indent=2)}")
            logger.debug(f"响应体: {response.text}")
            
            return response
        except Exception as e:
            logger.error(f"请求失败: {str(e)}")
            raise
    
    def get(self, url, params=None, **kwargs):
        """发送GET请求"""
        return self._request("get", url, params=params,** kwargs)
    
    def post(self, url, data=None, json=None, **kwargs):
        """发送POST请求"""
        return self._request("post", url, data=data, json=json,** kwargs)
    
    def put(self, url, data=None, json=None, **kwargs):
        """发送PUT请求"""
        return self._request("put", url, data=data, json=json,** kwargs)
    
    def delete(self, url, **kwargs):
        """发送DELETE请求"""
        return self._request("delete", url,** kwargs)
    
    def patch(self, url, data=None, **kwargs):
        """发送PATCH请求"""
        return self._request("patch", url, data=data,** kwargs)
    
    def set_headers(self, headers):
        """设置请求头"""
        if headers:
            self.session.headers.update(headers)
            logger.info(f"更新请求头: {headers}")
    
    def add_header(self, key, value):
        """添加单个请求头"""
        self.session.headers[key] = value
        logger.info(f"添加请求头: {key}={value}")
    
    def remove_header(self, key):
        """移除请求头"""
        if key in self.session.headers:
            del self.session.headers[key]
            logger.info(f"移除请求头: {key}")
    
    def close(self):
        """关闭会话"""
        self.session.close()
        logger.info("关闭API客户端会话")
