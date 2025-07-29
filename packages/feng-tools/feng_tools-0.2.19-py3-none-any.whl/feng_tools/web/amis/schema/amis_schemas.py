"""
Amis Schemas
pip install pydantic
"""
import math
from typing import Optional, Any, List
from pydantic import BaseModel, computed_field


class BaseResponse(BaseModel):
    status:Optional[int] = 0
    msg:Optional[str] = None
    data:Optional[dict[str, Any]] = None


class TableData(BaseModel):
    """表格数据"""
    # 总数据量，用于生成分页
    total:Optional[int] = 0
    # 当前页码
    page_num:Optional[int] = 1
    # 每页显示的行数
    page_size:Optional[int] = 20
    # 页数量
    page_count:Optional[int] = 0
    # 是否有下一页
    has_next:Optional[bool] = None
    # 行的数据
    items:Optional[List[Any]] = []

    @computed_field
    @property
    def hasNext(self) -> Optional[bool]:
        if self.has_next is None:
            return self.page_num<math.ceil(self.total/self.page_size)
        return self.has_next

    @computed_field
    @property
    def page(self) -> Optional[int]:
        return self.page_num

    @computed_field
    @property
    def perPage(self) -> Optional[int]:
        return self.page_size

    @computed_field
    @property
    def count(self) -> Optional[int]:
        return self.total


class TableResponse(BaseResponse):
    """表格响应"""
    data:TableData = []



