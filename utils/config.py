import os
import yaml
from dotenv import load_dotenv
from pathlib import Path
from utils.logger import logger

class Config:
    """配置管理类"""
    def __init__(self):
        self._config = {}
        self._load_env()
        self._load_config()
    
    def _load_env(self):
        """加载环境变量"""
        env_path = Path(".") / ".env"
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            logger.info("已加载.env文件中的环境变量")
    
    def _load_config(self):
        """加载配置文件"""
        env = os.getenv("TEST_ENV", "test")
        config_path = Path("config") / f"{env}.yaml"
        
        if not config_path.exists():
            logger.warning(f"未找到{env}环境的配置文件，使用默认配置")
            config_path = Path("config") / "default.yaml"
        
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self._config = yaml.safe_load(f) or {}
                logger.info(f"已加载{env}环境的配置文件: {config_path}")
        except Exception as e:
            logger.error(f"加载配置文件失败: {str(e)}")
            self._config = {}
    
    def get(self, key, default=None, separator="."):
        """
        获取配置值
        :param key: 配置键，支持嵌套键，如"api.base_url"
        :param default: 默认值
        :param separator: 分隔符
        :return: 配置值
        """
        keys = key.split(separator)
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def __getitem__(self, key):
        """支持字典式访问"""
        return self.get(key)
    
    def __contains__(self, key):
        """检查配置是否包含某个键"""
        return self.get(key, default=None) is not None

# 单例配置对象
config = Config()
