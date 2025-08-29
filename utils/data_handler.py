import json
from pathlib import Path

import pandas as pd
import yaml
from faker import Faker

from utils.logger import logger


class DataHandler:
    """增强版数据处理工具类（适配JSON测试用例和Java后端）"""

    base_data_dir = Path("data")
    json_case_dir = base_data_dir / "json"

    def __init__(self):
        self.fake = Faker("zh_CN")
        DataHandler.base_data_dir.mkdir(exist_ok=True)
        DataHandler.json_case_dir.mkdir(exist_ok=True)

    @staticmethod
    def load_json_cases(module_name, filename):
        """
        从指定模块目录读取JSON测试用例（适配按模块组织的结构）
        :param module_name: 模块名（如"user_api"、"order_api"）
        :param filename: JSON文件名（如"test_create_user.json"）
        :return: 测试用例列表（单条用例自动转为列表）
        """
        module_dir = DataHandler.json_case_dir / module_name
        module_dir.mkdir(exist_ok=True)
        file_path = module_dir / filename

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                cases = json.load(f)
                return [cases] if isinstance(cases, dict) else cases
        except FileNotFoundError:
            logger.error(f"JSON用例文件不存在: {file_path}")
            return []
        except Exception as e:
            logger.error(f"读取JSON用例失败: {str(e)}")
            return []

    def _replace_single_value(self, value):
        """替换单个值中的占位符"""
        if not isinstance(value, str):
            return value

        # 支持的动态参数（可根据Java接口需求扩展）
        placeholder_map = {
            "${random_username}": f"user_{self.fake.random_int(1000, 9999)}",
            "${random_phone}": self.fake.phone_number(),
            "${random_email}": self.fake.email(),
            "${random_id}": self.fake.random_int(1, 10000),
            "${timestamp}": str(int(self.fake.date_time_this_year().timestamp()))
        }

        # 替换占位符
        for placeholder, replacement in placeholder_map.items():
            if value == placeholder:
                return replacement
        return value  # 无匹配占位符则返回原值

    def generate_fake_data(self, data_type, **kwargs):
        """生成虚假测试数据（如姓名、手机号等）"""
        try:
            if hasattr(self.fake, data_type):
                data_generator = getattr(self.fake, data_type)
                return data_generator(**kwargs)
            else:
                logger.warning(f"不支持的数据类型: {data_type}")
                return None
        except Exception as e:
            logger.error(f"生成虚假数据失败: {str(e)}")
            return None

    def read_json(self, filename):
        """读取根目录下的JSON文件（非测试用例的普通JSON数据）"""
        file_path = self.base_data_dir / filename
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"JSON文件不存在: {file_path}")
            return None
        except Exception as e:
            logger.error(f"读取JSON文件失败: {str(e)}")
            return None

    def write_json(self, data, filename):
        """写入JSON文件"""
        file_path = self.base_data_dir / filename
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"数据已写入JSON文件: {file_path}")
            return True
        except Exception as e:
            logger.error(f"写入JSON文件失败: {str(e)}")
            return False

    def read_yaml(self, filename):
        """读取YAML文件"""
        file_path = self.base_data_dir / filename
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"YAML文件不存在: {file_path}")
            return None
        except Exception as e:
            logger.error(f"读取YAML文件失败: {str(e)}")
            return None

    def read_csv(self, filename, **kwargs):
        """读取CSV文件"""
        file_path = self.base_data_dir / filename
        try:
            df = pd.read_csv(file_path, **kwargs)
            return df.to_dict("records")
        except FileNotFoundError:
            logger.error(f"CSV文件不存在: {file_path}")
            return None
        except Exception as e:
            logger.error(f"读取CSV文件失败: {str(e)}")
            return None

    def get_test_cases(self, filename):
        """获取根目录下的测试用例（兼容多种格式）"""
        if filename.endswith(".json"):
            return self.read_json(filename)
        elif filename.endswith((".yaml", ".yml")):
            return self.read_yaml(filename)
        elif filename.endswith(".csv"):
            return self.read_csv(filename)
        else:
            logger.error(f"不支持的测试用例文件格式: {filename}")
            return None


data_handler = DataHandler()
