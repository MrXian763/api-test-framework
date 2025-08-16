import os
import json
import yaml
import pandas as pd
from faker import Faker
from pathlib import Path
from utils.logger import logger

class DataHandler:
    """数据处理工具类"""
    def __init__(self):
        self.fake = Faker("zh_CN")  # 初始化Faker，使用中文数据
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)
    
    def generate_fake_data(self, data_type, **kwargs):
        """
        生成虚假测试数据
        :param data_type: 数据类型，如"name", "phone_number", "email"等
        :param kwargs: 其他参数
        :return: 生成的虚假数据
        """
        try:
            if hasattr(self.fake, data_type):
                data_generator = getattr(self.fake, data_type)
                return data_generator(** kwargs)
            else:
                logger.warning(f"不支持的数据类型: {data_type}")
                return None
        except Exception as e:
            logger.error(f"生成虚假数据失败: {str(e)}")
            return None
    
    def read_json(self, filename):
        """读取JSON文件"""
        file_path = self.data_dir / filename
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
        file_path = self.data_dir / filename
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
        file_path = self.data_dir / filename
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
        file_path = self.data_dir / filename
        try:
            df = pd.read_csv(file_path,** kwargs)
            return df.to_dict("records")
        except FileNotFoundError:
            logger.error(f"CSV文件不存在: {file_path}")
            return None
        except Exception as e:
            logger.error(f"读取CSV文件失败: {str(e)}")
            return None
    
    def get_test_cases(self, filename):
        """获取测试用例数据"""
        if filename.endswith(".json"):
            return self.read_json(filename)
        elif filename.endswith(".yaml") or filename.endswith(".yml"):
            return self.read_yaml(filename)
        elif filename.endswith(".csv"):
            return self.read_csv(filename)
        else:
            logger.error(f"不支持的测试用例文件格式: {filename}")
            return None

# 实例化数据处理器
data_handler = DataHandler()
