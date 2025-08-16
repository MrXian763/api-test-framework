import os
import logging
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from colorlog import ColoredFormatter

# 确保日志目录存在
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

class Logger:
    """日志工具类"""
    def __init__(self):
        self.logger = logging.getLogger("api_test")
        self.logger.setLevel(logging.DEBUG)
        
        # 避免重复添加处理器
        if self.logger.handlers:
            return
        
        # 格式化器
        formatter = ColoredFormatter(
            "%(log_color)s%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # 文件处理器 (按天轮转)
        file_handler = TimedRotatingFileHandler(
            LOG_DIR / "api_test.log",
            when="D",
            interval=1,
            backupCount=7,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s:%(lineno)d - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        ))
        
        # 添加处理器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def get_logger(self):
        """获取logger实例"""
        return self.logger

# 单例日志对象
logger = Logger().get_logger()
