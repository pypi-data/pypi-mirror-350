"""
Access token工具
"""
import json
import os.path
from datetime import datetime

import requests

from feng_tools.file import file_tools
from feng_tools.web.weixin_tool import weixin_settings
from feng_tools.web.weixin_tool.core.weixin_enums import WeixinConfigKeyEnum
from feng_tools.web.weixin_tool.token.wx_token_models import WeixinTokenInfo


def _is_need_refresh(token_info: WeixinTokenInfo):
    """
    判断token是否需要刷新
    :param token_info:
    :return: 是否需要刷新，默认是False
    """
    space_time = datetime.now() - token_info.token_time
    space_seconds = space_time.total_seconds()
    if space_seconds - token_info.expires_in > 100:
        return True
    return False


def _save_token(access_token_file: str, token_info: WeixinTokenInfo):
    """保存token到本地"""
    file_tools.save_file(json.dumps(token_info.model_dump(mode='json')).encode('utf-8'),
                         access_token_file, binary_flag=True)


def refresh_access_token(app_id: str, app_secret: str) -> WeixinTokenInfo:
    """刷新token"""
    start_time = datetime.now()
    resp = requests.get(
        f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}')
    if resp.status_code == 200:
        resp_json = resp.json()
        if resp_json.get('errcode'):
            print(f"[{resp_json.get('errcode')}]{resp_json.get('errmsg')}")
        else:
            return WeixinTokenInfo(access_token=resp_json.get('access_token'),
                                   expires_in=resp_json.get('expires_in'),
                                   token_time=start_time)


def get_access_token(app_id: str, app_secret: str) -> str:
    """获取token"""
    access_token_file = weixin_settings.get_config(WeixinConfigKeyEnum.weixin_token_file)
    if os.path.exists(access_token_file):
        # token文件转换为token
        token_info_bytes = file_tools.read_file(access_token_file, binary_flag=True)
        token_info = WeixinTokenInfo.model_validate_json(token_info_bytes)
        # 判断已有的token是否需要刷新
        if _is_need_refresh(token_info) or not token_info.access_token:
            # 1、刷新token
            token_info = refresh_access_token(app_id=app_id, app_secret=app_secret)
            if token_info:
                # 2、保存刷新后的token
                _save_token(access_token_file, token_info)
                return token_info.access_token
        else:
            return token_info.access_token
    else:
        # 1、刷新token
        token_info = refresh_access_token(app_id=app_id, app_secret=app_secret)
        if token_info:
            # 2、保存刷新后的token
            _save_token(access_token_file, token_info)
            return token_info.access_token
