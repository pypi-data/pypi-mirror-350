from typing import Any, Generator

from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker, Session

from feng_tools.orm.sqlalchemy.sqlalchemy_settings import DbSessionSettings


class SqlalchemySessionTool:
    """Session类"""

    def __init__(self, engine: Engine,
                 async_engine: AsyncEngine=None,
                 session_settings:DbSessionSettings=None):
        self.engine = engine
        self.async_engine=async_engine
        if session_settings is None:
            session_settings=DbSessionSettings()
        self.session_settings=session_settings
        self._create_session_maker()


    def _create_session_maker(self):
        """Session创建者"""
        self.session_maker = sessionmaker(bind=self.engine,
                                          autocommit=self.session_settings.auto_commit,
                                          autoflush=self.session_settings.auto_flush,
                                          expire_on_commit=self.session_settings.expire_on_commit)
        if self.async_engine:
            self.async_session_maker = sessionmaker(bind=self.async_engine,
                                              class_=AsyncSession,
                                              autocommit=self.session_settings.auto_commit,
                                              autoflush=self.session_settings.auto_flush,
                                              expire_on_commit=self.session_settings.expire_on_commit,
                                              future=True)
    def get_Session(self):
        """获取Session"""
        return self.session_maker

    def get_AsyncSession(self):
        """获取异步Session"""
        return self.async_session_maker

    def create_session(self) -> Session:
        """获取Session"""
        return self.session_maker()

    def get_session_context(self) -> Generator[Session, Any, None]:
        """获取Session上下文"""
        with self.session_maker() as session:
            yield session



