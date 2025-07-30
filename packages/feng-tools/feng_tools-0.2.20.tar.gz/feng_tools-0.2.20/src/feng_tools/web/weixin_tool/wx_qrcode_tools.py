from typing import Literal
import requests


from feng_tools.web.weixin_tool.token import wx_token_tools


# 永久二维码
def create_qrcode(access_token: str, scene_value: str | int,
                  action_name: Literal['QR_SCENE', 'QR_STR_SCENE', 'QR_LIMIT_SCENE'] = 'QR_LIMIT_STR_SCENE',
                  hava_expire: bool = False, expire_seconds: int = 2592000):
    """
    创建二维码
    :param access_token:
    :param scene_value: 场景值ID
        - 整型参数值: 临时二维码时为32位非0整型，永久二维码时最大值为100000（目前参数只支持1--100000）
        - 字符串参数值: 字符串类型，长度限制为1到64
    :param action_name:
        - QR_SCENE为临时的整型参数值
        - QR_STR_SCENE为临时的字符串参数值
        - QR_LIMIT_SCENE为永久的整型参数值
        - QR_LIMIT_STR_SCENE为永久的字符串参数值
    :param hava_expire: 是否有过期时间
    :param expire_seconds: 二维码有效时间，以秒为单位。 最大不超过2592000（即30天），此字段如果不填，则默认有效期为60秒。
    :return:
    """
    params = dict()
    if hava_expire:
        params['expire_seconds'] = expire_seconds
    params['action_name'] = action_name
    if action_name == 'QR_SCENE' or action_name == 'QR_LIMIT_SCENE':
        params['action_info'] = {
            'scene_id': scene_value
        }
    else:
        params['action_info'] = {
            'scene_str': str(scene_value)
        }

    resp = requests.post(f'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={access_token}',
                         params={"expire_seconds": expire_seconds,
                                 "action_name": "QR_SCENE",
                                 "action_info": {"scene": {"scene_id": 123}}})
    resp.encoding = 'utf-8'
    json_resp = resp.json()
    print(resp.text)
    print()


if __name__ == '__main__':
    # access_token = wx_token_tools.get_access_token(app_id=settings_tools.get_config('weixin.app_id'),
    #                                                app_secret=settings_tools.get_config('weixin.app_secret'))
    #
    # print('access_token:', access_token)
    pass
