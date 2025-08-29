import pytest
from utils.data_handler import data_handler
from utils.logger import logger
from utils.assertions import assertions


def test_user_reset_pwd_success(authenticated_user_api):
    """测试用户重置密码成功用例"""
    test_cases = data_handler.load_json_cases(
        "user_api", "user_reset_pwd_test_cases.json")
    success_case = test_cases[0]
    logger.info(f"执行测试用例：{success_case['case_id']} - {success_case['title']}")
    resp = authenticated_user_api.reset_user_pwd(success_case['data']["oldPassword"],
                                                 success_case['data']["newPassword"],
                                                 success_case['data']["confirmPassword"])

    resp_json = resp.json()
    assertions.assert_response_code(resp, success_case.get("expected_code"))
    assertions.assert_response_time(
        resp, success_case.get("expected_resp_time"))
    assertions.assert_true(resp_json.get('data'))

    logger.info("成功用例执行完毕，开始恢复初始密码")
    try:
        recover_resp = authenticated_user_api.reset_user_pwd(
            oldPassword=success_case['data']["newPassword"],
            newPassword=success_case['data']["oldPassword"],
            confirmPassword=success_case['data']["oldPassword"]
        )
        if recover_resp.json().get("code") == 0:
            logger.info("密码已成功恢复为初始值")
        else:
            logger.warning("密码恢复失败，可能影响后续测试")
    except Exception as e:
        logger.error(f"恢复密码过程发生错误: {str(e)}")


@pytest.mark.parametrize(
    "fail_case",
    data_handler.load_json_cases(
        "user_api", "user_reset_pwd_test_cases.json")[1:],
    ids=lambda case: f"test_{case['case_id']}_{case['title'][:10]}"
)
def test_user_reset_pwd_fail(authenticated_user_api, fail_case):
    """测试用户重置密码失败用例"""
    logger.info(f"执行测试用例：{fail_case['case_id']} - {fail_case['title']}")
    resp = authenticated_user_api.reset_user_pwd(fail_case['data']["oldPassword"],
                                                 fail_case['data']["newPassword"],
                                                 fail_case['data']["confirmPassword"])
    resp_json = resp.json()

    assertions.assert_response_code(resp, fail_case.get("expected_code"))
    assertions.assert_response_time(resp, fail_case.get("expected_resp_time"))
    
