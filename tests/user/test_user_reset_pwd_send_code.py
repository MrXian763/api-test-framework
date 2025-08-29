import pytest
from utils.assertions import Assertions
from utils.logger import logger
from utils.data_handler import DataHandler


def test_user_reset_pwd_send_code_success(unauthenticated_user_api):
    """测试重置密码发送验证码成功"""
    success_case = DataHandler.load_json_cases(
        "user_api", "user_reset_pwd_send_code.json")[0]
    logger.info(f"开始执行用例: {success_case['case_id']} - {success_case['title']}")

    resp = unauthenticated_user_api.reset_user_send_code(
        success_case["data"]["userAccount"])

    Assertions.assert_response_code(resp, success_case["expected_code"])
    Assertions.assert_response_time(resp, success_case["expected_resp_time"])


@pytest.mark.parametrize(
    "fail_case",
    DataHandler.load_json_cases(
        "user_api", "user_reset_pwd_send_code.json")[1:],
    ids=lambda case: f"fail_{case['case_id']}_{case['title'][:10]}"
)
def test_post_user_reset_pwd_send_code_fail(unauthenticated_user_api, fail_case):
    logger.info(f"开始执行用例: {fail_case['case_id']} - {fail_case['title']}")

    resp = unauthenticated_user_api.reset_user_send_code(
        fail_case["data"]["userAccount"])
    resp_json = resp.json()
    err_msg = resp_json.get("message")

    Assertions.assert_response_code(resp, fail_case["expected_code"])
    Assertions.assert_equal(err_msg, fail_case["expected_message"])
    Assertions.assert_response_time(resp, fail_case["expected_resp_time"])
