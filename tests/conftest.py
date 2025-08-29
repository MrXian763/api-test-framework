import json

import pytest
from utils.config import config
from utils.logger import logger
from api.user_api import UserAPI


@pytest.fixture(scope="function")
def unauthenticated_user_api():
    """未认证的用户API客户端（每个测试用例全新实例）"""
    api_client = UserAPI()
    logger.info("初始化未认证的用户API客户端")
    yield api_client
    logger.info("关闭用户API客户端")


@pytest.fixture(scope="function")
def authenticated_user_api():
    """已认证的用户API客户端fixture（通用断言版）"""
    api_client = UserAPI()
    admin_username = config.get("test.user.admin.userAccount")
    admin_password = config.get("test.user.admin.userPassword")
    if not all([admin_username, admin_password]):
        pytest.fail("配置文件中未设置管理员账号（test.user.admin）")

    response = api_client.login(admin_username, admin_password)
    assert response.json().get("code") == 0, f"登录失败（HTTP状态码异常）: {response.text}"

    try:
        resp_json = response.json()
        token = resp_json.get("token") or resp_json.get("data", {}).get("token")
        assert token, "登录响应中未找到token"
        # api_client.add_header("Authorization", f"Bearer {token}")
        api_client.add_header("Authorization", token)
        logger.info("管理员登录成功，已绑定token")
    except json.JSONDecodeError:
        pytest.fail(f"登录响应不是JSON格式: {response.text}")

    yield api_client

    try:
        logout_resp = api_client.logout()
        assert logout_resp.status_code in [200, 204], f"登出失败: {logout_resp.text}"
        logger.info("管理员已登出")
    except Exception as e:
        logger.warning(f"登出异常: {str(e)}")
