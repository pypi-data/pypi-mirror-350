from typing import Type, Optional, TypeVar, Generic

from fastapi import APIRouter
from pydantic_settings import BaseSettings
from sqlalchemy import Column

try:
    from sqlmodel.main import FieldInfo
    from feng_tools.orm.sqlmodel.base_models import BaseModel
    is_sqlmodel = True
except  ImportError:
    is_sqlmodel = False

from feng_tools.orm.sqlalchemy.base_models import Model



def create_exclude_fields(new_exclude_fields:list[str]=None,
                          base_exclude_fields=None)-> set[str]:
    """创建排除字段集"""
    if base_exclude_fields is None:
        base_exclude_fields = ['created_at', 'updated_at', 'is_enable', 'deleted', 'deleted_at', 'order_num']
    if not new_exclude_fields:
        return set(base_exclude_fields)
    if base_exclude_fields:
        new_exclude_fields.extend(base_exclude_fields)
    return set(new_exclude_fields)

if is_sqlmodel:
    _M = TypeVar("_M", bound=BaseModel)
    _F = TypeVar("_F", bound=FieldInfo)
else:
    _M = TypeVar("_M", bound=Model)
    _F = TypeVar("_F", bound=Column)

class ModelAdminSettings(BaseSettings, Generic[_M, _F]):
    """模型管理"""
    # 该模型的api接口前缀
    api_prefix: Optional[str] = None
    # 改模型的api路由（当有该值时，可以不设置api_prefix；没有该值时，使用api_prefix创建）
    api_router: Optional[APIRouter] = None
    # 页面标题(当为空时，取：模型的__doc__管理)
    page_title: Optional[str] = None
    # 模型类
    model_class:Type[_M]
    # 模型类默认包含字段（即使包含了排除字段，也会被排除）
    schema_fields:Optional[list[str|_F]] = None
    # 模型类默认排除字段
    exclude_fields:Optional[set[str]] = create_exclude_fields(['password', ])
    # 添加
    has_add_api: Optional[bool] = True
    add_fields:Optional[list[str|_F]] = None
    add_exclude_fields: Optional[set[str]] = create_exclude_fields(['id', ])
    # 查看
    has_read_api:Optional[bool] = True
    read_fields: Optional[list[str|_F]] = None
    read_exclude_fields: Optional[set[str]] = create_exclude_fields(['password', ])
    # 修改
    has_update_api: Optional[bool] = True
    update_fields: Optional[list[str|_F]] = None
    update_exclude_fields: Optional[set[str]] = create_exclude_fields(['id', ])
    # 删除
    has_delete_api: Optional[bool] = True
    # 列表
    has_list_api: Optional[bool] = True
    # 分页列表
    has_list_by_page_api: Optional[bool] = True
    # 过滤字段
    filter_fields: Optional[set[str]] = None
    list_fields: Optional[list[str|_F]] = None
    list_exclude_fields: Optional[set[str]] = create_exclude_fields(['password', ])
    # 是否包含页面的api
    has_page_api:Optional[bool] = True
    class Config:
        arbitrary_types_allowed = True
