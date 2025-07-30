"""
logging工具
"""
import logging
import os
from pathlib import Path

from feng_tools.base.log import log_tools


class LoggingTools:
    def __init__(self, is_store: bool = True,
                 log_dir:str='logs',
                 log_format:str='[%(asctime)s %(levelname)s] - %(filename)s:%(lineno)d - %(message)s',
                 info_file_name='info.log', info_rotation='50 MB',
                 error_file_name='info.log',error_rotation='20 MB',):
        self.is_store = is_store
        self.log_dir = log_dir
        self.log_format=log_format
        self.formatter = logging.Formatter(self.log_format)
        self.info_file_name = info_file_name
        self.info_rotation = info_rotation
        self.error_file_name=error_file_name
        self.error_rotation=error_rotation

    def create_stream_handler(self, level=logging.INFO):
        handler = logging.StreamHandler()
        handler.setLevel(level)
        handler.setFormatter(self.formatter )
        return handler
    def create_file_handler(self, level=logging.INFO):
        info_file = os.path.join(self.log_dir, self.info_file_name)
        os.makedirs(Path(info_file).parent, exist_ok=True)
        handler = logging.FileHandler(info_file, mode='a', encoding='utf-8')
        handler.setLevel(level)
        handler.setFormatter(self.formatter)
        return handler
    def get_logger(self, logger_name:str=None,
                   level=logging.INFO):
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        logger.addHandler(self.create_stream_handler(level=level))
        if self.is_store:
            logger.addHandler(self.create_file_handler(level))
        return logger

    @staticmethod
    def get_error_msg(error_msg: str, exc: Exception = None):
        return log_tools.get_error_msg(error_msg, exc=exc)


if __name__ == '__main__':
    logging_tools = LoggingTools(is_store=True, log_dir='./logs')
    logger = logging_tools.get_logger(__file__, level=logging.DEBUG)
    logger.info('测试啦')