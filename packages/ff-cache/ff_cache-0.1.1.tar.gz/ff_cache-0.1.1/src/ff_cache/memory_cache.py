from time import time
from typing import Dict, List
from .cache import Cache, CacheItem


class MemoryCache(Cache):

    def __init__(self):
        """
        构造函数
        """
        super().__init__()
        self.cache: Dict[str, CacheItem] = {}
        self.cache_expired_at: Dict[str, int] = {}
        self.cache_tags: Dict[str, List[str]] = {}

    def has(self, key):
        """
        是否有缓存
        """
        return key in self.cache and self.cache_expired_at.get(key, 0) > time()
    
    def get(self, key):
        """
        获取缓存
        """
        if not self.has(key):
            return

        cache_item = self.cache.get(key)
        cache_item.ttl = self.cache_expired_at.get(key, 0) - time()

        return cache_item

    def save(self, cache_item):
        """
        保存缓存
        """
        self.cache[cache_item.key] = cache_item
        self.cache_expired_at[cache_item.key] = time() + cache_item.ttl
        
        for tag in cache_item.tags:
            _tag_releate_keys = self.cache_tags.get(tag, [])
            _tag_releate_keys.append(cache_item.key)
            self.cache_tags[tag] = _tag_releate_keys

        return True

    def delete(self, key):
        """
        删除元素
        """
        cache_item = self.get(key=key)

        if not cache_item:
            return True

        if key in self.cache: # pragma: no branch
            del self.cache[key]

        if key in self.cache_expired_at: # pragma: no branch
            del self.cache_expired_at[key]

        for tag in cache_item.tags:
            _tag_related_keys = self.cache_tags.get(tag, [])
            _tag_related_keys.remove(key)
            self.cache_tags[tag] = _tag_related_keys
        
        return True
    
    def delete_tag(self, tag):
        """
        删除缓存标签
        """
        if tag not in self.cache_tags:
            return True

        for key in self.cache_tags.get(tag, []):
            if key in self.cache: # pragma: no branch
                del self.cache[key]

            if key in self.cache_expired_at: # pragma: no branch
                del self.cache_expired_at[key]

        del self.cache_tags[tag]
        return True
    
    def clear(self):
        """
        清空缓存
        """
        self.cache = {}
        self.cache_expired_at = {}
        self.cache_tags = {}
        return True
    
    def is_empty(self):
        """
        检测是否是空缓存
        """
        return self.cache == {} and self.cache_expired_at == {} and self.cache_tags == {}
