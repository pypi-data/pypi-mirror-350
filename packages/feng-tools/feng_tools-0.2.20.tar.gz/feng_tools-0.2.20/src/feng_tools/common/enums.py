import enum
import typing
from typing import Optional, Any

from pydantic import BaseModel, Field
from sqlalchemy import TypeDecorator, Integer, String, Float,DECIMAL,Enum


class EnumItem(BaseModel):
    # 是否是默认项
    is_default: Optional[bool] = False
    # 标题
    title: str = Field(default=None, title='枚举标题')
    description: Optional[str] = Field(default=None, title='枚举描述')
    value: Optional[str | int | float] = Field(default=None, title='枚举值')
    data_dict: Optional[dict[str, Any]] = Field(title='数据字典', default=dict())

# 自定义 SQLAlchemy 类型处理器
class EnumItemType(TypeDecorator):
    impl = Integer
    cache_ok = True

    def __init__(self, enum_type):
        super().__init__()
        self.enum_type = enum_type
        self.value_to_member = {member.value.value: member for member in enum_type}
    def process_bind_param(self, value, dialect):
        """存入数据库的值"""
        if value is None:
            return None
        if hasattr( value.value, 'value'):
            return value.value.value
        return value.value
    def process_result_value(self, value, dialect):
        """从数据库转换为枚举成员"""
        if value is None:
            return None
        return self.value_to_member.get(value)



class IntegerEnum(EnumItemType):
    impl = Integer
class StringEnum(EnumItemType):
    impl = String
class FloatEnum(EnumItemType):
    impl = DECIMAL



class GenderTypeEnum(enum.Enum):
    """用户的性别"""
    # 值为 1 时是男性
    male = EnumItem(title='男', value=1)
    # 值为 2 时是女性
    female = EnumItem(title='女', value=2)
    # 值为 0 时是未知
    unknown = EnumItem(title='未知', value=0)

    @staticmethod
    def get_enum(value: int) -> typing.Union['GenderTypeEnum', None]:
        for item in GenderTypeEnum:
            if item.value.value == value:
                return item
        return None

    @staticmethod
    def get_enum_list() -> list[dict[str, Any]]:
        return [item.value.model_dump() for item in GenderTypeEnum]

if __name__ == '__main__':
    print(GenderTypeEnum.get_enum(2))
    print(GenderTypeEnum.get_enum_list())