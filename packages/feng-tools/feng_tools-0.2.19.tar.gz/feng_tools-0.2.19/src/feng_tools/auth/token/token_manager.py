from abc import ABC, abstractmethod
from typing import Generic, TypeVar

_T = TypeVar("_T")

class TokenManager(ABC, Generic[_T]):
    """Token管理器"""
    def __init__(self, ttl:int=7200, renew_threshold:int=1800):
        """
        :param ttl: Token有效期, 默认是 2小时（7200 秒）
        :param renew_threshold: 自动续期阈值, 默认是 剩余30分钟时续期
        """
        self.ttl = ttl
        self.renew_threshold=renew_threshold

    @abstractmethod
    def create_token(self, login_info:_T, token:str=None) -> str:
        """创建token"""
        pass

    @abstractmethod
    def validate_token(self, token:str) -> bool:
        """校验token"""
        pass

    @abstractmethod
    def get_login_info(self, token:str) -> _T:
        """通过token获取登录信息"""
        pass

    @abstractmethod
    def remove_token(self, token:str):
        """移除token"""
        pass

    @classmethod
    @abstractmethod
    def get_token_from_request(cls, request):
        """从request中获取token"""
        pass