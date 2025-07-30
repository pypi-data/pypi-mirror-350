from typing import Callable, Union
from .cache import Cache
from .functions import md5_key_builder


class ContextManager(object):

    _instance = None

    def __init__(
        self, 
        cache: Cache,
        key_builder: Callable[..., str] = md5_key_builder,
        ttl: Union[Callable[..., int], int] = 300
    ):
        """
        构造函数
        """
        self.cache = cache
        self.key_builder = key_builder
        self.ttl = ttl

    @classmethod
    def init(
        cls, 
        cache: Cache,
        key_builder: Callable[..., str] = md5_key_builder,
        ttl: Union[Callable[..., int], int] = 300
    ):
        """
        初始化
        """
        if cls._instance:
            raise Exception("CacheManager has been initialized.")

        cls._instance = ContextManager(cache=cache, key_builder=key_builder, ttl=ttl)
        return cls._instance
    
    @classmethod
    def get_cache(cls) -> Cache:
        """
        获取缓存
        """
        if not cls._instance:
            raise Exception("CacheManager has not been initialized, please initialize CacheManager first.")
        
        return cls._instance.cache
    
    @classmethod
    def get_key_builder(cls) -> Callable[..., str]:
        """
        获取key_builder
        """
        if not cls._instance:
            raise Exception("CacheManager has not been initialized, please initialize CacheManager first.")
        
        return cls._instance.key_builder
    
    @classmethod
    def get_ttl(cls) -> int:
        """
        获取默认超时设置
        """
        if not cls._instance:
            raise Exception("CacheManager has not been initialized, please initialize CacheManager first.")
        
        return cls._instance.ttl