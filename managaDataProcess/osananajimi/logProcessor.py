import logging
import os
from datetime import datetime


class LogProcessor:
    def __init__(self,
                 log_name="app.log",
                 encoding="utf-8",
                 log_level=logging.INFO,
                 log_format=None,
                 date_format=None):
        """
        初始化日志处理器

        Args:
            log_name (str): 日志文件名
            encoding (str): 文件编码格式，默认为utf-8
            log_level: 日志级别，默认为INFO
            log_format (str): 日志格式
            date_format (str): 日期格式
        """
        self.log_name = log_name
        self.encoding = encoding
        self.log_level = log_level

        # 设置默认日志格式
        if log_format is None:
            self.log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        else:
            self.log_format = log_format

        # 设置默认日期格式
        if date_format is None:
            self.date_format = '%Y-%m-%d %H:%M:%S'
        else:
            self.date_format = date_format

        # 创建日志目录（如果不存在）
        log_dir = os.path.dirname(self.log_name)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        self._setup_logger()

    def _setup_logger(self):
        """设置日志配置"""
        # 创建logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.log_level)

        # 避免重复添加handler
        if self.logger.handlers:
            for handler in self.logger.handlers:
                self.logger.removeHandler(handler)

        # 创建文件handler，指定编码格式
        file_handler = logging.FileHandler(
            self.log_name,
            encoding=self.encoding,
            mode='a'  # 追加模式
        )
        file_handler.setLevel(self.log_level)

        # 创建控制台handler（可选）
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)

        # 创建formatter
        formatter = logging.Formatter(
            self.log_format,
            datefmt=self.date_format
        )

        # 设置handler的formatter
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加handler到logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def info(self, message):
        """记录INFO级别日志"""
        self.logger.info(message)

    def debug(self, message):
        """记录DEBUG级别日志"""
        self.logger.debug(message)

    def warning(self, message):
        """记录WARNING级别日志"""
        self.logger.warning(message)

    def exception(self, message):
        """记录EXCEPTION级别日志"""
        self.logger.exception(message)

    def error(self, message):
        """记录ERROR级别日志"""
        self.logger.error(message)

    def critical(self, message):
        """记录CRITICAL级别日志"""
        self.logger.critical(message)

    def update_logger(self, **kwargs):
        """动态更新日志配置"""
        if 'log_name' in kwargs:
            self.log_name = kwargs['log_name']
        if 'encoding' in kwargs:
            self.encoding = kwargs['encoding']
        if 'log_level' in kwargs:
            self.log_level = kwargs['log_level']
        if 'log_format' in kwargs:
            self.log_format = kwargs['log_format']
        if 'date_format' in kwargs:
            self.date_format = kwargs['date_format']

        # 重新设置logger
        self._setup_logger()


# 使用示例
if __name__ == "__main__":
    # 创建日志处理器
    log_processor = LogProcessor(
        log_name="my_app.log",
        encoding="utf-8",
        log_level=logging.INFO
    )

    # 记录日志（包含中文）
    log_processor.info("这是一条中文日志信息")
    log_processor.debug("调试信息")
    log_processor.warning("警告信息")
    log_processor.error("错误信息：文件未找到")

    # 测试包含特殊字符的中文
    log_processor.info("特殊字符测试：中文🌍表情符号")

    # 动态更新配置
    log_processor.update_logger(
        log_name="new_app.log",
        encoding="gbk"  # 如果需要可以改为其他编码
    )
    log_processor.info("更新配置后的日志")
