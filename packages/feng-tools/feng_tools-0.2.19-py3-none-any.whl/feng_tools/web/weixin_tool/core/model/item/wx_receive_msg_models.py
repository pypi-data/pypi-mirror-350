from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class WeixinMsgBaseItem(BaseModel):
    """微信消息基本信息表"""
    id: Optional[int] = None
    # OpenID
    openid: Optional[str] = None
    # 开发者微信号
    to_user: Optional[str] = None
    # 发送方帐号（一个OpenID）
    from_user: Optional[str] = None
    # 消息创建时间 （整型）
    create_time: Optional[int] = None
    # 消息类型，文本为text, 图片为image，语音为voice，视频为video,小视频为shortvideo，地理位置为location，链接为link
    msg_type: Optional[str] = None
    # 消息id，64位整型
    msg_id: Optional[str] = None
    # 消息的数据ID（消息如果来自文章时才有）
    msg_data_id: Optional[str] = None
    # 多图文时第几篇文章，从1开始（消息如果来自文章时才有）
    idx: Optional[str] = None
    # 添加时间
    add_time: Optional[datetime] = None


class WeixinTextMsgItem(WeixinMsgBaseItem):
    """文本消息表"""
    # 文本消息内容
    msg_content: Optional[str] = None


class WeixinImageMsgItem(WeixinMsgBaseItem):
    """图片消息表"""
    # 图片链接（由系统生成）
    pic_url: Optional[str] = None
    # 图片消息媒体id，可以调用获取临时素材接口拉取数据。
    media_id: Optional[str] = None


class WeixinVoiceMsgItem(WeixinMsgBaseItem):
    """语音消息表"""
    # 语音消息媒体id，可以调用获取临时素材接口拉取数据。
    media_id: Optional[str] = None
    # 语音格式，如amr，speex等
    voice_format: Optional[str] = None
    # 语音识别结果，UTF8编码
    recognition: Optional[str] = None


class WeixinVideoMsgItem(WeixinMsgBaseItem):
    """视频消息表"""
    # 视频消息媒体id，可以调用获取临时素材接口拉取数据。
    media_id: Optional[str] = None
    # 视频消息缩略图的媒体id，可以调用多媒体文件下载接口拉取数据。
    thumb_media_id: Optional[str] = None


class WeixinLocationMsgItem(WeixinMsgBaseItem):
    """地理位置消息表"""
    # 地理位置纬度
    location_x: Optional[str] = None
    # 地理位置经度
    location_y: Optional[str] = None
    # 地图缩放大小
    scale: Optional[str] = None
    # 地理位置信息
    label: Optional[str] = None

    def __repr__(self):
        return self.label


class WeixinLinkMsgItem(WeixinMsgBaseItem):
    """链接消息表"""
    # 消息标题
    title: Optional[str] = None
    # 消息描述
    description: Optional[str] = None
    # 消息链接
    url: Optional[str] = None
