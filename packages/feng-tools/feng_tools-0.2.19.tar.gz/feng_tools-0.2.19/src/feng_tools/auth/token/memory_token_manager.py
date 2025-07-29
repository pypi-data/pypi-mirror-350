"""
pip install cachetools
"""
import hashlib
import time

from cachetools import TTLCache

from feng_tools.auth.token.token_manager import TokenManager


class MemoryTokenManager(TokenManager):
    def __init__(self, maxsize=1000, ttl:int=7200, renew_threshold:int=1800):
        super().__init__(ttl, renew_threshold)
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def create_token(self, login_info, token:str=None) -> str:
        """创建token"""
        # 简单生成 Token
        current_time = time.time()
        if not token:
            token = hashlib.md5(f"{str(login_info)}_{int(current_time)}".encode()).hexdigest().lower()
        self.cache[token] = {"login_info": login_info, "created_at": current_time}
        return token
    def _refresh_time(self, token:str) -> bool:
        token_info = self.cache.get(token)
        if token_info:
            remaining_time = self.ttl - (time.time() - token_info["created_at"])
            if remaining_time<=0:
                return False
            # 仅在用户访问时触发续期逻辑
            if remaining_time < self.renew_threshold:  # 如果剩余时间小于阈值，则续期
                # 更新缓存以延长有效期
                token_info["created_at"] = time.time()
                self.cache[token] = token_info
            return True
        return False
    def validate_token(self, token:str) -> bool:
        """校验token"""
        if token in self.cache:
            self._refresh_time(token)
            return True
        return False

    def get_login_info(self, token:str):
        """通过token获取登录信息"""
        if token in self.cache:
            return self.cache[token].get("login_info")
        return None

    def remove_token(self, token:str):
        """移除token"""
        if token in self.cache:
            del self.cache[token]

    @classmethod
    def get_token_from_request(cls, request):
        """从request中获取token"""
        # 假设 Token 存储在请求的 cookies 中
        # return request.cookies.get("token")
        # 假设 Token 存储在请求的 Authorization 头中
        if request.headers and request.headers.get('Authorization'):
            return request.headers.get('Authorization').lstrip('Bearer').strip()
        return None