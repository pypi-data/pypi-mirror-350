"""
微信小程序模型
"""

from sqlalchemy import Column, String

from feng_tools.common.enums import IntegerEnum, GenderTypeEnum
from feng_tools.orm.sqlalchemy.base_models import Model


class WeixinMpAppInfoPo(Model):
    """微信小程序APP信息"""
    __tablename__ = "weixin_mp_app_info"
    app_id = Column(String(255), comment='小程序appId', unique=False, nullable=True)
    app_secret = Column(String(255), comment='小程序appSecret', unique=False, nullable=True)


class WeixinMpUserInfoPo(Model):
    """微信小程序用户信息"""
    __tablename__ = "weixin_mp_user_info"
    app_id = Column(String(255), comment='小程序appId', unique=False, nullable=True)
    open_id = Column(String(255), comment='用户唯一标识', unique=False, nullable=True)
    union_id = Column(String(255), comment='用户在开放平台的唯一标识符', unique=False, nullable=True)
    session_key = Column(String(255), comment='会话密钥', unique=False, nullable=True)
    nick_name = Column(String(255), comment='昵称', unique=False, nullable=True)
    avatar_url = Column(String(255), comment='头像url', unique=False, nullable=True)
    country = Column(String(255), comment='用户所在国家', unique=False, nullable=True)
    province = Column(String(255), comment='用户所在省份', unique=False, nullable=True)
    city = Column(String(255), comment='用户所在城市', unique=False, nullable=True)
    gender = Column(IntegerEnum(GenderTypeEnum), comment='性别', unique=False, nullable=True)
    language = Column(String(255), comment='用户的语言，简体中文为 zh_CN', unique=False, nullable=True)
    token = Column(String(255), comment='Token值', unique=False, nullable=True)