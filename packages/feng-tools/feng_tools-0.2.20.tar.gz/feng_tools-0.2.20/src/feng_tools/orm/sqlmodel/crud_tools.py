"""
crud相关工具
"""
from typing import Union, Type, Callable

from sqlmodel import Session, select, SQLModel, Field,  func
from sqlalchemy.sql._typing import (
    _ColumnExpressionArgument,
)


class CrudTools:
    def __init__(self, engine):
        self.engine = engine


    @classmethod
    def get_model_class(cls, model:type[SQLModel]):
        if isinstance(model, SQLModel):
            model_class = type(model)
        else:
            model_class = model
        return model_class

    def get_one(self, model:type[SQLModel], id_value: int)-> Type[SQLModel] | None:
        """ 获取一条数据
        :param model: 模型
        :param id_value: 主键值
        :return: 主键对应数据
        """
        with Session(self.engine) as session:
            return session.get(self.get_model_class(model), id_value)

    def query_one(self, model:type[SQLModel], *where_clause: Union[_ColumnExpressionArgument[bool], bool]) -> list:
        """ 获取所有数据
        :param model: 模型
        :param where_clause: 条件
        :return: 数据列表
        """
        with Session(self.engine) as session:
            statement = select(self.get_model_class(model)).where(*where_clause)
            one_data = session.exec(statement).first()
        return one_data

    def query_all(self, model:type[SQLModel], *where_clause: Union[_ColumnExpressionArgument[bool], bool]) -> list:
        """ 获取所有数据
        :param model: 模型
        :param where_clause: 条件
        :return: 数据列表
        """
        with Session(self.engine) as session:
            statement = select(self.get_model_class(model)).where(*where_clause)
            data_list = session.exec(statement).all()
        return data_list

    def query_by_page(self, model:type[SQLModel], page:int, page_size:int, *where_clause: Union[_ColumnExpressionArgument[bool], bool]) -> list:
        """ 获取分页数据
        :param model: 模型
        :param page: 页码
        :param page_size: 每页条数
        :param where_clause: 条件
        :return: 数据列表
        """

        with Session(self.engine) as session:
            statement = select(self.get_model_class(model)).where(*where_clause).offset((page - 1) * page_size).limit(page_size)
            data_list = session.exec(statement).all()
        return data_list
    def insert_one(self, model_data:SQLModel) -> SQLModel:
        """ 插入一条数据
        """
        with Session(self.engine) as session:
            session.add(model_data)
            session.commit()
            session.refresh(model_data)
        return model_data

    def update_one(self, model:type[SQLModel], data_dict:dict, id_value: int=None)->Type[SQLModel] | None:
        """更新一条数据
        :param model: 模型
        :param id_value: 主键值
        :param data_dict: 数据字典
        """
        if not id_value:
            id_value = getattr(model, 'id')
        with Session(self.engine) as session:
            db_data = session.get(self.get_model_class(model), id_value)
            if db_data:
                model_fields = getattr(model, "__fields__")
                for key, value in data_dict.items():
                    if key in model_fields:
                        setattr(db_data, key, value)
                session.add(db_data)
                session.commit()
                session.refresh(db_data)
            return db_data

    def delete_one(self, model:type[SQLModel], id_value: int) -> bool:
        """ 删除一条数据
        :param model: 模型
        :param id_value: 主键值
        :return: 是否删除成功
        """
        with Session(self.engine) as session:
            db_data = session.get(self.get_model_class(model), id_value)
            if db_data:
                session.delete(db_data)
                session.commit()
                return True
        return False

    def get_count(self, model:type[SQLModel], *where_clause: Union[_ColumnExpressionArgument[bool], bool]):
        """ 获取数据条数
        :param model: 模型
        :param where_clause: 条件
        :return: 数据条数
        """
        with Session(self.engine) as session:
            statement = select(self.get_model_class(model)).where(*where_clause)
            total = session.exec(select(func.count()).select_from(statement.subquery())).one()
        return total

    def get_max(self, model:type[SQLModel], field:Field):
        """ 获取最大值
        :param model: 模型
        :param field: 字段
        :return: 最大值
        """
        with Session(self.engine) as session:
            statement = select(self.get_model_class(model)).order_by(field.desc())
            max_value = session.exec(statement).first()
        return max_value

    def get_min(self, model:type[SQLModel], field:Field):
        """ 获取最小值
        :param model: 模型
        :param field: 字段
        :return: 最小值
        """
        with Session(self.engine) as session:
            statement = select(self.get_model_class(model)).order_by(field.asc())
            min_value = session.exec(statement).first()
        return min_value

    def get_avg(self, model:type[SQLModel], field:Field):
        """ 获取平均值
        :param model: 模型
        :param field: 字段
        :return: 平均值
        """
        with Session(self.engine) as session:
            statement = select(func.avg(field)).select_from(self.get_model_class(model))
            avg_value = session.exec(statement).one()
        return avg_value

    def get_sum(self, model:type[SQLModel], field:Field):
        """ 获取总和
        :param model: 模型
        :param field: 字段
        :return: 总和
        """
        with Session(self.engine) as session:
            statement = select(func.sum(field)).select_from(self.get_model_class(model))
            sum_value = session.exec(statement).one()
        return sum_value

    def get_max_min_avg_sum(self, model:type[SQLModel], field:Field):
        """ 获取最大值、最小值、平均值、总和
        :param model: 模型
        :param field: 字段
        :return: 最大值、最小值、平均值、总和
        """
        with Session(self.engine) as session:
            statement = select(func.max(field), func.min(field), func.avg(field), func.sum(field)).select_from(self.get_model_class(model))
            max_min_avg_sum = session.exec(statement).one()
        return max_min_avg_sum

    def get_max_min_avg_sum_by_page(self, model:type[SQLModel], page:int, page_size:int, field:Field):
        """ 获取分页最大值、最小值、平均值、总和
        :param model: 模型
        :param page: 页码
        :param page_size: 每页条数
        :param field: 字段
        :return: 最大值、最小值、平均值、总和
        """
        with Session(self.engine) as session:
            statement = select(func.max(field), func.min(field), func.avg(field), func.sum(field)).select_from(self.get_model_class(model)).offset((page - 1) * page_size).limit(page_size)
            max_min_avg_sum = session.exec(statement).one()
        return max_min_avg_sum

    def auto_db(self, func:Callable):
        """装饰器：自动管理数据库会话"""
        def wrapper(*args, **kwargs):
            with Session(self.engine) as session:
                if 'db' not in kwargs:
                    kwargs['db'] = session
                return func(*args, **kwargs)
        return wrapper

    def auto_commit_db(self, func:Callable):
        """装饰器：自动管理数据库会话"""
        def wrapper(*args, **kwargs):
            with Session(self.engine) as session:
                if 'db' not in kwargs:
                    kwargs['db'] = session
                try:
                    result = func(*args, **kwargs)
                    session.commit()
                    return result
                except Exception as e:
                    session.rollback()
                    raise e
        return wrapper