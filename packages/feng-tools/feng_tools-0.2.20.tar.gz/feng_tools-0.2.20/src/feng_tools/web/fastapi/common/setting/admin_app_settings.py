from typing import Optional

from pydantic_settings import BaseSettings
from sqlalchemy import Engine

from feng_tools.web.fastapi.common.page.admin_app_page import AdminAppPage
from feng_tools.web.fastapi.common.handler.file_handler import FileHandler
from feng_tools.orm.sqlalchemy.sqlalchemy_settings import DatabaseSettings


class AdminAppSettings(BaseSettings):
    # 管理应用的前缀
    prefix: Optional[str] = '/admin'
    # 数据库引擎（如果不配置该项，则需要配置database_setting）
    db_engine: Optional[Engine] = None
    # 数据库设置(如果设置了db_engine，就不用配置该项)
    database_setting: Optional[DatabaseSettings] = None
    # 管理应用的主体（用于生成app的主体页面）
    admin_app_page:AdminAppPage
    # 文件上传和下载处理类
    file_handler: FileHandler



