from api.base_api import BaseAPI
from utils.logger import logger

class UserAPI(BaseAPI):
    """用户相关接口封装"""
    
    def __init__(self):
        super().__init__()
        self.base_path = "/users"
    
    def get_user_list(self, page=1, per_page=10):
        """获取用户列表"""
        url = self.base_path
        params = {"page": page, "per_page": per_page}
        return self.get(url, params=params)
    
    def get_user(self, user_id):
        """获取单个用户信息"""
        url = f"{self.base_path}/{user_id}"
        return self.get(url)
    
    def create_user(self, user_data):
        """创建用户"""
        url = self.base_path
        return self.post(url, json=user_data)
    
    def update_user(self, user_id, user_data):
        """更新用户信息"""
        url = f"{self.base_path}/{user_id}"
        return self.put(url, json=user_data)
    
    def delete_user(self, user_id):
        """删除用户"""
        url = f"{self.base_path}/{user_id}"
        return self.delete(url)
    
    def login(self, username, password):
        """用户登录"""
        url = "/auth/login"
        data = {"username": username, "password": password}
        response = self.post(url, json=data)
        
        # 如果登录成功，保存token
        if response.status_code == 200:
            token = response.json().get("token")
            if token:
                self.add_header("Authorization", f"Bearer {token}")
                logger.info("登录成功，已设置Authorization头")
        
        return response
    
    def logout(self):
        """用户登出"""
        url = "/auth/logout"
        response = self.post(url)
        
        # 清除token
        self.remove_header("Authorization")
        logger.info("已登出，清除Authorization头")
        
        return response
