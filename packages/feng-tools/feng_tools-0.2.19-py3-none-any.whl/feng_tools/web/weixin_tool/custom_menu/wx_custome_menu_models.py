from typing import Optional

from pydantic import BaseModel


class WeixinButtonItem(BaseModel):
    """根菜单项（用于具有子菜单的菜单项）"""
    name: str
    sub_button: list


class WeixinClickButtonItem(BaseModel):
    """click：点击推事件用户点击click类型按钮后，微信服务器会通过消息接口推送消息类型为event的结构给开发者（参考消息接口指南），并且带上按钮中开发者填写的key值，开发者可以通过自定义的key值与用户进行交互；
    """
    type: str = 'click'
    name: str
    key: str


class WeixinViewButtonItem(BaseModel):
    """view:跳转URL用户点击view类型按钮后，微信客户端将会打开开发者在按钮中填写的网页URL，可与网页授权获取用户基本信息接口结合，获得用户基本信息。
    """
    type: str = 'view'
    name: str
    url: str


class WeixinMiniProgramButtonItem(BaseModel):
    """miniprogram:用户点击miniprogram类型按钮后，微信客户端将会打开开发者在按钮中填写微信小程序页面。
    """
    type: str = 'miniprogram'
    name: str
    url: str = 'http://mp.weixin.qq.com'
    # 小程序的appid（仅认证公众号可配置）
    appid: str
    # 小程序的页面路径
    pagepath: str


class WeixinScanPushButtonItem(BaseModel):
    """scancode_push: 扫码推事件用户点击按钮后，微信客户端将调起扫一扫工具，完成扫码操作后显示扫描结果（如果是URL，将进入URL），且会将扫码的结果传给开发者，开发者可以下发消息。
    """
    type: str = 'scancode_push'
    name: str
    key: str
    sub_button: Optional[list] = []


class WeixinScanWaitButtonItem(BaseModel):
    """scancode_waitmsg：扫码推事件且弹出“消息接收中”提示框用户点击按钮后，微信客户端将调起扫一扫工具，完成扫码操作后，将扫码的结果传给开发者，同时收起扫一扫工具，然后弹出“消息接收中”提示框，随后可能会收到开发者下发的消息。
    """
    type: str = 'scancode_waitmsg'
    name: str
    key: str
    sub_button: Optional[list] = []


class WeixinPhotoButtonItem(BaseModel):
    """pic_sysphoto：弹出系统拍照发图用户点击按钮后，微信客户端将调起系统相机，完成拍照操作后，会将拍摄的相片发送给开发者，并推送事件给开发者，同时收起系统相机，随后可能会收到开发者下发的消息。
    """
    type: str = 'pic_sysphoto'
    name: str
    key: str
    sub_button: Optional[list] = []


class WeixinPicButtonItem(BaseModel):
    """pic_photo_or_album：弹出拍照或者相册发图用户点击按钮后，微信客户端将弹出选择器供用户选择“拍照”或者“从手机相册选择”。用户选择后即走其他两种流程。
    """
    type: str = 'pic_photo_or_album'
    name: str
    key: str
    sub_button: Optional[list] = []


class WeixinPicWxButtonItem(BaseModel):
    """pic_weixin：弹出微信相册发图器用户点击按钮后，微信客户端将调起微信相册，完成选择操作后，将选择的相片发送给开发者的服务器，并推送事件给开发者，同时收起相册，随后可能会收到开发者下发的消息。
    """
    type: str = 'pic_weixin'
    name: str
    key: str
    sub_button: Optional[list] = []


class WeixinLocationButtonItem(BaseModel):
    """location_select：弹出地理位置选择器用户点击按钮后，微信客户端将调起地理位置选择工具，完成选择操作后，将选择的地理位置发送给开发者的服务器，同时收起位置选择工具，随后可能会收到开发者下发的消息。
    """
    type: str = 'location_select'
    name: str
    key: str


class WeixinMediaButtonItem(BaseModel):
    """media_id：下发消息（除文本消息）用户点击media_id类型按钮后，微信服务器会将开发者填写的永久素材id对应的素材下发给用户，永久素材类型可以是图片、音频、视频 、图文消息。请注意：永久素材id必须是在“素材管理/新增永久素材”接口上传后获得的合法id。
    """
    type: str = 'media_id'
    name: str
    media_id: str


class WeixinArticleButtonItem(BaseModel):
    """article_id：用户点击 article_id 类型按钮后，微信客户端将会以卡片形式，下发开发者在按钮中填写的图文消息
    """
    type: str = 'article_id'
    name: str
    article_id: str


class WeixinArticleViewButtonItem(BaseModel):
    """article_view_limited：类跳转图文消息URL用户点击article_view_limited类型按钮后，微信客户端将打开开发者在按钮中article_id对应的图文消息URL。
    """
    type: str = 'article_view_limited'
    name: str
    # 发布后获得的合法 article_id
    article_id: str


if __name__ == '__main__':
    print(WeixinClickButtonItem(name='test', key='测试').model_copy())
