from typing import Callable, Any

from sqlalchemy import BinaryExpression, ColumnElement

from sqlalchemy.orm import Session, Query

from feng_tools.orm.sqlalchemy.base_models import Model
from feng_tools.orm.sqlalchemy.core.sqlalchemy_enums import SortTypeEnum
from feng_tools.orm.sqlalchemy.core.sqlalchemy_meta_class import ModelMetaClass
from feng_tools.orm.sqlalchemy.sqlalchemy_model_utils import to_dict


def add(model, db: Session, auto_commit=True):
    db.add(model)
    if auto_commit:
        db.commit()
        db.refresh(model)
    return model


def add_all(model_list: list, db: Session) -> list:
    db.add_all(model_list)
    db.commit()
    for tmp_model in model_list:
        db.refresh(tmp_model)
    return model_list


def create_commit_query(model_class, callback: Callable, *criterion, db: Session) -> Any:
    """
    创建提交的query
    :param model_class: model类
    :param callback: 回调函数，用于传入 Query
    :param criterion: Query条件， 如：CategoryInfo.id <= 280
    :param db: 自动导入的db
    :return: 回调函数的结果，Any
    """
    if criterion:
        db_query = db.query(model_class).filter(*criterion)
    else:
        db_query = db.query(model_class)
    return callback(db_query)


def create_id_criterion(model: Any) -> ColumnElement[bool]:
    return type(model).id.__eq__(model.id)


def update(model, *criterion, db: Session, auto_commit=True):
    if criterion:
        db_query = db.query(type(model)).filter(*criterion)
    else:
        db_query = db.query(type(model)).filter(create_id_criterion(model))
    db_query.update(to_dict(model))
    if auto_commit:
        db.commit()
    return db_query.first()


def update_batch(model_list: list, db: Session):
    db.add_all(model_list)
    db.commit()
    return model_list


def save(model, *criterion, db: Session, exist_update: bool = True):
    if criterion:
        db_query = db.query(type(model)).where(*criterion)
    else:
        db_query = db.query(type(model)).where(create_id_criterion(model))
    old_data = db_query.first()
    if old_data:
        if exist_update:
            db_query.update(to_dict(model))
            return db_query.first()
        else:
            return old_data
    else:
        return add(model, db=db)


def save_batch_by_where(model_list: list, criterion_fun: Callable, db: Session,
                        exist_update: bool = True) -> list:
    """
    批量存在更新记录，否则插入记录
    :param model_list: Model数据列表
    :param criterion_fun:  通过接受model，返回判断条件, 如：lambda x: type(x).ts_code == x.ts_code
    :param db: 自动注入的Session
    :param exist_update: 如果存在则更新，如果为False，则如果存在则啥也不做
    :return: Model数据列表
    """
    for tmp_model in model_list:
        criterion = criterion_fun(tmp_model)
        if not criterion and tmp_model.id:
            criterion = type(tmp_model).id == tmp_model.id
        if type(criterion) == BinaryExpression:
            criterion = (criterion,)
        if criterion and db.query(type(tmp_model)).filter(*criterion).count() > 0:
            if exist_update:
                update(tmp_model, *criterion, db=db, auto_commit=False)
        else:
            add(tmp_model, db=db, auto_commit=False)
    db.commit()
    for tmp_model in model_list:
        db.refresh(tmp_model)
    return model_list



def delete_by_model(model, db: Session):
    db.delete(model)
    db.commit()
    return model


def delete(model, *criterion, db: Session):
    """
    删除记录
    :param criterion: 删除条件如：CategoryInfo.id <= 280， 默认按照id删除
    :return:
    """
    if criterion:
        model_class = type(model)
        if issubclass(type(model), Model):
            model_class = type(model)
        elif issubclass(type(model), ModelMetaClass):
            model_class = model
        db.query(model_class).filter(*criterion).delete()
    else:
        db.query(type(model)).filter(create_id_criterion(model)).delete()
    db.commit()
    return True


def delete_by_class(model_class, *criterion, db: Session):
    """
    删除记录
    :param criterion: 删除条件如：CategoryInfo.id <= 280， 默认按照id删除
    :return:
    """
    if criterion:
        db.query(model_class).filter(*criterion).delete()
        db.commit()
    else:
        raise AttributeError('Args [*criterion] can not be None')
    return True


def delete_by_ids(model_class, ids: list[int], db: Session):
    """根据id批量删除"""
    db.query(model_class).filter(model_class.id.in_(ids)).delete()
    db.commit()


def get_by_id(model_class, id_value: int, db: Session):
    return db.get(model_class, id_value)


def create_query(model_class, *criterion, db: Session) -> Query:
    if criterion:
        return db.query(model_class).filter(*criterion)
    else:
        return db.query(model_class)


def query_all(model_class, *criterion, db: Session,
              sort_column: str = 'order_num', sort_type: SortTypeEnum = SortTypeEnum.desc) -> list:
    if sort_type == SortTypeEnum.desc:
        _order_by = getattr(model_class, sort_column).desc()
    else:
        _order_by = getattr(model_class, sort_column).asc()
    return create_query(model_class, *criterion, db=db).order_by(_order_by).all()


def query_one(model_class, *criterion, db: Session):
    """根据 where条件查询一条记录"""
    return create_query(model_class, *criterion, db=db).first()


def query_by_ids(model_class, id_list: list[int], db: Session) -> list:
    """通过id集合查询"""
    return query_all(model_class, type(model_class).id.in_(id_list), db=db)


def query_page(model_class, page_num, page_size, *criterion, db: Session,
               sort_column: str = 'order_num', sort_type: SortTypeEnum = SortTypeEnum.desc):
    """分页查询"""
    start_index = (page_num - 1) * page_size
    if sort_type == SortTypeEnum.desc:
        _order_by = getattr(model_class, sort_column).desc()
    else:
        _order_by = getattr(model_class, sort_column).asc()
    return create_query(model_class, *criterion, db=db).order_by(_order_by).offset(start_index).limit(page_size).all()


def count(model_class, *criterion, db: Session) -> int:
    """查询记录数"""
    return create_query(model_class, *criterion, db=db).count()
