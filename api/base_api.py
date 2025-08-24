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

    def _log_request_details(self, method, full_url, kwargs):
        """详细记录请求信息"""
        # 构建请求详情字典
        request_details = {
            "method": method.upper(),
            "url": full_url,
            "timeout": kwargs.get("timeout", self.timeout)
        }

        # 添加请求参数（避免敏感信息）
        if "params" in kwargs:
            request_details["params"] = kwargs["params"]
        if "headers" in kwargs:
            request_details["headers"] = kwargs["headers"]

        # 处理请求体（敏感信息过滤）
        if "json" in kwargs:
            request_body = kwargs["json"].copy()
            # 过滤密码等敏感信息
            if "password" in request_body:
                request_body["password"] = "***"
            if "userPassword" in request_body:
                request_body["userPassword"] = "***"
            request_details["json"] = request_body

        if "data" in kwargs:
            request_details["data"] = "表单数据存在" if kwargs["data"] else None

        logger.debug(f"请求详情: {json.dumps(request_details, ensure_ascii=False, indent=2)}")

    def _log_response_details(self, response, elapsed):
        """安全记录响应信息，处理无响应体情况"""
        # 基础响应信息
        logger.info(f"收到响应: {response.status_code}, 耗时: {elapsed:.3f}s")

        # 记录响应头
        try:
            logger.debug(f"响应头: {json.dumps(dict(response.headers), ensure_ascii=False, indent=2)}")
        except Exception as e:
            logger.warning(f"记录响应头失败: {str(e)}")

        try:
            if not response.content:
                logger.debug("响应体: 空响应体")
                return

            response_json = response.json()
            logger.debug(f"响应体(JSON): {json.dumps(response_json, ensure_ascii=False, indent=2)}")

        except json.JSONDecodeError:
            try:
                text_content = response.text
                max_length = 1000
                if len(text_content) > max_length:
                    text_content = text_content[:max_length] + f"...(省略剩余{len(text_content) - max_length}字符)"
                logger.debug(f"响应体(文本): {text_content}")
            except Exception as e:
                logger.warning(f"记录文本响应体失败: {str(e)}")

        except Exception as e:
            logger.warning(f"处理响应体时发生异常: {str(e)}")

    @retry(
        stop=stop_after_attempt(config.get("api.retry.attempts", 2)),
        wait=wait_fixed(config.get("api.retry.wait_seconds", 1)),
        retry=retry_if_exception_type((requests.exceptions.ConnectionError, requests.exceptions.Timeout))
    )
    def _request(self, method, url, **kwargs):
        # 拼接完整URL（不变）
        if not url.startswith(("http://", "https://")) and self.base_url:
            full_url = f"{self.base_url.rstrip('/')}/{url.lstrip('/')}"
        else:
            full_url = url

        session_headers = dict(self.session.headers)

        if "headers" not in kwargs:
            # 使用字典构造函数代替copy()
            kwargs["headers"] = dict(session_headers)
        else:
            # 确保传入的headers是字典
            if kwargs["headers"] is None:
                kwargs["headers"] = {}
            else:
                # 合并headers，使用字典构造函数避免copy()
                merged_headers = dict(session_headers)
                merged_headers.update(kwargs["headers"])
                kwargs["headers"] = merged_headers

        kwargs.setdefault("timeout", self.timeout)

        logger.info(f"发送{method.upper()}请求: {full_url}")
        self._log_request_details(method, full_url, kwargs)

        start_time = time.time()
        try:
            response = self.session.request(method, full_url, **kwargs)
            elapsed = time.time() - start_time
            self._log_response_details(response, elapsed)
            return response
        except Exception as e:
            logger.error(f"请求失败: {str(e)}", exc_info=True)
            raise

    def get(self, url, params=None, **kwargs):
        """发送GET请求"""
        return self._request("get", url, params=params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """发送POST请求"""
        return self._request("post", url, data=data, json=json, **kwargs)

    def put(self, url, data=None, json=None, **kwargs):
        """发送PUT请求"""
        return self._request("put", url, data=data, json=json, **kwargs)

    def delete(self, url, **kwargs):
        """发送DELETE请求"""
        return self._request("delete", url, **kwargs)

    def patch(self, url, data=None, **kwargs):
        """发送PATCH请求"""
        return self._request("patch", url, data=data, **kwargs)

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
