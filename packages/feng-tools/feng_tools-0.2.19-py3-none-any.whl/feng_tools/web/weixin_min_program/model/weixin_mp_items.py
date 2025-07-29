from typing import Optional

from pydantic import BaseModel, ConfigDict


class MpUserInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    nick_name: Optional[str] = None
    avatar_url: Optional[str] = None
    country: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    gender: Optional[int] = None
    language: Optional[str] = None

