import json
import jmespath
from jsonschema import validate, ValidationError
from utils.logger import logger


class Assertions:
    """断言工具类"""

    @staticmethod
    def assert_equal(actual, expected, message="值不相等"):
        """断言相等"""
        try:
            assert actual == expected, f"{message} - 实际值: {actual}, 预期值: {expected}"
            logger.info(f"断言成功: {actual} == {expected}")
        except AssertionError as e:
            logger.error(f"断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_not_equal(actual, expected, message="值相等"):
        """断言不相等"""
        try:
            assert actual != expected, f"{message} - 实际值: {actual}, 预期值: {expected}"
            logger.info(f"断言成功: {actual} != {expected}")
        except AssertionError as e:
            logger.error(f"断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_in(actual, expected, message="实际值不在预期列表中"):
        """断言包含"""
        try:
            assert actual in expected, f"{message} - 实际值: {actual}, 预期列表: {expected}"
            logger.info(f"断言成功: {actual} 在 {expected} 中")
        except AssertionError as e:
            logger.error(f"断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_not_in(actual, expected, message="实际值在预期列表中"):
        """断言不包含"""
        try:
            assert actual not in expected, f"{message} - 实际值: {actual}, 预期列表: {expected}"
            logger.info(f"断言成功: {actual} 不在 {expected} 中")
        except AssertionError as e:
            logger.error(f"断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_true(condition, message="条件为假"):
        """断言为真"""
        try:
            assert condition, message
            logger.info(f"断言成功: {message}")
        except AssertionError as e:
            logger.error(f"断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_false(condition, message="条件为真"):
        """断言为假"""
        try:
            assert not condition, message
            logger.info(f"断言成功: {message}")
        except AssertionError as e:
            logger.error(f"断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_response_code(response, expected_code=0):
        """断言响应状态码"""
        try:
            status_code = response.json().get("code")
            assert status_code == expected_code, \
                f"响应状态码不正确 - 实际: {status_code}, 预期: {expected_code}"
            logger.info(f"响应状态码断言成功: {status_code} == {expected_code}")
        except AssertionError as e:
            logger.error(f"响应状态码断言失败: {str(e)}")
            logger.error(f"响应内容: {response.text}")
            raise

    @staticmethod
    def assert_response_time(response, max_time=1):
        """断言响应时间"""
        elapsed = response.elapsed.total_seconds()
        try:
            assert elapsed <= max_time, \
                f"响应时间过长 - 实际: {elapsed:.2f}s, 最大允许: {max_time}s"
            logger.info(f"响应时间断言成功: {elapsed:.2f}s <= {max_time}s")
        except AssertionError as e:
            logger.error(f"响应时间断言失败: {str(e)}")
            raise

    @staticmethod
    def assert_json_path(response, json_path, expected_value=None):
        """
        断言JSON响应中指定路径的值
        :param response: 响应对象
        :param json_path: JMESPath表达式
        :param expected_value: 预期值，为None时仅检查路径存在
        """
        try:
            json_data = response.json()
            actual_value = jmespath.search(json_path, json_data)

            if actual_value is None:
                raise AssertionError(f"JSON路径不存在: {json_path}")

            if expected_value is not None:
                assert actual_value == expected_value, \
                    f"JSON路径值不匹配 - 路径: {json_path}, 实际: {actual_value}, 预期: {expected_value}"

            logger.info(f"JSON路径断言成功: {json_path} = {actual_value}")
            return actual_value
        except json.JSONDecodeError:
            logger.error("响应不是有效的JSON")
            raise
        except AssertionError as e:
            logger.error(f"JSON路径断言失败: {str(e)}")
            logger.error(f"响应内容: {response.text}")
            raise
        except Exception as e:
            logger.error(f"断言JSON路径时发生错误: {str(e)}")
            raise

    @staticmethod
    def assert_json_schema(response, schema):
        """断言JSON响应符合指定的JSON Schema"""
        try:
            json_data = response.json()
            validate(instance=json_data, schema=schema)
            logger.info("JSON Schema断言成功")
        except json.JSONDecodeError:
            logger.error("响应不是有效的JSON")
            raise
        except ValidationError as e:
            logger.error(f"JSON Schema断言失败: {str(e)}")
            logger.error(f"响应内容: {response.text}")
            raise
        except Exception as e:
            logger.error(f"断言JSON Schema时发生错误: {str(e)}")
            raise


# 实例化断言工具
assertions = Assertions()
