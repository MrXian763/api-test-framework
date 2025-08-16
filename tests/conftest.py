import pytest
from api.user_api import UserAPI
from utils.data_handler import data_handler
from utils.logger import logger

@pytest.fixture(scope="session")
def user_api():
    """用户API客户端fixture，会话级别"""
    api = UserAPI()
    logger.info("初始化用户API客户端")
    yield api
    api.close()
    logger.info("关闭用户API客户端")

@pytest.fixture(scope="module")
def authenticated_user_api(user_api):
    """已认证的用户API客户端fixture，模块级别"""
    # 使用测试账号登录
    username = "test_user"
    password = "test_password"
    
    response = user_api.login(username, password)
    assert response.status_code == 200, f"登录失败: {response.text}"
    
    yield user_api
    
    # 登出
    user_api.logout()

@pytest.fixture(params=data_handler.get_test_cases("user_test_cases.json"))
def user_test_case(request):
    """用户接口测试用例数据fixture，参数化"""
    return request.param

@pytest.fixture
def temp_user(authenticated_user_api):
    """创建临时用户fixture，自动清理"""
    # 创建用户
    user_data = {
        "name": data_handler.generate_fake_data("name"),
        "email": data_handler.generate_fake_data("email"),
        "username": data_handler.generate_fake_data("user_name")
    }
    
    response = authenticated_user_api.create_user(user_data)
    assert response.status_code == 201, f"创建用户失败: {response.text}"
    
    user_id = response.json().get("id")
    logger.info(f"创建临时用户: {user_id}")
    
    yield response.json()
    
    # 清理：删除用户
    if user_id:
        delete_response = authenticated_user_api.delete_user(user_id)
        if delete_response.status_code == 204:
            logger.info(f"已删除临时用户: {user_id}")
        else:
            logger.warning(f"删除临时用户{user_id}失败: {delete_response.text}")
