from feng_tools.web.weixin_tool.core.model.item.wx_receive_event_models import WeixinSubscribeEventItem, \
    WeixinQrEventItem, WeixinScanEventItem, WeixinLocationEventItem, WeixinMenuEventItem, WeixinEventItem
from feng_tools.web.weixin_tool.core.parse.receive_event.parse_tool import parse_event, parse_event_key, parse_ticket, \
    parse_location_precision, parse_location_x, parse_location_y
from feng_tools.web.weixin_tool.core.parse.receive_msg.parse_tool import parse_to_user, parse_from_user, \
    parse_create_time, parse_msg_type


def parse_subscribe_event(openid, msg) -> WeixinSubscribeEventItem:
    """转换订阅/取消订阅事件表"""
    return WeixinSubscribeEventItem(
        openid=openid,
        to_user=parse_to_user(msg),
        from_user=parse_from_user(msg),
        create_time=parse_create_time(msg),
        msg_type=parse_msg_type(msg),
        event=parse_event(msg)
    )


def parse_qr_event(openid, msg) -> WeixinQrEventItem:
    """扫描带参数二维码事件"""
    return WeixinQrEventItem(
        openid=openid,
        to_user=parse_to_user(msg),
        from_user=parse_from_user(msg),
        create_time=parse_create_time(msg),
        msg_type=parse_msg_type(msg),
        event=parse_event(msg),
        event_key=parse_event_key(msg),
        ticket=parse_ticket(msg),
    )


def parse_scan_event(openid, msg) -> WeixinScanEventItem:
    """用户已关注时的事件推送"""
    return WeixinScanEventItem(
        openid=openid,
        to_user=parse_to_user(msg),
        from_user=parse_from_user(msg),
        create_time=parse_create_time(msg),
        msg_type=parse_msg_type(msg),
        event=parse_event(msg),
        event_key=parse_event_key(msg),
        ticket=parse_ticket(msg),
    )


def parse_location_event(openid, msg) -> WeixinLocationEventItem:
    """上报地理位置事件"""
    return WeixinLocationEventItem(
        openid=openid,
        to_user=parse_to_user(msg),
        from_user=parse_from_user(msg),
        create_time=parse_create_time(msg),
        msg_type=parse_msg_type(msg),
        event=parse_event(msg),
        location_x=parse_location_x(msg),
        location_y=parse_location_y(msg),
        precision=parse_location_precision(msg),
    )


def parse_menu_event(openid, msg) -> WeixinMenuEventItem:
    """点击自定义菜单事件"""
    return WeixinMenuEventItem(
        openid=openid,
        to_user=parse_to_user(msg),
        from_user=parse_from_user(msg),
        create_time=parse_create_time(msg),
        msg_type=parse_msg_type(msg),
        event=parse_event(msg),
        event_key=parse_event_key(msg),
    )


def parse(openid, msg) -> WeixinEventItem:
    """转换事件"""
    event = parse_event(msg)
    if event == 'unsubscribe':
        return parse_subscribe_event(openid, msg)
    if event == 'subscribe':
        event_key = parse_event_key(msg)
        if not event_key:
            return parse_subscribe_event(openid, msg)
        if event_key.startswith('qrscene_'):
            return parse_qr_event(openid, msg)
    if event == 'SCAN':
        return parse_scan_event(openid, msg)
    if event == 'LOCATION':
        return parse_location_event(openid, msg)
    if event == 'CLICK' or event == 'VIEW':
        return parse_menu_event(openid, msg)
