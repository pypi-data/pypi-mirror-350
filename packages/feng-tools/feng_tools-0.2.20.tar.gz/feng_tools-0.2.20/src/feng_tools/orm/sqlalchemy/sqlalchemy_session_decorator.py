import logging
import traceback

from sqlalchemy import Engine

from feng_tools.base.decorator.decorator_tools import run_func
from feng_tools.orm.sqlalchemy.sqlalchemy_session_tools import SqlalchemySessionTool

logger = logging.getLogger(__name__)


def auto_commit_db(session_tool: SqlalchemySessionTool, retry: int = 0):
    """自动注入自动提交的db: Session"""
    def auto_wrap(func):
        def wrap(*args, **kwargs):
            if 'db' in kwargs:
                return run_func(func, *args, **kwargs)
            with session_tool.session_maker() as session:
                try:
                    kwargs['db'] = session
                    result = run_func(func, *args, **kwargs)
                    session.commit()
                    return result
                except Exception as e:
                    logger.error(f'[Db session commit data exception]{e}')
                    traceback.print_exc()
                    session.rollback()
                    if retry > 0:
                        kwargs.pop('db')
                        return auto_commit_db(session_tool, retry - 1)(func)(*args, **kwargs)
                    raise e
        return wrap
    return auto_wrap


def auto_db(session_tool: SqlalchemySessionTool):
    """自动注入db: Session"""
    def auto_wrap(func):
        def wrap(*args, **kwargs):
            if 'db' in kwargs:
                return run_func(func, *args, **kwargs)
            with session_tool.session_maker() as session:
                kwargs['db'] = session
                return run_func(func, *args, **kwargs)
        return wrap
    return auto_wrap


def auto_commit_conn(engine:Engine):
    """自动注入自动提交的conn: Connection"""

    def auto_wrap(func):
        def wrap(*args, **kwargs):
            if 'conn' in kwargs:
                return run_func(func, *args, **kwargs)
            with engine.connect() as conn:
                try:
                    kwargs['conn'] = conn
                    result = run_func(func, *args, **kwargs)
                    conn.commit()
                    return result
                except Exception as e:
                    logger.error(f'[Db connection commit data exception]{e}')
                    traceback.print_exc()
                    conn.rollback()
                    raise e
        return wrap

    return auto_wrap


def auto_conn(engine:Engine):
    """自动注入conn: Connection"""

    def auto_wrap(func):
        def wrap(*args, **kwargs):
            if 'conn' in kwargs:
                return run_func(func, *args, **kwargs)
            with engine.connect() as conn:
                kwargs['conn'] = conn
                return run_func(func, *args, **kwargs)
        return wrap
    return auto_wrap
