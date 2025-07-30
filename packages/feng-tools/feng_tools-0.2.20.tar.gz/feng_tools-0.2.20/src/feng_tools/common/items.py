from typing import Optional, Literal

from pydantic import BaseModel, Field


class LinkItem(BaseModel):
    """链接项"""
    href: str = Field(title='链接地址')
    title: str = Field(title='链接标题')
    target: Optional[Literal['_blank', '_self', '_parent', '_top']] = '_self'
    code: Optional[str | int] = Field(default=None, title='编码')
    description: Optional[str] = Field(default=None, title='链接描述')
    image: Optional[str] = Field(default=None, title='链接图片')
    icon: Optional[str] = Field(default=None, title='链接图标')
    is_active: Optional[bool] = Field(title='是否激活', default=False)
    children: Optional[list['LinkItem']] = Field(title='子项', default=[])
    data_dict: Optional[dict[str, str | int | float]] = Field(title='数据字典', default=dict())
    is_ok: Optional[bool] = Field(title='是否可正常访问', default=True)
