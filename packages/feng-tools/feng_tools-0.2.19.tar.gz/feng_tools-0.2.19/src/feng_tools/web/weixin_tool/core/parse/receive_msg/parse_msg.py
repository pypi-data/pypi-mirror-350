from feng_tools.web.weixin_tool.core.model.item.wx_receive_msg_models import WeixinTextMsgItem, WeixinImageMsgItem, WeixinVoiceMsgItem, \
    WeixinVideoMsgItem, WeixinLocationMsgItem, WeixinLinkMsgItem
from feng_tools.web.weixin_tool.core.parse.receive_msg.parse_tool import parse_to_user, parse_from_user, parse_create_time, parse_msg_type, \
    parse_msg_content, parse_pic_url, parse_media_id, parse_msg_id, parse_msg_data_id, parse_idx, parse_voice_format, \
    parse_recognition, parse_thumb_media_id, parse_location_x, parse_location_y, parse_location_label, \
    parse_location_scale, parse_link_title, parse_link_description, parse_link_url


def parse_text_msg(openid, msg) -> WeixinTextMsgItem:
    """转换文本消息"""
    return WeixinTextMsgItem(
        openid=openid,
        to_user=parse_to_user(msg),
        from_user=parse_from_user(msg),
        create_time=parse_create_time(msg),
        msg_type=parse_msg_type(msg),
        msg_content=parse_msg_content(msg),
        msg_id=parse_msg_id(msg),
        msg_data_id=parse_msg_data_id(msg),
        idx=parse_idx(msg),
    )


def parse_image_msg(openid, msg) -> WeixinImageMsgItem:
    """转换图片消息"""
    return WeixinImageMsgItem(
        openid=openid,
        to_user=parse_to_user(msg),
        from_user=parse_from_user(msg),
        create_time=parse_create_time(msg),
        msg_type=parse_msg_type(msg),
        pic_url=parse_pic_url(msg),
        media_id=parse_media_id(msg),
        msg_id=parse_msg_id(msg),
        msg_data_id=parse_msg_data_id(msg),
        idx=parse_idx(msg),
    )


def parse_voice_msg(openid, msg) -> WeixinVoiceMsgItem:
    """转换语音消息"""
    return WeixinVoiceMsgItem(
        openid=openid,
        to_user=parse_to_user(msg),
        from_user=parse_from_user(msg),
        create_time=parse_create_time(msg),
        msg_type=parse_msg_type(msg),
        media_id=parse_media_id(msg),
        voice_format=parse_voice_format(msg),
        recognition=parse_recognition(msg),
        msg_id=parse_msg_id(msg),
        msg_data_id=parse_msg_data_id(msg),
        idx=parse_idx(msg),
    )


def parse_video_msg(openid, msg) -> WeixinVideoMsgItem:
    """转换视频消息"""
    return WeixinVideoMsgItem(
        openid=openid,
        to_user=parse_to_user(msg),
        from_user=parse_from_user(msg),
        create_time=parse_create_time(msg),
        msg_type=parse_msg_type(msg),
        media_id=parse_media_id(msg),
        thumb_media_id=parse_thumb_media_id(msg),
        msg_id=parse_msg_id(msg),
        msg_data_id=parse_msg_data_id(msg),
        idx=parse_idx(msg),
    )


def parse_location_msg(openid, msg) -> WeixinLocationMsgItem:
    """转换地理消息"""
    return WeixinLocationMsgItem(
        openid=openid,
        to_user=parse_to_user(msg),
        from_user=parse_from_user(msg),
        create_time=parse_create_time(msg),
        msg_type=parse_msg_type(msg),
        location_x=parse_location_x(msg),
        location_y=parse_location_y(msg),
        scale=parse_location_scale(msg),
        label=parse_location_label(msg),
        msg_id=parse_msg_id(msg),
        msg_data_id=parse_msg_data_id(msg),
        idx=parse_idx(msg),
    )


def parse_link_msg(openid, msg) -> WeixinLinkMsgItem:
    """转换链接消息"""
    return WeixinLinkMsgItem(
        openid=openid,
        to_user=parse_to_user(msg),
        from_user=parse_from_user(msg),
        create_time=parse_create_time(msg),
        msg_type=parse_msg_type(msg),
        title=parse_link_title(msg),
        description=parse_link_description(msg),
        url=parse_link_url(msg),
        msg_id=parse_msg_id(msg),
        msg_data_id=parse_msg_data_id(msg),
        idx=parse_idx(msg),
    )
