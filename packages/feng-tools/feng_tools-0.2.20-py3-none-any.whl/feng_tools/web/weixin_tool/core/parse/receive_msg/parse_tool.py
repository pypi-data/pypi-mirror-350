from feng_tools.base.re.re_tools import get_match_first_group


def parse_to_user(msg):
    return get_match_first_group(r'<ToUserName><!\[CDATA\[(.*?)\]\]></ToUserName>', msg)


def parse_from_user(msg):
    return get_match_first_group(r'<FromUserName><!\[CDATA\[(.*?)\]\]></FromUserName>', msg)


def parse_create_time(msg):
    return get_match_first_group(r'<CreateTime>(.*?)</CreateTime>', msg)


def parse_msg_type(msg):
    return get_match_first_group(r'<MsgType><!\[CDATA\[(.*?)\]\]></MsgType>', msg)


def parse_msg_content(msg):
    return get_match_first_group(r'<Content><!\[CDATA\[(.*?)\]\]></Content>', msg)


def parse_msg_id(msg):
    return get_match_first_group(r'<MsgId>(.*?)</MsgId>', msg)


def parse_msg_data_id(msg):
    return get_match_first_group(r'<MsgDataId>(.*?)</MsgDataId>', msg)


def parse_idx(msg):
    return get_match_first_group(r'<Idx>(.*?)</Idx>', msg)


def parse_pic_url(msg):
    return get_match_first_group(r'<PicUrl><!\[CDATA\[(.*?)\]\]></PicUrl>', msg)


def parse_media_id(msg):
    return get_match_first_group(r'<MediaId><!\[CDATA\[(.*?)\]\]></MediaId>', msg)


def parse_voice_format(msg):
    return get_match_first_group(r'<Format><!\[CDATA\[(.*?)\]\]></Format>', msg)


def parse_recognition(msg):
    return get_match_first_group(r'<Recognition><!\[CDATA\[(.*?)\]\]></Recognition>', msg)


def parse_thumb_media_id(msg):
    return get_match_first_group(r'<ThumbMediaId><!\[CDATA\[(.*?)\]\]></ThumbMediaId>', msg)


def parse_location_x(msg):
    return get_match_first_group(r'<Location_X>(.*?)</Location_X>', msg)


def parse_location_y(msg):
    return get_match_first_group(r'<Location_Y>(.*?)</Location_Y>', msg)


def parse_location_scale(msg):
    return get_match_first_group(r'<Scale>(.*?)</Scale>', msg)


def parse_location_label(msg):
    return get_match_first_group(r'<Label><!\[CDATA\[(.*?)\]\]></Label>', msg)


def parse_link_title(msg):
    return get_match_first_group(r'<Title><!\[CDATA\[(.*?)\]\]></Title>', msg)


def parse_link_description(msg):
    return get_match_first_group(r'<Description><!\[CDATA\[(.*?)\]\]></Description>', msg)


def parse_link_url(msg):
    return get_match_first_group(r'<Url><!\[CDATA\[(.*?)\]\]></Url>', msg)
