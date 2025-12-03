import logging
from pathlib import Path
from datetime import datetime


class Logger:
    """日志工具类,用于记录测试执行过程"""

    _initialized = False

    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # 避免重复添加handler
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self):
        """配置日志处理器"""
        # 创建logs目录
        log_dir = Path(__file__).parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)

        # 文件handler - 记录所有日志
        log_file = log_dir / f"test_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # 控制台handler - 只显示INFO及以上
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message: str):
        """调试信息"""
        self.logger.debug(message)

    def info(self, message: str):
        """一般信息"""
        self.logger.info(message)

    def warning(self, message: str):
        """警告信息"""
        self.logger.warning(message)

    def error(self, message: str):
        """错误信息"""
        self.logger.error(message)

    @classmethod
    def get_logger(cls, name: str = "TestLogger"):
        """获取日志实例(类方法,方便直接调用)"""
        return cls(name)
