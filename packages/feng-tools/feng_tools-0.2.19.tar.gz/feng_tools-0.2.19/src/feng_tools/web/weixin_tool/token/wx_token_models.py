from datetime import datetime

from pydantic import BaseModel


class WeixinTokenInfo(BaseModel):
    """Token信息"""
    # 获取到的凭证
    access_token: str
    # 凭证有效时间，单位：秒
    expires_in: int
    # token获取的时间，用于判断token是否过期
    token_time: datetime