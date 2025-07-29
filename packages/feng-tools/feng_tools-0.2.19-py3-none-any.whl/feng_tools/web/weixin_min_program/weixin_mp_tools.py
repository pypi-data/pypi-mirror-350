"""
微信小程序工具
"""
from feng_tools.base.encrypt import hashlib_tools
from feng_tools.web.weixin_min_program.core.weixin_mp_decrypt import WXBizDataCrypt


def calc_signature(session_key: str, raw_data: str):
    """
    计算signature ： https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/signature.html
    signature = sha1( rawData + session_key )
    :return:
    """
    return hashlib_tools.calc_sha1(raw_data + session_key)


def check_signature(signature: str, session_key: str, raw_data: str):
    """数据签名校验"""
    signature_value = calc_signature(session_key, raw_data)
    return signature == signature_value


def decrypt_data(app_id: str, session_key: str, encrypted_data: str, iv_value: str):
    """解密数据"""
    return WXBizDataCrypt(app_id, session_key).decrypt(encrypted_data, iv_value)


if __name__ == '__main__':
    check_sign = '75e81ceda165f4ffa64f4068af58c64b8f54b88c'
    sign = calc_signature(session_key='HyVFkGl5F5OQWJZZaNzBBg==',
                          raw_data='{"nickName":"Band","gender":1,"language":"zh_CN","city":"Guangzhou","province":"Guangdong","country":"CN","avatarUrl":"http://wx.qlogo.cn/mmopen/vi_32/1vZvI39NWFQ9XM4LtQpFrQJ1xlgZxx3w7bQxKARol6503Iuswjjn6nIGBiaycAjAtpujxyzYsrztuuICqIM5ibXQ/0"}'
                          )
    if check_sign == sign:
        print('success')
