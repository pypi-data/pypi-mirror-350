import json

import requests

from feng_tools.web.weixin_tool import weixin_settings
from feng_tools.web.weixin_tool.core.weixin_enums import WeixinConfigKeyEnum
from feng_tools.web.weixin_tool.custom_menu.wx_custome_menu_models import WeixinButtonItem, WeixinViewButtonItem, \
    WeixinMiniProgramButtonItem, WeixinScanWaitButtonItem
from feng_tools.web.weixin_tool.token import wx_token_tools


def create_menu(access_token: str, menu_list: list):
    menu_dict_list = [tmp.model_dump() for tmp in menu_list]
    json_data = '{ "button": ' + json.dumps(menu_dict_list, ensure_ascii=False) + ' }'
    resp = requests.post(url=f'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={access_token}',
                         json=json_data)
    if resp.status_code == 200:
        resp_json = resp.json()
        if resp_json.get('errcode'):
            print(f"[{resp_json.get('errcode')}]{resp_json.get('errmsg')}")


if __name__ == '__main__':
    menu_list = []
    menu_list.append(WeixinButtonItem(name='优秀网站',
                                      sub_button=[
                                          WeixinViewButtonItem(name='阿锋书屋', url='https://www.afengbook.com')]))

    menu_list.append(WeixinButtonItem(name='小程序',
                                      sub_button=[WeixinMiniProgramButtonItem(name='土味情话', appid='',
                                                                              pagepath='pages/home/index')]))
    menu_list.append(WeixinScanWaitButtonItem(name='扫一扫', key='scancode_10001'))
    access_token = wx_token_tools.get_access_token(weixin_settings.get_config(WeixinConfigKeyEnum.weixin_app_id),
                                                   weixin_settings.get_config(WeixinConfigKeyEnum.weixin_app_secret))
    create_menu(access_token, menu_list)
