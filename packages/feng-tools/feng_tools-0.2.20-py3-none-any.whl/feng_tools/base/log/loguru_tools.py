"""
loguru工具：pip install loguru
"""
import os.path

from loguru import logger

from feng_tools.base.log import log_tools


class LoguruTools:
    def __init__(self, is_store=True,
                 log_dir:str='logs',
                 log_format:str = "[{time} {level}] - {file}:{line} - {message}",
                 info_level='INFO',info_file_name='info.log', info_rotation='50 MB',
                 error_level='WARNING',error_file_name='info.log',error_rotation='20 MB',):
        self.is_store=is_store
        self.log_dir = log_dir
        self.log_format = log_format
        self.info_level=info_level
        self.info_file_name = info_file_name
        self.info_rotation = info_rotation
        self.error_level=error_level
        self.error_file_name=error_file_name
        self.error_rotation=error_rotation
        self._logger = logger
        self._init_logger()

    def _init_logger(self):
        if self.is_store:
            info_file = os.path.join(self.log_dir, self.info_file_name)
            self._logger.add(info_file,
                             format=self.log_format,
                       rotation=self.info_rotation,
                       compression='zip',
                       encoding='utf-8', level=self.info_level)
            error_file = os.path.join(self.log_dir, self.error_file_name)
            self._logger.add(error_file,
                             format=self.log_format,
                             rotation=self.error_rotation,
                             compression='zip', encoding='utf-8',
                             level=self.error_level)


    def get_logger(self):
        return self._logger

    @staticmethod
    def get_error_msg(error_msg: str, exc: Exception = None):
        return log_tools.get_error_msg(error_msg, exc=exc)


if __name__ == '__main__':
    log_tools = LoguruTools(is_store=True, log_dir='./logs')
    logger = log_tools.get_logger()
    logger.info('测试啦')