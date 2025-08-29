import pytest
from utils.data_handler import data_handler
from utils.logger import logger
from utils.assertions import assertions


def test_get_current_user_success(authenticated_user_api):
    """获取当前登录用户（正向）"""
    test_cases = data_handler.load_json_cases("user_api", "user_get_current_test_cases.json")
    success_case = test_cases[0]
    logger.info(f"执行测试用例: {success_case['case_id']} - {success_case['title']}")
    resp = authenticated_user_api.get_current_user()
    resp_json = resp.json()
    data_content = resp_json.get("data")

    if not data_content:
        assertions.fail("响应总data字段为空或不存在")

    assertions.assert_response_code(resp, success_case.get("expected_code"))
    assertions.assert_response_time(resp, success_case.get("expected_resp_time"))

    for field in success_case["expected_fields"]:
        if field not in data_content:
            assertions.fail(f"响应data缺少字段: {field}")
