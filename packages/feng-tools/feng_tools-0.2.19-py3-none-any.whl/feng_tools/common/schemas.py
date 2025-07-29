from typing import Optional, TypeVar, Generic

from pydantic import BaseModel, Field

_T = TypeVar("_T")

class ApiResponse(BaseModel, Generic[_T]):
    """api接口响应"""
    success:Optional[bool] = Field(default=True, description="是否成功")
    message: Optional[str] = Field(default='success', description="提示信息")
    # 0或者200都是正常
    error_code: Optional[int] = Field(default=0, description="错误编码")
    data:Optional[_T] = Field(default=None, description="返回数据")


class HandleResult(BaseModel, Generic[_T]):
    """处理结果"""
    success:Optional[bool] = Field(default=True, description="是否成功")
    # 0或者200都是正常
    error_code:Optional[int] = Field(default=0, description="错误编码")
    message:Optional[str] = Field(default='success', description="提示信息")
    data:Optional[_T] = Field(default=None, description="返回数据")


