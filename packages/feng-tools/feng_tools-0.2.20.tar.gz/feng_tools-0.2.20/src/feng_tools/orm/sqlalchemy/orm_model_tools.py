"""
ORM的Model工具
"""
from typing import Any

from pydantic import BaseModel
from pydantic.fields import FieldInfo
from sqlalchemy import Column

from feng_tools.base.convert import type_convert_tools
from feng_tools.orm.sqlalchemy.base_models import Model


def _convert_value_type(field_value: Any, model_column_field: FieldInfo | Column,
                        date_time_format: str) -> Any:
    """转换ORM的Model的值的类型为pydantic模型值"""
    field_type = None
    if isinstance(model_column_field, FieldInfo):
        field_type = model_column_field.annotation
    elif isinstance(model_column_field, Column):
        field_type = model_column_field.type.python_type
    return type_convert_tools.convert_value_to_type(field_value, field_type, datetime_format=date_time_format)


def _convert_orm_value_type(field_value: Any, py_model_field: FieldInfo,
                            date_time_format: str) -> Any:
    """转换ORM的Model的值的类型为pydantic模型值"""
    return _convert_value_type(field_value, py_model_field, date_time_format)


def orm_model_to_py_model(orm_model: Any, py_model_class: type[BaseModel],
                          date_time_format: str = '%Y-%m-%d %H:%M:%S',
                          field_mapping: dict[str, str] = None) -> Any:
    """
    ORM模型转为pydantic的Model
    :param orm_model: orm的model对象
    :param py_model_class: pydantic的Model类
    :param date_time_format: date_time的字符串格式
    :param field_mapping: 字段映射集{ orm的model字段名: pydantic的Model字段名},示例：{'category_code':'category_name'}
    :return:  pydantic的Model对象
    """
    orm_dict = {c.name: getattr(orm_model, c.name) for c in orm_model.__table__.columns}
    py_model_fields = py_model_class.model_fields
    convert_dict = dict()
    for tmp_field, tmp_value in orm_dict.items():
        if tmp_field in py_model_fields and tmp_value is not None:
            convert_dict[tmp_field] = _convert_orm_value_type(tmp_value, py_model_fields.get(tmp_field),
                                                              date_time_format)
        if field_mapping and tmp_field in field_mapping:
            convert_dict[field_mapping.get(tmp_field)] = _convert_orm_value_type(tmp_value,
                                                                                 py_model_fields.get(
                                                                                     field_mapping.get(tmp_field)),
                                                                                 date_time_format)
    return py_model_class(**convert_dict)


def _convert_py_value_type(field_value: Any, orm_model_column: Column,
                           date_time_format: str) -> Any:
    """转换pydantic的Model的值的类型为ORM模型值"""
    return _convert_value_type(field_value, orm_model_column, date_time_format)


def py_model_to_orm_model(py_model: BaseModel, orm_model_class: type[Model],
                          date_time_format: str = '%Y-%m-%d %H:%M:%S',
                          field_mapping: dict[str, str] = None) -> Model:
    """
    pydantic的Model转为ORM模型
    :param py_model: pydantic的Model对象
    :param orm_model_class: orm的model类
    :param date_time_format: date_time的字符串格式
    :param field_mapping: 字段映射集{ pydantic的Model字段名：orm的model字段名},示例：{'category_title':'sub_title'}
    :return: orm的model对象
    """
    py_dict = py_model.model_dump()
    orm_column_dict = {c.name: c for c in orm_model_class.__table__.columns}
    orm_dict = dict()
    for tmp_field, tmp_value in py_dict.items():
        if tmp_value is not None and tmp_field in orm_column_dict:
            orm_column = orm_column_dict.get(tmp_field)
            orm_dict[tmp_field] = _convert_py_value_type(tmp_value, orm_column, date_time_format)
        if field_mapping and tmp_field in field_mapping:
            orm_dict[field_mapping.get(tmp_field)] = _convert_orm_value_type(tmp_value,
                                                                             orm_column_dict.get(
                                                                                 field_mapping.get(tmp_field)),
                                                                             date_time_format)
    return orm_model_class(**orm_dict)


def orm_model_to_dict(orm_model: Any, skip_none: bool = False):
    """
    orm的Model转为json
    :param orm_model: orm的Model对象
    :param skip_none: 是否跳过None值
    :return: dict数据
    """
    orm_dict = {c.name: getattr(orm_model, c.name) for c in orm_model.__table__.columns}
    if skip_none:
        result_dict = dict()
        for tmp_key, tmp_value in orm_dict.items():
            if tmp_value is not None:
                result_dict[tmp_key] = tmp_value
        return result_dict
    return orm_dict
