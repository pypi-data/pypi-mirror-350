from abc import ABC, abstractmethod


class CacheItem:

    def __init__(self, key, value, ttl, tags = []):
        """
        construct
        """
        self.key = key
        self.value = value
        self.ttl = ttl
        self.tags = tags

class Cache(ABC):

    @abstractmethod
    def has(self, key: str) -> bool:
        """
        检查缓存是否存在
        """

    @abstractmethod
    def get(self, key: str) -> CacheItem:
        """
        获取缓存
        """

    @abstractmethod
    def save(self, cache_item: CacheItem) -> bool:
        """
        保存缓存
        """

    @abstractmethod
    def delete(self, key: str) -> bool:
        """
        删除缓存
        """

    @abstractmethod
    def delete_tag(self, tag: str) -> bool:
        """
        删除缓存标签(按标签删除缓存)
        """

    @abstractmethod
    def clear(self) -> bool:
        """
        清空缓存
        """

    @abstractmethod
    def is_empty(self) -> bool:
        """
        检测是否是空缓存
        """