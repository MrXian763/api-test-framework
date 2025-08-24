import yaml
from pathlib import Path
from utils.logger import logger


class Config:
    def __init__(self, env="test"):
        self.env = env
        # 配置文件路径（必须与实际文件位置一致）
        self.default_config = Path("config") / "default.yaml"
        self.env_config = Path("config") / f"{env}.yaml"
        self.data = self._load()

    def _load(self):
        if self.env_config.exists():
            with open(self.env_config, "r", encoding="utf-8") as f:
                logger.info(f"加载环境配置: {self.env_config}")
                return yaml.safe_load(f)
        elif self.default_config.exists():
            with open(self.default_config, "r", encoding="utf-8") as f:
                logger.info(f"加载默认配置: {self.default_config}")
                return yaml.safe_load(f)
        else:
            logger.error(f"配置文件不存在: {self.default_config}")
            return {}

    def get(self, key, default=None):
        keys = key.split(".")
        value = self.data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value


config = Config()
