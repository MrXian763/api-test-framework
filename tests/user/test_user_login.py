import json
import pytest
from utils.assertions import assertions
from utils.logger import logger
from utils.data_handler import data_handler


def test_post_user_login_success(unauthenticated_user_api):
    """登录成功场景"""
    test_cases = data_handler.load_json_cases("user_api", "user_login_test_cases.json")
    success_case = test_cases[0]

    logger.info(f"执行测试用例: {success_case['case_id']} - {success_case['title']}")
    response = unauthenticated_user_api.login(
        success_case["data"]["userAccount"],
        success_case["data"]["userPassword"]
    )

    assertions.assert_response_code(response, success_case["expected_code"])
    assertions.assert_response_time(response, 1)

    json_data = response.json()
    logger.debug(f"接口返回数据: {json.dumps(json_data, ensure_ascii=False, indent=2)}")

    data_content = json_data.get("data", {})
    if not data_content:
        assertions.fail("响应中data字段为空或不存在")

    for field in success_case["expected_fields"]:
        if field not in data_content:
            assertions.fail(f"响应data缺少字段: {field}")
        logger.info(f"字段 {field} 存在性断言成功")


@pytest.mark.parametrize(
    "fail_case",
    data_handler.load_json_cases("user_api", "user_login_test_cases.json")[1:],
    ids=lambda case: f"fail_{case['case_id']}_{case['title'][:10]}"
)
def test_post_user_login_fail(unauthenticated_user_api, fail_case):
    """所有登录失败场景"""
    logger.info(f"执行测试用例: {fail_case['case_id']} - {fail_case['title']}")
    response = unauthenticated_user_api.login(
        fail_case["data"]["userAccount"],
        fail_case["data"]["userPassword"]
    )

    error_json = response.json()
    error_msg = error_json.get("message", "")

    assertions.assert_response_code(response, fail_case["expected_code"])
    assertions.assert_equal(error_msg, fail_case['expected_message'])
    assertions.assert_response_time(response, 1)
