"""
微信小程序的api调用服务
"""
import requests

from feng_tools.web.http.http_auto_retry_tools import auto_retry
from feng_tools.web.weixin_min_program import weixin_mp_settings
from feng_tools.web.weixin_min_program.core.weixin_mp_models import Jscode2sessionResult, TokenResult, CheckResult, \
    GenerateUrlLink
from feng_tools.web.weixin_min_program.model.weixin_mp_config_schemas import WeixinMpConfigKeyEnum


@auto_retry(max_retries=3)
def request_jscode2session(mp_app_id: str, js_code: str) -> Jscode2sessionResult | None:
    """
    小程序登录： https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/code2Session.html
    :param mp_app_id:
    :param js_code:
    :return:
    """
    mp_app_id = weixin_mp_settings.get_config(mp_app_id, WeixinMpConfigKeyEnum.mp_app_id)
    mp_app_secret = weixin_mp_settings.get_config(mp_app_id, WeixinMpConfigKeyEnum.mp_app_secret)
    params = {
        'appid': mp_app_id,
        'secret': mp_app_secret,
        'js_code': js_code,
        'grant_type': 'authorization_code',
    }
    resp = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=params)
    if resp.status_code == 200:
        return Jscode2sessionResult(**resp.json())
    return None


def request_token(mp_app_id: str) -> TokenResult | None:
    """
    获取接口调用凭据: https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/mp-access-token/getAccessToken.html
    :return:
    """
    mp_app_id = weixin_mp_settings.get_config(mp_app_id, WeixinMpConfigKeyEnum.mp_app_id)
    mp_app_secret = weixin_mp_settings.get_config(mp_app_id, WeixinMpConfigKeyEnum.mp_app_secret)
    params = {
        'appid': mp_app_id,
        'secret': mp_app_secret,
        'grant_type': 'client_credential',
    }
    resp = requests.get('https://api.weixin.qq.com/cgi-bin/token', params=params)
    if resp.status_code == 200:
        return TokenResult(**resp.json())
    return None


def request_check_session(access_token: str, openid: str, signature: str) -> CheckResult | None:
    """
    检验登录态： https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/user-login/checkSessionKey.html
    :return:
    """
    params = {
        'access_token': access_token,
        'openid': openid,
        'signature': signature,
        'sig_method': 'hmac_sha256'
    }
    resp = requests.get('https://api.weixin.qq.com/wxa/checksession', params=params)
    if resp.status_code == 200:
        return CheckResult(**resp.json())
    return None


def request_generate_url_link(access_token: str, page_path: str, query: str = None,
                              expire_interval: int = 30,
                              env_version: str = 'release') -> GenerateUrlLink | None:
    """
    获取URLLink: https://developers.weixin.qq.com/miniprogram/dev/OpenApiDoc/qrcode-link/url-link/generateUrlLink.html
    :param access_token: 接口调用凭证
    :param page_path: 通过 URL Link 进入的小程序页面路径，必须是已经发布的小程序存在的页面，不可携带 query 。path 为空时会跳转小程序主页
    :param query: 通过 URL Link 进入小程序时的query，最大1024个字符，只支持数字，大小写英文以及部分特殊字符：!#$&'()*+,/:;=?@-._~%
    :param expire_interval: 到期失效的URL Link的失效间隔天数。生成的到期失效URL Link在该间隔时间到达前有效。最长间隔天数为30天。expire_type 为 1 必填
    :param env_version: 默认值"release"。要打开的小程序版本。正式版为 "release"，体验版为"trial"，开发版为"develop"，仅在微信外打开时生效。
    :return:
    """
    params = {
        'path': page_path,
        'expire_type': 1,
        'expire_interval': expire_interval,
        'env_version': env_version
    }
    if query:
        params['query'] = query
    api_url = 'https://api.weixin.qq.com/wxa/generate_urllink?access_token='+access_token
    resp = requests.post(api_url, params=params)
    if resp.status_code == 200:
        return GenerateUrlLink(**resp.json())
    return None

