import logging
import traceback
from typing import Callable, Any

from sqlalchemy import BinaryExpression, ColumnElement, text
from sqlalchemy.orm import Session, Query

from feng_tools.orm.sqlalchemy.base_models import Model
from feng_tools.orm.sqlalchemy.core.sqlalchemy_enums import SortTypeEnum
from feng_tools.orm.sqlalchemy.core.sqlalchemy_meta_class import ModelMetaClass
from feng_tools.orm.sqlalchemy.sqlalchemy_model_utils import to_dict
from feng_tools.orm.sqlalchemy.sqlalchemy_session_tools import SqlalchemySessionTool


class CrudTool:
    logger = logging.getLogger(__name__)

    def __init__(self, session_tool:SqlalchemySessionTool):
        self.session_tool = session_tool

    def add(self, model):
        with self.session_tool.session_maker() as session:
            try:
                session.add(model)
                session.commit()
                session.refresh(model)
                return model
            except Exception as e:
                session.rollback()
                self.logger.error(f'[Db session add data exception]{e}')
                traceback.print_exc()
                raise e

    def add_all(self, model_list: list) -> list:
        with self.session_tool.session_maker() as session:
            try:
                session.add_all(model_list)
                session.commit()
                for tmp_model in model_list:
                    session.refresh(tmp_model)
                return model_list
            except Exception as e:
                session.rollback()
                self.logger.error(f'[Db session add_all data exception]{e}')
                traceback.print_exc()
                raise e
    def create_commit_query(self, model_class, callback: Callable, *criterion) -> Any:
        """
        创建提交的query
        :param model_class: model类
        :param callback: 回调函数，用于传入 Query
        :param criterion: Query条件， 如：CategoryInfo.id <= 280
        :return: 回调函数的结果，Any
        """
        with self.session_tool.session_maker() as session:
            if criterion:
                db_query = session.query(model_class).filter(*criterion)
            else:
                db_query = session.query(model_class)
            return callback(db_query)

    @classmethod
    def create_id_criterion(cls, model: Any) -> ColumnElement[bool]:
        return type(model).id.__eq__(model.id)


    def update(self, model, *criterion):
        with self.session_tool.session_maker() as session:
            if criterion:
                db_query = session.query(type(model)).filter(*criterion)
            else:
                db_query = session.query(type(model)).filter(self.create_id_criterion(model))
            db_query.update(to_dict(model))
            session.commit()
            return db_query.first()


    def update_batch(self, model_list: list):
        with self.session_tool.session_maker() as db:
            db.add_all(model_list)
            db.commit()
            return model_list


    def save(self, model, *criterion, exist_update: bool = True):
        with self.session_tool.session_maker() as db:
            if criterion:
                db_query = db.query(type(model)).where(*criterion)
            else:
                db_query = db.query(type(model)).where(self.create_id_criterion(model))
            old_data = db_query.first()
            if old_data:
                if exist_update:
                    db_query.update(to_dict(model))
                    db.commit()
                    return db_query.first()
                else:
                    return old_data
            else:
                db.add(model)
                db.commit()
                db.refresh(model)
                return model


    def save_batch_by_where(self, model_list: list, criterion_fun: Callable,
                            exist_update: bool = True) -> list:
        """
        批量存在更新记录，否则插入记录
        :param model_list: Model数据列表
        :param criterion_fun:  通过接受model，返回判断条件, 如：lambda x: type(x).ts_code == x.ts_code
        :param exist_update: 如果存在则更新，如果为False，则如果存在则啥也不做
        :return: Model数据列表
        """
        with self.session_tool.session_maker() as db:
            for tmp_model in model_list:
                criterion = criterion_fun(tmp_model)
                if not criterion and tmp_model.id:
                    criterion = type(tmp_model).id == tmp_model.id
                if type(criterion) == BinaryExpression:
                    criterion = (criterion,)
                if criterion and db.query(type(tmp_model)).filter(*criterion).count() > 0:
                    if exist_update:
                        if criterion:
                            db_query = db.query(type(tmp_model)).filter(*criterion)
                        else:
                            db_query = db.query(type(tmp_model)).filter(self.create_id_criterion(tmp_model))
                        db_query.update(to_dict(tmp_model))
                else:
                    db.add(tmp_model)
            db.commit()
            for tmp_model in model_list:
                db.refresh(tmp_model)
            return model_list



    def delete_by_model(self, model):
        with self.session_tool.session_maker() as db:
            try:
                db.delete(model)
                db.commit()
                return model
            except Exception as e:
                db.rollback()
                self.logger.error(f'[Db session delete_by_model data exception]{e}')
                traceback.print_exc()
                raise e


    def delete(self, model, *criterion):
        """
        删除记录
        :param criterion: 删除条件如：CategoryInfo.id <= 280， 默认按照id删除
        :return:
        """
        with self.session_tool.session_maker() as db:
            try:
                if criterion:
                    model_class = type(model)
                    if issubclass(type(model), Model):
                        model_class = type(model)
                    elif issubclass(type(model), ModelMetaClass):
                        model_class = model
                    db.query(model_class).filter(*criterion).delete()
                else:
                    db.query(type(model)).filter(self.create_id_criterion(model)).delete()
                db.commit()
                return True
            except Exception as e:
                db.rollback()
                self.logger.error(f'[Db session delete data exception]{e}')
                traceback.print_exc()
                raise e


    def delete_by_ids(self, model_class, ids: list[int]):
        """根据id批量删除"""
        with self.session_tool.session_maker() as db:
            try:
                db.query(model_class).filter(model_class.id.in_(ids)).delete()
                db.commit()
            except Exception as e:
                db.rollback()
                self.logger.error(f'[Db session delete_by_ids data exception]{e}')
                traceback.print_exc()
                raise e

    def get_by_id(self, model_class, id_value: int):
        with self.session_tool.session_maker() as db:
            return db.get(model_class, id_value)


    def create_query(self, model_class, *criterion, db:Session) -> Query:
        if criterion:
            return db.query(model_class).filter(*criterion)
        else:
            return db.query(model_class)

    def query_all(self, model_class, *criterion,
                  sort_column: str = 'order_num', sort_type: SortTypeEnum = SortTypeEnum.desc) -> list:
        with self.session_tool.session_maker() as db:
            if sort_type == SortTypeEnum.desc:
                _order_by = getattr(model_class, sort_column).desc()
            else:
                _order_by = getattr(model_class, sort_column).asc()
            return self.create_query(model_class, *criterion, db=db).order_by(_order_by).all()



    def query_one(self, model_class, *criterion,
                  sort_column: str = None, sort_type: SortTypeEnum = SortTypeEnum.desc):
        """根据 where条件查询一条记录"""
        with self.session_tool.session_maker() as db:
            db_query = self.create_query(model_class, *criterion, db=db)
            if sort_column:
                if sort_type == SortTypeEnum.desc:
                    _order_by = getattr(model_class, sort_column).desc()
                else:
                    _order_by = getattr(model_class, sort_column).asc()
                db_query = db_query.order_by(_order_by)
            return db_query.first()


    def query_by_ids(self, model_class, id_list: list[int]) -> list:
        """通过id集合查询"""
        return self.query_all(model_class, type(model_class).id.in_(id_list))


    def query_page(self, model_class, page_num, page_size, *criterion,
                   sort_column: str = 'order_num', sort_type: SortTypeEnum = SortTypeEnum.desc):
        """分页查询"""
        with self.session_tool.session_maker() as db:
            start_index = (page_num - 1) * page_size
            if sort_type == SortTypeEnum.desc:
                _order_by = getattr(model_class, sort_column).desc()
            else:
                _order_by = getattr(model_class, sort_column).asc()
            return self.create_query(model_class, *criterion, db=db).order_by(_order_by).offset(start_index).limit(page_size).all()


    def count(self, model_class, *criterion) -> int:
        """查询记录数"""
        with self.session_tool.session_maker() as db:
            return self.create_query(model_class, *criterion, db=db).count()

    def query_more_by_sql(self, sql: str) -> list[dict[str, Any]]:
        with self.session_tool.session_maker() as session:
            cursor = session.execute(text(sql))
            result_list = []
            for tmp_line in cursor.fetchall():
                result_list.append({tmp_key: tmp_line[index] for index, tmp_key in enumerate(cursor.keys())})
            return result_list

    def query_one_by_sql(self, sql: str) -> dict[str, Any]:
        with self.session_tool.session_maker() as session:
            cursor = session.execute(text(sql))
            sql_result = cursor.fetchone()
            return {tmp_key: sql_result[index] for index, tmp_key in enumerate(cursor.keys())}

    def query_by_sql(self, sql: str) -> list[tuple]:
        """通过sql语句查找"""
        with self.session_tool.session_maker() as session:
            cursor = session.execute(text(sql))
            return cursor.fetchall()

    def exec_by_sql(self, sql: str):
        """通过sql运行"""
        with self.session_tool.session_maker() as session:
            cursor = session.execute(text(sql))
            session.commit()
            return cursor.lastrowid
