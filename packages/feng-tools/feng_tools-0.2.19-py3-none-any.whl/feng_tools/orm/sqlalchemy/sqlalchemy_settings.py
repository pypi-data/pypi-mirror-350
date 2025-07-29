from typing import Optional

from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    # 数据库连接 URL，用于同步数据库连接。格式如：mysql+pymysql://user:password@host:port/dbname
    url: Optional[str] = None
    # 异步数据库连接 URL，用于异步数据库操作。格式如：mysql+aiomysql://user:password@host:port/dbname
    async_url: Optional[str] = None
    # 数据库连接池大小，默认保留的连接数
    pool_size: Optional[int] = 5
    # 连接池最大溢出数量，即最多允许超过 pool_size 的连接数
    max_overflow: Optional[int] = 10
    # 获取连接的最大等待时间（秒），超时将抛出异常。
    pool_timeout: Optional[int] = 30
    # 连接池回收时间（秒），超过该时间的连接会被关闭并重新创建，防止长时间空闲导致的断开。
    pool_recycle: Optional[int] = 3600
    # 是否启用 SQL 日志输出，设为 True 时会在控制台打印执行的 SQL 语句。
    echo: Optional[int] = True
    # 连接池日志输出级别，常见值有 'debug', 'info' 等。
    echo_pool: Optional[str] = 'debug'
    # 是否在每次从连接池获取连接前检查连接有效性，避免使用已断开的连接。
    pool_pre_ping: Optional[bool] = True
    # 是否（后进先出）
    pool_use_lifo: Optional[bool] = True

class DbSessionSettings(BaseSettings):
    # 是否自动提交
    auto_commit: Optional[bool] = False
    # 是否自动flush
    auto_flush: Optional[bool] = False
    # 提交事务后是否使所有数据库映射对象过期。设为 True 时在提交后会刷新对象数据。
    expire_on_commit: Optional[bool] = False