from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import create_engine

from feng_tools.orm.sqlalchemy.sqlalchemy_settings import DatabaseSettings


def new_engine(settings:DatabaseSettings):
    """新建Engine"""
    return create_engine(
        settings.url,
        pool_size=settings.pool_size,
        max_overflow=settings.max_overflow,
        pool_timeout=settings.pool_timeout,
        pool_recycle=settings.pool_recycle,
        echo=settings.echo,
        echo_pool=settings.echo_pool,
        pool_pre_ping=settings.pool_pre_ping)


def new_async_engine(async_settings:DatabaseSettings):
    """新建异步Engine"""
    return create_async_engine(
        async_settings.url,
        pool_size=async_settings.pool_size,
        max_overflow=async_settings.max_overflow,
        pool_timeout=async_settings.pool_timeout,
        pool_recycle=async_settings.pool_recycle,
        echo=async_settings.echo,
        echo_pool=async_settings.echo_pool,
        pool_pre_ping=async_settings.pool_pre_ping)