import json
from time import time
from typing import Optional
from redis.asyncio import Redis, ConnectionPool

from ff_cache.asyncio.cache import AsyncCache, CacheItem
from ff_cache.serializer import Serializer, PickleSerializer


class AsyncRedisCache(AsyncCache):

    def __init__(
        self,
        url: Optional[str] = None,
        connection_pool: Optional[ConnectionPool] = None,
        prefix: str = "_ff_cache",
        max_delete_batch: int = 100,
        serializer: Serializer = None
    ):
        """
        构造函数
        """
        super().__init__()
        self.url = url
        self.connection_pool = connection_pool
        self.prefix = prefix
        self.max_delete_batch = max_delete_batch
        self.serializer = serializer if serializer else PickleSerializer()

        if not self.url and not self.connection_pool:
            raise RuntimeError(
                "Failed to initialize redis client instance. "
                "redis url or connection pool cannot be empty at the same time."
            )
        
        if not self.connection_pool:
            self.connection_pool = ConnectionPool.from_url(self.url)

    def get_redis_client(self) -> Redis:
        """
        获取Redis实例
        """
        return Redis(connection_pool=self.connection_pool)

    def _cache_key(self, key: str):
        """
        获取cache_key
        """
        return f"{self.prefix}:cache:{key}"
    
    def _cache_tag_key(self, key: str):
        """
        获取缓存对应的tag_key
        """
        return f"{self.prefix}:cache:{key}_tags"

    def _tag_key(self, tag: str):
        """
        获取tag_key
        """
        return f"{self.prefix}:tags:{tag}"
    
    def _trash_key(self, key: str):
        """
        获取待回收的tag_key
        """
        _prefix = f"{self.prefix}:"
        _key = key[len(_prefix):] if key.startswith(_prefix) else key
        return f"{self.prefix}:trash:{_key}"

    async def has(self, key: str):
        """
        判断key是否存在
        """
        redis_client = self.get_redis_client()
        return await redis_client.exists(self._cache_key(key))
    
    async def get(self, key):
        """
        获取缓存
        """
        if not await self.has(key=key):
            return

        redis_client = self.get_redis_client()
        _key = self._cache_key(key=key)
        _tag_key = self._cache_tag_key(key=key)

        async with redis_client.pipeline() as pipe:
            pipe.get(_key)
            pipe.get(_tag_key)
            pipe.ttl(_key)
            value, tags, ttl = await pipe.execute()

        if value and not redis_client.get_connection_kwargs().get("decode_responses"):
            value = value.decode("utf-8")

        return CacheItem(
            key=key,
            value=self.serializer.decode(value),
            ttl=ttl,
            tags=json.loads(tags) if tags else []
        )

    async def save(self, cache_item):
        """
        保存缓存
        """
        redis_client = self.get_redis_client()

        _key = self._cache_key(key=cache_item.key)
        _tag_key = self._cache_tag_key(key=cache_item.key)
        _value = self.serializer.encode(cache_item.value)

        async with redis_client.pipeline() as pipe:
            pipe.set(_key, _value.encode("utf-8"), ex=cache_item.ttl)

            if cache_item.tags:
                pipe.set(_tag_key, json.dumps(cache_item.tags), ex=cache_item.ttl)
                for tag in cache_item.tags:
                    pipe.zadd(self._tag_key(tag=tag), {_key: time() + cache_item.ttl})

            await pipe.execute()
        
        return True
    
    async def delete(self, key):
        """
        删除缓存
        """
        redis_client = self.get_redis_client()

        _key = self._cache_key(key)
        _tag_key = self._cache_tag_key(key)
        tags = await redis_client.get(_tag_key)

        async with redis_client.pipeline() as pipe:
            pipe.unlink(_key, _tag_key)

            if tags:
                for tag in tags:
                    pipe.zrem(self._tag_key(tag=tag), _key)

            await pipe.execute()           

        return True

    async def delete_tag(self, tag):
        """
        通过标签删除缓存
        """
        _key = self._tag_key(tag=tag)
        _trash_key = self._trash_key(key=_key)
        redis_client = self.get_redis_client()
        
        if not await redis_client.exists(_key):
            return True

        await redis_client.rename(_key, _trash_key)
        await self._delete_trash_tag(trash_key=_trash_key)
        return True

    async def _delete_trash_tag(self, trash_key: str):
        """
        移除缓存标签
        """
        cursor = 0
        redis_client = self.get_redis_client()

        while True:
            cursor, elements = await redis_client.zscan(trash_key, cursor=cursor, count=self.max_delete_batch)

            if elements: # pragma: no branch
                _elements = [e for e, _ in elements]
                _tag_elements = [f"{e}_tags" for e, _ in elements]
                await redis_client.unlink(*_elements, *_tag_elements)

            if cursor <= 0: # pragma: no branch
                break

        await redis_client.unlink(trash_key)
        return True

    async def clear(self):
        """
        清除缓存        
        """
        cursor = 0
        redis_client = self.get_redis_client()

        while True:
            cursor, keys = await redis_client.scan(cursor, match=f"{self.prefix}*", count=self.max_delete_batch)

            if keys:
                await redis_client.unlink(*keys)
                
            if cursor <= 0: # pragma: no branch
                break

        return True
    
    async def is_empty(self):
        """
        检测是否是空缓存
        """
        cursor = 0
        redis_client = self.get_redis_client()
        cursor, keys = await redis_client.scan(cursor, match=f"{self.prefix}*", count=self.max_delete_batch)

        return True if not keys else False