"""
sqlmodel 基础模型
"""
from datetime import datetime, date
from typing import Optional

from sqlmodel import SQLModel, Field


class BaseModel(SQLModel):
    """基础模型"""
    id: Optional[int] = Field(default=None, title='主键', primary_key=True, nullable=False, index=True, unique=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now, title='添加时间', nullable=True)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now, title='修改时间', nullable=True)
    is_enable: Optional[bool]  = Field(default=True, title='是否可用', nullable=True)
    deleted: Optional[bool] = Field(default=False, title='是否删除', nullable=True)
    deleted_at: Optional[datetime] = Field(default=None, title='删除时间', nullable=True)
    order_num: Optional[float]  = Field(default=100, title='排序值', nullable=True)
    def to_dict(self, date_format="%Y-%m-%d", datetime_formate="%Y-%m-%d %H:%M:%S"):
        """将模型对象转换为字典格式"""
        data = self.model_dump()
        # 处理日期字段，格式化为指定格式
        for key, value in data.items():
            if value is not None:
                if isinstance(value, datetime):
                    data[key] = value.strftime(datetime_formate)
                elif isinstance(value, date):
                    data[key] = value.strftime(date_format)
        return data

    def to_json(self, date_format="%Y-%m-%d", datetime_formate="%Y-%m-%d %H:%M:%S"):
        """将模型对象转换为json格式"""
        return self.to_dict(date_format, datetime_formate)