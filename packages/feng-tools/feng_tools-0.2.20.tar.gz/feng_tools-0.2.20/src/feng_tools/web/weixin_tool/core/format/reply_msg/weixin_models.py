import os.path
from pathlib import Path
from typing import Union, List

from pydantic import BaseModel, Field

msg_xml_base = os.path.join(Path(__file__).parent, 'xml')


class WeixinReplyMsg(BaseModel):
    to_user: str = Field(title='接收方帐号（收到的OpenID）')
    from_user: str = Field(title='开发者微信号')
    create_time: int = Field(title='消息创建时间 （整型）')


class WeixinReplyTextMsg(WeixinReplyMsg):
    """文本消息"""
    _xml_file = os.path.join(msg_xml_base, 'text_msg.xml')
    content: str = Field(title='回复的消息内容',
                         description='回复的消息内容（换行：在 content 中能够换行，微信客户端就支持换行显示）')


class WeixinReplyImageMsg(WeixinReplyMsg):
    """图片消息"""
    _xml_file = os.path.join(msg_xml_base, 'image_msg.xml')
    media_id: str = Field(title='素材id', description='通过素材管理中的接口上传多媒体文件，得到的id。')


class WeixinReplyVoiceMsg(WeixinReplyMsg):
    """语音消息"""
    _xml_file = os.path.join(msg_xml_base, 'voice_msg.xml')
    media_id: str = Field(title='素材id', description='通过素材管理中的接口上传多媒体文件，得到的id。')


class WeixinReplyVideoMsg(WeixinReplyMsg):
    """视频消息"""
    _xml_file = os.path.join(msg_xml_base, 'video_msg.xml')
    media_id: str = Field(title='素材id', description='通过素材管理中的接口上传多媒体文件，得到的id。')
    title: Union[str, None] = Field(title='视频消息的标题')
    description: Union[str, None] = Field(title='视频消息的描述')


class WeixinReplyMusicMsg(WeixinReplyMsg):
    """音乐消息"""
    _xml_file = os.path.join(msg_xml_base, 'music_msg.xml')
    title: Union[str, None] = Field(title='音乐标题')
    description: Union[str, None] = Field(title='音乐描述')
    music_url: Union[str, None] = Field(title='音乐链接')
    hq_music_url: Union[str, None] = Field(title='高质量音乐链接', description='WIFI环境优先使用该链接播放音乐')
    thumb_media_id: str = Field(title='缩略图的媒体id', description='通过素材管理中的接口上传多媒体文件，得到的id')


class Article(BaseModel):
    _xml_file = os.path.join(msg_xml_base, 'news_msg_item.xml')
    title: str = Field(title='图文消息标题')
    description: str = Field(title='图文消息描述')
    pic_url: str = Field(title='图片链接', description='支持JPG、PNG格式，较好的效果为大图360*200，小图200*200')
    url: str = Field(title='点击图文消息跳转链接')


class WeixinReplyNewsMsg(WeixinReplyMsg):
    """图文消息"""
    _xml_file = os.path.join(msg_xml_base, 'news_msg.xml')
    article_count: int = Field(title='图文消息个数',
                               description='当用户发送文本、图片、语音、视频、图文、地理位置这六种消息时，开发者只能回复1条图文消息；其余场景最多可回复8条图文消息')
    articles: List[Article] = Field(title='图文消息信息', description='注意，如果图文数超过限制，则将只发限制内的条数')
