import hashlib
from typing import Any

from fastapi import Query
from starlette.requests import Request

from feng_tools.web.weixin_tool import weixin_settings
from feng_tools.web.weixin_tool.core.model.item.wx_receive_event_models import WeixinEventItem
from feng_tools.web.weixin_tool.core.model.item.wx_receive_msg_models import WeixinImageMsgItem, WeixinTextMsgItem, \
    WeixinVoiceMsgItem, \
    WeixinVideoMsgItem, WeixinLocationMsgItem, WeixinLinkMsgItem
from feng_tools.web.weixin_tool.core.parse import parse_receive
from feng_tools.web.weixin_tool.core.weixin_enums import WeixinConfigKeyEnum


async def convert_params(request: Request, signature: str = Query(title='微信加密签名'),
                         timestamp: str = Query(title='时间戳'),
                         nonce: str = Query(title='随机数'),
                         openid: str = Query(title='OpenID')) -> tuple[
    WeixinTextMsgItem | WeixinImageMsgItem | WeixinVoiceMsgItem | WeixinVideoMsgItem | WeixinLocationMsgItem | WeixinLinkMsgItem | WeixinEventItem, bytes,
    dict[str, Any]]:
    """格式化参数"""
    if signature == hashlib.sha1(
            ''.join(sorted([weixin_settings.get_config(WeixinConfigKeyEnum.weixin_token), timestamp, nonce])).encode(
                'utf-8')).hexdigest():
        # 证明请求来自微信服务器
        if request.headers['content-type'] == 'text/xml':
            body = await request.body()
            query_params = {
                'signature': signature,
                'timestamp': timestamp,
                'nonce': nonce,
                'openid': openid
            }
            return parse_receive.parse(openid, body), body, query_params
