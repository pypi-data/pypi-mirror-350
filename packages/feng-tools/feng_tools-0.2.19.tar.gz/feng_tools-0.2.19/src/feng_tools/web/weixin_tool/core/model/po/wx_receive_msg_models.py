from sqlalchemy import Column, Integer, String

from feng_tools.orm.sqlalchemy.base_models import Model


class WeixinMsgBaseModel(Model):
    """微信消息基本信息表"""
    __abstract__ = True
    openid = Column(String(125), comment='OpenID', nullable=False)
    to_user = Column(String(250), comment='开发者微信号', nullable=False)
    from_user = Column(String(250), comment='发送方帐号（一个OpenID）', nullable=False)
    create_time = Column(Integer, comment='消息创建时间 （整型）', nullable=False)
    # 消息类型，文本为text, 图片为image，语音为voice，视频为video,小视频为shortvideo，地理位置为location，链接为link
    msg_type = Column(String(30), comment='消息类型', nullable=False)
    msg_id = Column(String(64), comment='消息id，64位整型', nullable=False)
    msg_data_id = Column(String(64), comment='消息的数据ID（消息如果来自文章时才有）', nullable=True)
    idx = Column(String(64), comment='多图文时第几篇文章，从1开始（消息如果来自文章时才有）', nullable=True)


class WeixinTextMsgPo(WeixinMsgBaseModel):
    """文本消息表"""
    __tablename__ = 'wx_text_msg'
    msg_content = Column(String(850), comment='文本消息内容', nullable=False)

    def __repr__(self):
        return self.msg_content[:50]


class WeixinImageMsgPo(WeixinMsgBaseModel):
    """图片消息表"""
    __tablename__ = 'wx_image_msg'
    pic_url = Column(String(500), comment='图片链接（由系统生成）', nullable=False)
    media_id = Column(String(250), comment='图片消息媒体id，可以调用获取临时素材接口拉取数据。', nullable=False)

    def __repr__(self):
        return self.pic_url


class WeixinVoiceMsgPo(WeixinMsgBaseModel):
    """语音消息表"""
    __tablename__ = 'wx_voice_msg'
    media_id = Column(String(250), comment='语音消息媒体id，可以调用获取临时素材接口拉取数据。', nullable=False)
    voice_format = Column(String(30), comment='语音格式，如amr，speex等', nullable=False)
    recognition = Column(String(500), comment='语音识别结果，UTF8编码', nullable=True)

    def __repr__(self):
        return self.media_id


class WeixinVideoMsgPo(WeixinMsgBaseModel):
    """视频消息表"""
    __tablename__ = 'wx_video_msg'
    media_id = Column(String(250), comment='视频消息媒体id，可以调用获取临时素材接口拉取数据。', nullable=False)
    thumb_media_id = Column(String(255), comment='视频消息缩略图的媒体id，可以调用多媒体文件下载接口拉取数据。',
                            nullable=False)

    def __repr__(self):
        return self.media_id


class WeixinLocationMsgPo(WeixinMsgBaseModel):
    """地理位置消息表"""
    __tablename__ = 'wx_location_msg'
    location_x = Column(String(20), comment='地理位置纬度', nullable=False)
    location_y = Column(String(20), comment='地理位置经度', nullable=False)
    scale = Column(String(10), comment='地图缩放大小', nullable=False)
    label = Column(String(150), comment='地理位置信息', nullable=False)

    def __repr__(self):
        return self.label


class WeixinLinkMsgPo(WeixinMsgBaseModel):
    """链接消息表"""
    __tablename__ = 'wx_link_msg'
    title = Column(String(100), comment='消息标题', nullable=False)
    description = Column(String(500), comment='消息描述', nullable=False)
    url = Column(String(500), comment='消息链接', nullable=False)

    def __repr__(self):
        return self.title
