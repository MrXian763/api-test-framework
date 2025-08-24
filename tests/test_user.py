import json
from utils.assertions import assertions
from utils.logger import logger
from utils.data_handler import data_handler


def test_post_user_login(user_api):
    """测试用户登录"""
    test_cases = data_handler.load_json_cases("user_api", "user_login_test_cases.json")

    success_case = test_cases[0]
    fail_case1 = test_cases[1]
    fail_case2 = test_cases[2]
    fail_case3 = test_cases[3]
    fail_case4 = test_cases[4]
    fail_case5 = test_cases[5]

    run_success_case(user_api, success_case)

    fail_cases = [fail_case1, fail_case2, fail_case3, fail_case4, fail_case5]
    for case in fail_cases:
        run_fail_case(user_api, case)


def run_success_case(user_api, case):
    """执行登录成功场景测试"""
    logger.info(f"执行测试用例: {case['case_id']} - {case['title']}")
    response = user_api.login(case["data"]["userAccount"], case["data"]["userPassword"])

    assertions.assert_response_code(response, case["expected_status"])
    assertions.assert_response_time(response, 1)

    json_data = response.json()
    logger.debug(f"接口返回数据: {json.dumps(json_data, ensure_ascii=False, indent=2)}")

    data_content = json_data.get("data", {})
    if not data_content:
        assertions.fail("响应中data字段为空或不存在")

    for field in case["expected_fields"]:
        if field not in data_content:
            assertions.fail(f"响应data缺少字段: {field}")
        logger.info(f"字段 {field} 存在性断言成功")


def run_fail_case(user_api, case):
    """执行登录失败场景测试"""
    logger.info(f"执行测试用例: {case['case_id']} - {case['title']}")
    response = user_api.login(case["data"]["userAccount"], case["data"]["userPassword"])

    assertions.assert_response_code(response, case["expected_status"])
    assertions.assert_response_time(response, 1)

    error_json = response.json()
    error_msg = error_json.get("message", "")
    assertions.assert_equal(error_msg, "请求参数错误", "错误信息不一致")
