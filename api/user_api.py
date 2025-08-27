from api.base_api import BaseAPI
from utils.logger import logger


class UserAPI(BaseAPI):
    """用户相关接口封装"""

    def __init__(self):
        super().__init__()
        self.base_path = "/user"

    def login(self, userAccount, userPassword):
        """用户登录"""
        url = "/user/login"
        data = {"userAccount": userAccount, "userPassword": userPassword}
        response = self.post(url, json=data)
        if response.json().get("code") == 200:
            response_json = response.json()
            data_content = response_json.get("data")
            if data_content is not None:
                token = data_content.get("token")
                if token:
                    self.add_header("Authorization", token)
                    logger.info("登录成功，已设置Authorization头")
            else:
                error_msg = response_json.get("message", "未知错误")
                logger.warning(f"登录业务失败: {error_msg}")

        return response

    def logout(self):
        """用户登出（增强错误处理）"""
        current_token = self.session.headers.get("Authorization")
        logger.info(f"登出请求携带的token: {current_token}")

        url = f"{self.base_path}/logout"
        try:
            response = self.post(url)
            logger.info(f"登出响应状态码: {response.status_code}")
            self.remove_header("Authorization")
            logger.info("已登出，清除Authorization头")
            return response

        except Exception as e:
            logger.error(f"登出过程发生错误: {str(e)}")
            self.remove_header("Authorization")
            return None

    def register(self, checkPassword, userAccount, userPassword):
        """用户注册"""
        url = f"{self.base_path}/register"
        data = {"checkPassword": checkPassword, "userAccount": userAccount, "userPassword": userPassword}
        resp = self.post(url, json=data)
        return resp
