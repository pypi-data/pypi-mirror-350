"""
微信小程序服务
"""
from typing import Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from feng_tools.base.encrypt import hashlib_tools
from feng_tools.common.enums import GenderTypeEnum
from feng_tools.orm.sqlalchemy import sqlalchemy_model_utils
from feng_tools.web.weixin_min_program import weixin_mp_settings
from feng_tools.web.weixin_min_program.model.weixin_mp_config_schemas import WeixinMpConfigItem
from feng_tools.web.weixin_min_program.model.weixin_mp_items import MpUserInfo
from feng_tools.web.weixin_min_program.model.weixin_mp_models import WeixinMpUserInfoPo
from feng_tools.web.weixin_min_program.model.weixin_mp_open_schemas import WxMpLoginInfo, WxMpUserInfo, \
    WxMpUserBasicInfo


class WeixinMpService:
    def __init__(self, SessionLocal:Type[Session]):
        self.SessionLocal=SessionLocal


    def run_mp_login(self, login_info: WxMpLoginInfo) -> str:
        """
        微信小程序登录
        :param login_info: 登录信息
        :return: token
        """
        print(login_info.model_dump(mode='json'))
        token = hashlib_tools.calc_md5(f'{login_info.mp_app_id}_{login_info.open_id}_{login_info.union_id}')
        po = WeixinMpUserInfoPo(
            app_id=login_info.mp_app_id,
            open_id=login_info.open_id,
            union_id=login_info.union_id,
            session_key=login_info.session_key,
            token=token
        )
        with self.SessionLocal() as db:
            result = db.execute(select(WeixinMpUserInfoPo)
                                .where(WeixinMpUserInfoPo.app_id == login_info.mp_app_id,
                                       WeixinMpUserInfoPo.open_id == login_info.open_id))
            db_data = result.scalar_one_or_none()  # 获取单个结果或None
            if db_data:
                sqlalchemy_model_utils.copy_new_model_to_db_model(db_data, po)
                db.commit()
                # db.refresh(db_data)
            else:
                # 新增
                db.add(po)
                db.commit()
                # db.refresh(po)
            return token


    def run_mp_get_login_info(self, token: str) -> WxMpLoginInfo:

        with self.SessionLocal() as db:
            result = db.execute(select(WeixinMpUserInfoPo)
                                .where(WeixinMpUserInfoPo.token == token))
            userinfoPo = result.scalar_one_or_none()
            return WxMpLoginInfo(
                mp_app_id=userinfoPo.app_id,
                session_key=userinfoPo.session_key,
                union_id=userinfoPo.union_id,
                open_id=userinfoPo.open_id
            )

    def run_mp_save_userinfo(self, user_info: WxMpUserInfo) -> dict|None:
        with self.SessionLocal() as db:
            result = db.execute(select(WeixinMpUserInfoPo)
                                .where(WeixinMpUserInfoPo.token ==  user_info.token))
            userinfo_po = result.scalar_one_or_none()
            if userinfo_po:
                userinfo_po.nick_name = user_info.nick_name
                userinfo_po.avatar_url = user_info.avatar_url
                userinfo_po.country = user_info.country
                userinfo_po.province = user_info.province
                userinfo_po.city = user_info.city
                userinfo_po.gender = GenderTypeEnum.get_enum(user_info.gender)
                userinfo_po.language = user_info.language
                db.commit()
                return MpUserInfo.model_validate(userinfo_po).model_dump()
            return None

    def run_mp_save_user_basic_info(self, user_basic_info: WxMpUserBasicInfo) -> dict|None:
        with self.SessionLocal() as db:
            result = db.execute(select(WeixinMpUserInfoPo)
                                .where(WeixinMpUserInfoPo.token ==  user_basic_info.token))
            userinfo_po = result.scalar_one_or_none()
            if userinfo_po:
                userinfo_po.nick_name = user_basic_info.nick_name
                userinfo_po.avatar_url = user_basic_info.avatar_url
                db.commit()
                return MpUserInfo.model_validate(userinfo_po).model_dump()
            return None

    def get_openid_by_token(self, token: str) -> str|None:
        with self.SessionLocal() as db:
            result = db.execute(select(WeixinMpUserInfoPo)
                                .where(WeixinMpUserInfoPo.token == token))
            userinfo_po = result.scalar_one_or_none()
            if userinfo_po:
                return userinfo_po.open_id
        return None


def init_weixin_mp_setting(app_id, app_secret, mp_service: WeixinMpService):
    """初始化微信小程序"""
    weixin_mp_settings.init_mp_config(mp_app_id=app_id,
                                      mp_config_item=WeixinMpConfigItem(
                                          mp_app_id=app_id,
                                          mp_app_secret=app_secret,
                                          mp_login_callback=mp_service.run_mp_login,
                                          mp_get_login_info_callback=mp_service.run_mp_get_login_info,
                                          mp_save_userinfo_callback=mp_service.run_mp_save_userinfo,
                                          mp_save_user_basic_info_callback=mp_service.run_mp_save_user_basic_info
                                      ))
