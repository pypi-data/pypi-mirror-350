from feng_tools.web.weixin_tool.core.format.reply_msg.weixin_format_tool import format_xml_msg
from feng_tools.web.weixin_tool.core.format.reply_msg.weixin_models import WeixinReplyMsg, WeixinReplyNewsMsg


def format_msg(reply_msg: WeixinReplyMsg):
    """格式化回复消息"""
    if isinstance(reply_msg, WeixinReplyNewsMsg):
        articles_item_list = list()
        for article in reply_msg.articles:
            articles_item_list.append(format_xml_msg(article))
        setattr(reply_msg, 'articles_str', '\n'.join(articles_item_list))
    return format_xml_msg(reply_msg)



