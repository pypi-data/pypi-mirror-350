import math
import time

from feng_tools.web.weixin_tool.core.format import weixin_format_replay
from feng_tools.web.weixin_tool.core.format.reply_msg.weixin_models import WeixinReplyTextMsg
from feng_tools.web.weixin_tool.core.response import XmlResponse


def reply_text(source_msg_model, text_content: str) -> XmlResponse:
    """响应文本内容"""
    crate_time = math.floor(time.time())
    reply_msg = WeixinReplyTextMsg(to_user=source_msg_model.from_user, from_user=source_msg_model.to_user,
                                   create_time=crate_time,
                                   content=text_content)
    return XmlResponse(weixin_format_replay.format_msg(reply_msg))

