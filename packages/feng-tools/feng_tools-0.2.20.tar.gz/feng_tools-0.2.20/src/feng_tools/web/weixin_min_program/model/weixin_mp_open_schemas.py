from typing import Optional
from pydantic import BaseModel


class WxMpLoginInfo(BaseModel):
    """微信小程序登录信息"""
    # 小程序 appId
    mp_app_id: Optional[str] = None
    # 会话密钥
    session_key: Optional[str] = None
    # 用户在开放平台的唯一标识符，若当前小程序已绑定到微信开放平台账号下会返回，详见 UnionID 机制说明。
    union_id: Optional[str] = None
    # 用户唯一标识
    open_id: Optional[str] = None


class WxMpUserInfo(BaseModel):
    """微信小程序用户信息"""
    # 认证token
    token: Optional[str] = None
    nick_name: Optional[str] = None
    avatar_url: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    province: Optional[str] = None
    gender: Optional[int] = None
    language: Optional[str] = None


class WxMpUserBasicInfo(BaseModel):
    """微信小程序基础用户信息"""
    # 认证token
    token: Optional[str] = None
    nick_name: Optional[str] = None
    avatar_url: Optional[str] = None
