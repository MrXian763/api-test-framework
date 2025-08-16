import pytest
from utils.assertions import assertions
from utils.logger import logger

@pytest.mark.smoke
@pytest.mark.high
def test_get_user_list(authenticated_user_api):
    """测试获取用户列表"""
    response = authenticated_user_api.get_user_list()
    
    # 断言状态码
    assertions.assert_response_code(response, 200)
    
    # 断言响应时间
    assertions.assert_response_time(response, 1)
    
    # 断言响应结构
    json_data = response.json()
    assertions.assert_true(isinstance(json_data, dict), "响应不是JSON对象")
    assertions.assert_true("data" in json_data, "响应中不包含data字段")
    assertions.assert_true(isinstance(json_data["data"], list), "data字段不是数组")
    
    # 断言分页信息
    assertions.assert_json_path(response, "page", 1)
    assertions.assert_json_path(response, "per_page", 10)

@pytest.mark.regression
@pytest.mark.medium
def test_create_and_get_user(authenticated_user_api, temp_user):
    """测试创建用户并查询用户信息"""
    # temp_user是通过fixture创建的临时用户
    user_id = temp_user["id"]
    user_name = temp_user["name"]
    
    # 查询刚创建的用户
    response = authenticated_user_api.get_user(user_id)
    
    # 断言
    assertions.assert_response_code(response, 200)
    assertions.assert_json_path(response, "id", user_id)
    assertions.assert_json_path(response, "name", user_name)

@pytest.mark.regression
@pytest.mark.medium
def test_update_user(authenticated_user_api, temp_user):
    """测试更新用户信息"""
    user_id = temp_user["id"]
    
    # 准备更新数据
    new_name = "Updated Name"
    update_data = {"name": new_name}
    
    # 更新用户
    response = authenticated_user_api.update_user(user_id, update_data)
    assertions.assert_response_code(response, 200)
    
    # 验证更新结果
    get_response = authenticated_user_api.get_user(user_id)
    assertions.assert_json_path(get_response, "name", new_name)

@pytest.mark.parametrize("page, per_page", [
    (1, 10),
    (2, 20),
    (3, 5)
])
def test_user_list_pagination(authenticated_user_api, page, per_page):
    """测试用户列表分页功能"""
    response = authenticated_user_api.get_user_list(page=page, per_page=per_page)
    
    assertions.assert_response_code(response, 200)
    assertions.assert_json_path(response, "page", page)
    assertions.assert_json_path(response, "per_page", per_page)
    
    # 检查返回的数量不超过per_page
    data = response.json().get("data", [])
    assertions.assert_true(len(data) <= per_page, "返回数量超过每页限制")

def test_invalid_user_id(authenticated_user_api):
    """测试查询不存在的用户ID"""
    invalid_user_id = 999999
    response = authenticated_user_api.get_user(invalid_user_id)
    
    # 断言404错误
    assertions.assert_response_code(response, 404)
    assertions.assert_json_path(response, "error", "User not found")
