import pytest
from utils.data_handler import data_handler
from utils.logger import logger
from utils.assertions import assertions
import random
import time


def test_post_user_register_success(user_api):
    """注册成功场景"""
    test_cases = data_handler.load_json_cases("user_api", "user_register_test_cases.json")
    success_case = test_cases[0]

    logger.info(f"开始执行用例：{success_case['case_id']} - {success_case['title']}")
    response = user_api.register(success_case['data']["checkPassword"], generate_unique_account(),
                                 success_case['data']["userPassword"])

    assertions.assert_response_code(response, success_case['expected_code'])
    assertions.assert_response_time(response, 1)


@pytest.mark.parametrize(
    "fail_case",
    data_handler.load_json_cases("user_api", "user_register_test_cases.json")[1:],
    ids=lambda case: f"fail_{case['case_id']}_{case['title'][:10]}"
)
def test_post_user_register_fail(user_api, fail_case):
    """所有注册失败场景"""
    logger.info(f"开始执行用例：{fail_case['case_id']} - {fail_case['title']}")
    response = user_api.register(fail_case['data']["checkPassword"], fail_case['data']["userAccount"],
                                 fail_case['data']["userPassword"])
    resp_json = response.json()
    err_msg = resp_json.get("message", "")

    assertions.assert_response_code(response, fail_case['expected_code'])
    assertions.assert_equal(err_msg, fail_case['expected_message'])
    assertions.assert_response_time(response, 1)


def generate_unique_account():
    """生成随机账号，避免正向用例预期错误"""
    prefix = "test_"
    timestamp = str(int(time.time()))[-6:]
    random_num = random.randint(10, 99)
    account = f"{prefix}{timestamp}_{random_num}"
    return account


"""todo 根据用户名删除用户，避免测试数据污染"""
