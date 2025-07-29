import math
from typing import Generic, TypeVar, Optional, List

from pydantic import computed_field, BaseModel

from feng_tools.base.pydantic import common_models

_T = TypeVar("_T")

class ApiResponse(common_models.ApiResponse):
    """api接口响应"""
    @computed_field
    @property
    def status(self) -> Optional[int]:
        return 0 if self.success else 1

    @computed_field
    @property
    def msg(self) -> Optional[str]:
        return self.message


class ListData(BaseModel, Generic[_T]):
    """列表数据"""
    # 总数量
    total:Optional[int] = None
    # 数据项
    item_list:Optional[List[_T]] = None


class PageListData(ListData, Generic[_T]):
    """分页列表数据"""
    # 页码，从1开始
    page_num: Optional[int] = None
    # 分页大小，如：10
    page_size: Optional[int] = None
    # 分页数量
    page_count: Optional[int] = None

    @computed_field
    @property
    def has_next(self) -> Optional[bool]:
        return self.page_num<math.ceil(self.total/self.page_size)

    @computed_field
    @property
    def count(self) -> Optional[int]:
        return self.total

    @computed_field
    @property
    def rows(self) -> Optional[Optional[List[_T]]]:
        return self.item_list
