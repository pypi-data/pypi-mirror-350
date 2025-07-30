from sqlalchemy import Engine
from sqlmodel import SQLModel


def init_db(engine:Engine):
    """初始化数据库"""
    SQLModel.metadata.create_all(engine)
