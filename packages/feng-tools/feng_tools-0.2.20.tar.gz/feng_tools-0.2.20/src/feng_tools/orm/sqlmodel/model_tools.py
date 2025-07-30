"""
SQLModel 模型相关工具
pip install sqlmodel
"""
from typing import Optional, List, Any, get_origin, Annotated, Dict, get_args

from fastapi._compat import sequence_annotation_to_type
from pydantic import BaseModel
from pydantic.v1.typing import is_union, is_literal_type, is_none_type
from pydantic.v1.utils import lenient_issubclass
from sqlmodel import SQLModel
from sqlmodel.main import FieldInfo


def get_model_fields(model_class:type[SQLModel]) -> dict[str, FieldInfo]:
    """获取模型所有字段"""
    return getattr(model_class, "__fields__")

def get_allow_fields(model_field_dict:dict[str, FieldInfo],
                        include_fields:Optional[List[str|FieldInfo]] = None,
                        exclude_fields:Optional[list[str]]=None) -> dict[str, FieldInfo]:
    """获取模型的允许字段"""
    allow_field_dict = dict()
    for key, field_info in model_field_dict.items():
        if exclude_fields and key in exclude_fields:
            continue
        if include_fields is None:
            allow_field_dict[key] = field_info
        elif len(include_fields) == 0:
            break
        else:
            for tmp_field in include_fields:
                if not isinstance(tmp_field, str):
                    tmp_field = getattr(tmp_field, 'key')
                if key == tmp_field:
                    allow_field_dict[key] = field_info
    return allow_field_dict

def get_field_annotation(field_info:FieldInfo) -> type:
    """获取字段类型"""
    return field_info.annotation


def get_annotation_outer_type(tp: Any) -> Any:
    """获取声明的基本类型."""
    if tp is Ellipsis:
        return Any
    origin = get_origin(tp)
    if origin is None:
        return tp
    elif is_union(origin) or origin is Annotated:
        pass
    elif origin in sequence_annotation_to_type:
        return sequence_annotation_to_type[origin]
    elif origin in {Dict, dict}:
        return dict
    elif lenient_issubclass(origin, BaseModel):
        return origin
    args = get_args(tp)
    for arg in args:
        if is_literal_type(tp):
            arg = type(arg)
        if is_none_type(arg):
            continue
        return get_annotation_outer_type(arg)
    return tp



