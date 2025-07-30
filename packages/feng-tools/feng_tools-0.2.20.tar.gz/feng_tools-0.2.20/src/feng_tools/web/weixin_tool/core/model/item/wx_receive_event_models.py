from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WeixinEventItem(BaseModel):
    """微信事件基本信息"""
    id: Optional[int] = None
    # OpenID
    openid: Optional[str] = None
    # 开发者微信号
    to_user: Optional[str] = None
    # 发送方帐号（一个OpenID）
    from_user: Optional[str] = None
    # 消息创建时间 （整型）
    create_time: Optional[int] = None
    # 消息类型，event
    msg_type: Optional[str] = None
    # 添加时间
    add_time: Optional[datetime] = None


class WeixinSubscribeEventItem(WeixinEventItem):
    """关注/取消关注事件表"""
    # 事件类型，subscribe(订阅)、unsubscribe(取消订阅)
    event: Optional[str] = None


class WeixinQrEventItem(WeixinEventItem):
    """扫描带参数二维码事件"""
    # 事件类型，subscribe
    event: Optional[str] = None
    # 事件 KEY 值，qrscene_为前缀，后面为二维码的参数值
    event_key: Optional[str] = None
    # 二维码的ticket，可用来换取二维码图片
    ticket: Optional[str] = None


class WeixinScanEventItem(WeixinEventItem):
    """用户已关注时的事件推送"""
    # 事件类型，SCAN
    event: Optional[str] = None
    # 事件 KEY 值，是一个32位无符号整数，即创建二维码时的二维码scene_id
    event_key: Optional[str] = None
    # 二维码的ticket，可用来换取二维码图片
    ticket: Optional[str] = None

    def __repr__(self):
        return self.event_key


class WeixinLocationEventItem(WeixinEventItem):
    """上报地理位置事件"""
    # 事件类型，LOCATION
    event: Optional[str] = None
    # 地理位置纬度
    location_x: Optional[str] = None
    # 地理位置经度
    location_y: Optional[str] = None
    # 地理位置精度
    precision: Optional[str] = None

    def __repr__(self):
        return self.location_x, self.location_y


class WeixinMenuEventItem(WeixinEventItem):
    """点击自定义菜单事件"""
    # 事件类型，CLICK:点击菜单拉取消息, VIEW:点击菜单跳转链接时的事件推送
    event: Optional[str] = None
    # 事件 KEY 值，与自定义菜单接口中KEY值对应 或 设置的跳转URL
    event_key: Optional[str] = None

