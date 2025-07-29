from enum import Enum
from typing import Callable, Optional

from pydantic import BaseModel

from feng_tools.web.weixin_min_program.model.weixin_mp_open_schemas import WxMpLoginInfo, WxMpUserInfo, WxMpUserBasicInfo


class WeixinMpConfigItem(BaseModel):
    """微信小程序配置"""
    # 小程序 appId
    mp_app_id: Optional[str] = None
    # 小程序 appSecret
    mp_app_secret: Optional[str] = None
    # 小程序登录Callback
    mp_login_callback: Optional[Callable[[WxMpLoginInfo], str]] = None
    # 小程序获取登录信息Callback
    mp_get_login_info_callback: Optional[Callable[[str], WxMpLoginInfo]] = None
    #  小程序保存用户信息Callback
    mp_save_userinfo_callback: Optional[Callable[[WxMpUserInfo], dict]] = None
    #  小程序保存用户信息Callback
    mp_save_user_basic_info_callback: Optional[Callable[[WxMpUserBasicInfo], dict]] = None


class WeixinMpConfigKeyEnum(Enum):
    """微信配置枚举"""
    # 小程序 appId
    mp_app_id = 'mp_app_id'
    # 小程序 appSecret
    mp_app_secret = 'mp_app_secret'
    # 小程序登录Callback
    mp_login_callback = 'mp_login_callback'
    # 小程序获取登录信息Callback
    mp_get_login_info_callback = 'mp_get_login_info_callback'
    # 小程序保存用户信息Callback
    mp_save_userinfo_callback = 'mp_save_userinfo_callback'
    # 小程序保存用户基础信息Callback
    mp_save_user_basic_info_callback = 'mp_save_user_basic_info_callback'
