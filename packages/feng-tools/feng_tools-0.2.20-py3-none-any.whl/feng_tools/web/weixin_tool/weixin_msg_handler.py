from abc import ABCMeta, abstractmethod, ABC

from feng_tools.web.weixin_tool.core import weixin_reply_tool
from feng_tools.web.weixin_tool.core.model.item.weixin_items import ServiceItem, WeixinMpServiceItem, LinkServiceItem
from feng_tools.web.weixin_tool.core.model.item.wx_receive_event_models import WeixinEventItem, WeixinSubscribeEventItem
from feng_tools.web.weixin_tool.core.model.item.wx_receive_msg_models import WeixinTextMsgItem, WeixinImageMsgItem, \
    WeixinVoiceMsgItem, WeixinVideoMsgItem, WeixinLocationMsgItem, WeixinLinkMsgItem
from feng_tools.web.weixin_tool.core.response import XmlResponse


class WeixinTextMsgHandler(metaclass=ABCMeta):
    """微信文本消息处理"""

    def __init__(self):
        self.msg_handler = None
        self.msg_item = None

    def init(self, msg_handler: 'WeixinMsgHandler'):
        self.msg_handler = msg_handler
        self.msg_item = msg_handler.msg_item

    def handle(self) -> XmlResponse:
        return self.msg_handler.return_no_handle()


class WeixinMsgHandler(metaclass=ABCMeta):

    def __init__(self,
                 msg_model: WeixinTextMsgItem | WeixinImageMsgItem | WeixinVoiceMsgItem | WeixinVideoMsgItem | WeixinLocationMsgItem | WeixinLinkMsgItem | WeixinEventItem,
                 text_msg_handler: WeixinTextMsgHandler):
        self.msg_item = msg_model
        self.text_msg_handler = text_msg_handler
        self.text_msg_handler.init(self)

    def get_service_list(self) -> list[str]:
        """获取app服务列表"""
        service_list = []
        for tmp_service_item in self.get_all_service():
            if isinstance(tmp_service_item, WeixinMpServiceItem):
                service_list.append(f'<a data-miniprogram-appid="{tmp_service_item.app_id}" data-miniprogram-path="{tmp_service_item.path}">{tmp_service_item.title}</a>')
            elif isinstance(tmp_service_item, LinkServiceItem):
                service_list.append(f'<a href="{tmp_service_item.href}">{tmp_service_item.title}</a>')
        return service_list

    def handle(self) -> XmlResponse:
        # 查询是否在黑名单中
        if self.is_in_blacklist():
            return self.handle_in_blacklist()
        if isinstance(self.msg_item, WeixinTextMsgItem):
            return self.handle_text_msg()
        elif isinstance(self.msg_item, WeixinEventItem):
            if isinstance(self.msg_item, WeixinSubscribeEventItem):
                if getattr(self.msg_item, 'event') == 'subscribe':
                    return self.handle_subscribe()
                elif getattr(self.msg_item, 'event') == 'unsubscribe':
                    return self.handle_unsubscribe()
        return self.return_no_handle()

    def return_no_handle(self) -> XmlResponse:
        resp_msg_list = ['抱歉，暂无相关服务！', '现有如下服务：']
        resp_msg_list.extend(self.get_service_list())
        return weixin_reply_tool.reply_text(self.msg_item, '\n'.join(resp_msg_list))

    def handle_subscribe(self) -> XmlResponse:
        """关注的事件"""
        resp_msg_list = ['终于等到您了，为您提供了如下服务：']
        resp_msg_list.extend(self.get_service_list())
        resp_msg_list.append('（取消关注后，即使重新关注，也将无法使用服务！）')
        return weixin_reply_tool.reply_text(self.msg_item, '\n'.join(resp_msg_list))

    def handle_in_blacklist(self) -> XmlResponse:
        """处理黑名单中"""
        # 处理黑名单
        return weixin_reply_tool.reply_text(self.msg_item,
                                            '抱歉，你曾取消过关注，如果想要继续提供服务，请<a href="mailto:afenghome@aliyun.com" target="_blank">联系管理员</a>！')

    @abstractmethod
    def get_all_service(self) -> list[ServiceItem]:
        return []

    def handle_text_msg(self) -> XmlResponse:
        return self.text_msg_handler.handle()

    def is_in_blacklist(self) -> bool:
        """是否在黑名单中"""
        # black_list = blacklist_service.query_weixin_black_list()
        # # 查询用户黑名单
        # return self.msg_item.from_user in black_list
        return False

    def handle_unsubscribe(self) -> XmlResponse:
        """取消关注的事件"""
        # 将用户加入黑名单
        # black_po = BlacklistInfoPo(
        #     type_code='wx_blacklist',
        #     type_value=self.msg_item.from_user
        # )
        # # 将用户加入黑名单
        # blacklist_po_service.save(black_po,
        #                           BlacklistInfoPo.type_code == black_po.type_code,
        #                           BlacklistInfoPo.type_value == black_po.type_value)
        return weixin_reply_tool.reply_text(self.msg_item, 'success')


class DefaultWeixinMsgHandler(WeixinMsgHandler, ABC):

    def get_all_service(self) -> list[ServiceItem]:
        return [LinkServiceItem(title='阿锋之家', href='https://www.afenghome.com'),
                LinkServiceItem(title='阿锋搜书', href='https://www.afengbook.com')]

