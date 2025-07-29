from typing import Callable, Any

# 微信小程序配置
__WEIXIN_MP_CONFIG_CACHE__ = dict()

from feng_tools.web.weixin_min_program.model.weixin_mp_config_schemas import WeixinMpConfigKeyEnum, WeixinMpConfigItem


def init_mp_config(mp_app_id: str, mp_config_item: WeixinMpConfigItem):
    """初始化微信小程序配置"""
    _set_config(mp_app_id, WeixinMpConfigKeyEnum.mp_app_id, mp_config_item.mp_app_id)
    _set_config(mp_app_id, WeixinMpConfigKeyEnum.mp_app_secret, mp_config_item.mp_app_secret)
    _set_config(mp_app_id, WeixinMpConfigKeyEnum.mp_login_callback, mp_config_item.mp_login_callback)
    _set_config(mp_app_id, WeixinMpConfigKeyEnum.mp_get_login_info_callback, mp_config_item.mp_get_login_info_callback)
    _set_config(mp_app_id, WeixinMpConfigKeyEnum.mp_save_userinfo_callback, mp_config_item.mp_save_userinfo_callback)
    _set_config(mp_app_id, WeixinMpConfigKeyEnum.mp_save_user_basic_info_callback,
                mp_config_item.mp_save_user_basic_info_callback)


def _set_config(mp_app_id: str, config_key: WeixinMpConfigKeyEnum, config_value: str | Callable):
    """设置配置"""
    if not __WEIXIN_MP_CONFIG_CACHE__.get(mp_app_id):
        __WEIXIN_MP_CONFIG_CACHE__[mp_app_id] = dict()
    __WEIXIN_MP_CONFIG_CACHE__[mp_app_id][config_key] = config_value


def get_config(mp_app_id: str, config_key: WeixinMpConfigKeyEnum) -> Any | None:
    """获取配置"""
    if __WEIXIN_MP_CONFIG_CACHE__.get(mp_app_id):
        return __WEIXIN_MP_CONFIG_CACHE__.get(mp_app_id).get(config_key)
    return None
