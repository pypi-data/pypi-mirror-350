from typing import Optional

from pydantic import BaseModel


class Jscode2sessionResult(BaseModel):
    # 会话密钥
    session_key: Optional[str] = None
    # 用户在开放平台的唯一标识符，若当前小程序已绑定到微信开放平台账号下会返回，详见 UnionID 机制说明。
    unionid: Optional[str] = None
    # 用户唯一标识
    openid: Optional[str] = None
    # 错误码:  【40029】js_code无效  【45011】API 调用太频繁，请稍候再试 【40226】 高风险等级用户，小程序登录拦截 。 【-1】系统繁忙，此时请开发者稍候再试
    errcode: Optional[int] = None
    # 错误信息
    errmsg: Optional[str] = None


class TokenResult(BaseModel):
    # 获取到的凭证
    access_token: Optional[str] = None
    # 凭证有效时间，单位：秒。目前是7200秒之内的值。
    expires_in: Optional[int] = None


class CheckResult(BaseModel):
    # 错误码, 0: ok   87009: 无效的签名
    errcode: Optional[int] = None
    # 错误信息
    errmsg: Optional[str] = None


class GenerateUrlLink(BaseModel):
    # 错误码, 0: ok   87009: 无效的签名
    errcode: Optional[int] = None
    # 错误信息
    errmsg: Optional[str] = None
    # 生成的小程序 URL Link
    url_link: Optional[str] = None


class WxUserInfo(BaseModel):
    nickName: Optional[str] = None
    avatarUrl: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    province: Optional[str] = None
    gender: Optional[int] = None
    is_demote: Optional[bool] = None
    language: Optional[str] = None


class WxUserProfile(BaseModel):
    encryptedData: Optional[str] = None
    iv: Optional[str] = None
    rawData: Optional[str] = None
    signature: Optional[str] = None
    userInfo: Optional[WxUserInfo] = None
    app_id: str
    token: str


class WxUserBasicInfo(BaseModel):
    app_id: str
    token: str
    nickName: Optional[str] = None
    avatarUrl: Optional[str] = None
