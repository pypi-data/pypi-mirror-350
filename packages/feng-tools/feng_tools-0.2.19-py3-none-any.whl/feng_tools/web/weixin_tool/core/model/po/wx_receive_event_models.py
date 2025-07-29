from sqlalchemy import Column, Integer, String

from feng_tools.orm.sqlalchemy.base_models import Model


class WeixinEventModel(Model):
    """微信事件基本信息表"""
    __abstract__ = True
    openid = Column(String(125), comment='OpenID', nullable=False)
    to_user = Column(String(250), comment='开发者微信号', nullable=False)
    from_user = Column(String(250), comment='发送方帐号（一个OpenID）', nullable=False)
    create_time = Column(Integer, comment='消息创建时间 （整型）', nullable=False)
    # 消息类型，event
    msg_type = Column(String(30), comment='消息类型，event', nullable=False)


class WeixinSubscribeEventPo(WeixinEventModel):
    """订阅/取消订阅事件表"""
    __tablename__ = 'wx_subscribe_event'
    event = Column(String(20), comment='事件类型，subscribe(订阅)、unsubscribe(取消订阅)', nullable=False)

    def __repr__(self):
        return self.event


class WeixinQrEventPo(WeixinEventModel):
    """扫描带参数二维码事件"""
    __tablename__ = 'wx_qr_event'
    event = Column(String(20), comment='事件类型，subscribe', nullable=False)
    event_key = Column(String(500), comment='事件 KEY 值，qrscene_为前缀，后面为二维码的参数值', nullable=False)
    ticket = Column(String(250), comment='二维码的ticket，可用来换取二维码图片', nullable=False)

    def __repr__(self):
        return self.event_key


class WeixinScanEventPo(WeixinEventModel):
    """用户已关注时的事件推送"""
    __tablename__ = 'wx_scan_event'
    event = Column(String(20), comment='事件类型，SCAN', nullable=False)
    event_key = Column(String(64), comment='事件 KEY 值，是一个32位无符号整数，即创建二维码时的二维码scene_id',
                       nullable=False)
    ticket = Column(String(250), comment='二维码的ticket，可用来换取二维码图片', nullable=False)

    def __repr__(self):
        return self.event_key


class WeixinLocationEventPo(WeixinEventModel):
    """上报地理位置事件"""
    __tablename__ = 'wx_location_event'
    event = Column(String(20), comment='事件类型，LOCATION', nullable=False)
    location_x = Column(String(20), comment='地理位置纬度', nullable=False)
    location_y = Column(String(20), comment='地理位置经度', nullable=False)
    precision = Column(String(20), comment='地理位置精度', nullable=False)

    def __repr__(self):
        return self.location_x, self.location_y


class WeixinMenuEventPo(WeixinEventModel):
    """点击自定义菜单事件"""
    __tablename__ = 'wx_menu_event'
    event = Column(String(20), comment='事件类型，CLICK:点击菜单拉取消息, VIEW:点击菜单跳转链接时的事件推送',
                   nullable=False)
    event_key = Column(String(255), comment='事件 KEY 值，与自定义菜单接口中KEY值对应 或 设置的跳转URL', nullable=False)

    def __repr__(self):
        return self.event_key
