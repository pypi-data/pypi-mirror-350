"""
微信数据解密: https://developers.weixin.qq.com/miniprogram/dev/framework/open-ability/signature.html#%E5%8A%A0%E5%AF%86%E6%95%B0%E6%8D%AE%E8%A7%A3%E5%AF%86%E7%AE%97%E6%B3%95
安装：
- windows平台： pip install pycryptodome
- linux平台： pip install pycrypto
    - 如果出现：ModuleNotFoundError: No module named 'Crypto'，则执行以下操作：
        pip install pycryptodome
"""
import base64
import json
from Crypto.Cipher import AES


class WXBizDataCrypt:
    def __init__(self, app_id, session_key):
        self.app_id = app_id
        self.session_key = session_key

    def decrypt(self, encrypted_data, iv: str):
        # base64 decode
        sessionKey = base64.b64decode(self.session_key)
        encryptedData = base64.b64decode(encrypted_data)
        iv = base64.b64decode(iv)
        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)
        _unpad = lambda s: s[:-ord(s[len(s) - 1:])]
        decrypted = json.loads(_unpad(cipher.decrypt(encryptedData)))
        if decrypted['watermark']['appid'] != self.app_id:
            raise Exception('Invalid Buffer')
        return decrypted

