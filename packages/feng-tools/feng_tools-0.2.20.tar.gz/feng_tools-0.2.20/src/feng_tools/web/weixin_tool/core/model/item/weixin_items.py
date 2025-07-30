from typing import Optional

from pydantic import BaseModel


class ServiceItem(BaseModel):
    """服务项"""
    # 服务标题
    title: Optional[str] = None


class LinkServiceItem(ServiceItem):
    """链接服务项"""
    # 链接url
    href: Optional[str] = None


class WeixinMpServiceItem(ServiceItem):
    """微信小程序服务项"""
    # 小程序 Appid
    app_id: Optional[str] = None
    # 页面路径
    path: Optional[str] = '/pages/index/index'

