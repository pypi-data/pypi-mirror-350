from typing import Callable

from feng_tools.web.weixin_tool.core.weixin_enums import WeixinConfigKeyEnum, WeixinConfigItem

# 微信配置
__WEIXIN_CONFIG_CACHE__ = dict()


def init_config(weixin_config_item: WeixinConfigItem):
    init_weixin_config(weixin_config_item)


def init_weixin_config(weixin_config_item: WeixinConfigItem):
    """初始化微信公众号配置"""
    _set_config(WeixinConfigKeyEnum.weixin_app_id, weixin_config_item.weixin_app_id)
    _set_config(WeixinConfigKeyEnum.weixin_app_secret, weixin_config_item.weixin_app_secret)
    _set_config(WeixinConfigKeyEnum.weixin_token, weixin_config_item.weixin_token)
    _set_config(WeixinConfigKeyEnum.weixin_encoding_aes_key, weixin_config_item.weixin_encoding_aes_key)
    _set_config(WeixinConfigKeyEnum.weixin_msg_callback, weixin_config_item.weixin_msg_callback)
    _set_config(WeixinConfigKeyEnum.weixin_token_file, weixin_config_item.weixin_token_file)


def _set_config(config_key: WeixinConfigKeyEnum, config_value: str | Callable):
    """设置配置"""
    __WEIXIN_CONFIG_CACHE__[config_key] = config_value


def get_config(config_key: WeixinConfigKeyEnum) -> str | Callable:
    """获取配置"""
    return __WEIXIN_CONFIG_CACHE__.get(config_key)
