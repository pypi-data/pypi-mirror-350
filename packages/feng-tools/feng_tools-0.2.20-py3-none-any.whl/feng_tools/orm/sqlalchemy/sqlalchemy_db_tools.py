from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from feng_tools.orm.sqlalchemy.sqlalchemy_settings import DatabaseSettings


class SqlalchemyDbTool:
    """db工具类"""

    def __init__(self, db_settings: DatabaseSettings):
        self.db_settings = db_settings

    def create_engine(self) -> Engine:
        """创建engine"""
        return create_engine(url=self.db_settings.url,
                             pool_size=self.db_settings.pool_size,
                             max_overflow=self.db_settings.max_overflow,
                             pool_timeout=self.db_settings.pool_timeout,
                             pool_recycle=self.db_settings.pool_recycle,
                             echo=self.db_settings.echo,
                             echo_pool=self.db_settings.echo_pool,
                             pool_pre_ping=self.db_settings.pool_pre_ping,
                             pool_use_lifo=self.db_settings.pool_use_lifo)

    def create_async_engine(self) -> AsyncEngine:
        """创建异步engine"""
        return create_async_engine(url=self.db_settings.async_url,
                             pool_size=self.db_settings.pool_size,
                             max_overflow=self.db_settings.max_overflow,
                             pool_timeout=self.db_settings.pool_timeout,
                             pool_recycle=self.db_settings.pool_recycle,
                             echo=self.db_settings.echo,
                             echo_pool=self.db_settings.echo_pool,
                             pool_pre_ping=self.db_settings.pool_pre_ping,
                             pool_use_lifo=self.db_settings.pool_use_lifo
        )