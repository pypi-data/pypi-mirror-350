from datetime import datetime, date, time
from typing import Any

from sqlalchemy import Column, DateTime, Boolean, Float, func, BigInteger

from feng_tools.orm.sqlalchemy.core.sqlalchemy_meta_class import ModelMetaClass
from feng_tools.orm.sqlalchemy.init import Base


class Model(Base, metaclass=ModelMetaClass):
    """模型根类"""
    __abstract__ = True

    id = Column(BigInteger, comment='主键', primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, comment='添加时间', default=func.now())
    updated_at = Column(DateTime, comment='修改时间', default=func.now(), onupdate=func.now())
    is_enable = Column(Boolean, comment='是否可用', default=True)
    deleted = Column(Boolean, comment='是否删除', default=False)
    deleted_at = Column(DateTime, comment='删除时间', default=None)
    order_num = Column(Float, comment='排序值', default=100)

    def to_dict(self) -> dict[str, Any]:
        return {
            c.name: getattr(self, c.name)
            for c  in self.__table__.columns
        }
    def to_json(self, date_format="%Y-%m-%d", datetime_formate="%Y-%m-%d %H:%M:%S",
                time_formate="%H:%M:%S"):
        data_dict =  self.to_dict()
        for key, value in data_dict.items():
            if isinstance(value, datetime):
                data_dict[key] = value.strftime(datetime_formate)
            elif isinstance(value, date):
                data_dict[key] = value.strftime(date_format)
            elif isinstance(value, time):
                data_dict[key] = value.strftime(time_formate)
        return data_dict

    def get_update_data(self):
        """获取更新字段
        使用示例：
        # 执行批量更新
        await session.execute(
            update(Model)
            .where(Model.id == new_model.id)
            .values(**update_data)
        )
        """
        return {k: v for k, v in self.__dict__.items()
                       if not k.startswith('_') and k != 'id'}

