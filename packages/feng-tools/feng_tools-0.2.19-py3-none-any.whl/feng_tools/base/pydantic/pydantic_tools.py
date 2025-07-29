"""
pydantic 工具
- pip install pydantic -i https://pypi.tuna.tsinghua.edu.cn/simple/
"""
from typing import Type, Optional

import pydantic
from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo



def _get_model_properties(orm_model_class: Type, add_flag: bool = False) \
        -> dict[str, tuple[type[BaseModel], FieldInfo]]:
    """通过orm类，获取model类的属性"""
    orm_column_dict = {c.name: c for c in orm_model_class.__table__.columns}
    add_ignore_list = ['id', 'add_time', 'update_time', 'is_enable', 'order_num']
    properties = dict()
    for tmp_field, tmp_column in orm_column_dict.items():
        if add_flag and tmp_field in add_ignore_list:
            continue
        tmp_type = tmp_column.type.python_type
        properties[tmp_field] = (Optional[tmp_type], Field(default=None, title=tmp_column.comment))
    return properties


def create_model_by_po(orm_model_class: Type, add_flag: bool = False) -> type[BaseModel]:
    """通过orm模型创建pydantic模型类"""
    table_name = orm_model_class.__table__.name
    vo_class_name = ''.join([tmp.title() for tmp in table_name.split('_')])
    class_name = f'{vo_class_name}Form'
    if add_flag:
        class_name = f'{vo_class_name}AddForm'
    return pydantic.create_model(
        __model_name=class_name,
        __config__=None,
        __base__=None,
        __module__=__name__,
        __validators__=None,
        __cls_kwargs__=None,
        __slots__=None,
        **_get_model_properties(orm_model_class, add_flag)
    )


