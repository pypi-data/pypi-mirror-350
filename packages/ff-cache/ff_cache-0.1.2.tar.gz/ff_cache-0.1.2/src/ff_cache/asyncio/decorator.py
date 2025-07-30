import asyncio
import inspect
from functools import wraps
from typing import Callable, List, Union

from .cache import AsyncCache
from ff_cache.cache import Cache, CacheItem
from ff_cache.context import ContextManager


def cache(
    cache: Cache = None,
    key: Union[Callable[..., str], str] = None, 
    ttl: Union[Callable[..., int], int] = None,
    tags: List[str] = []
):
    """
    缓存装饰器

    Args:
        cache: 缓存实例
        key: 缓存键名
        ttl: 过期时间
        tags: 缓存标签

    Returns:
        缓存包装函数对象
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            return await _cache_func(
                func=func, cache=cache, key=key, ttl=ttl, tags=tags, *args, **kwargs
            )
        return wrapper        
    return decorator

async def _cache_func(
    *args,
    func,
    cache: Cache, 
    key: Union[Callable[..., str], str],
    ttl: Union[Callable[..., int], int] = 0,
    tags: List[str] = [],
    **kwargs
):
    key = key if key else ContextManager.get_key_builder()
    ttl = ttl if ttl else ContextManager.get_ttl()
    cache = cache if cache else ContextManager.get_cache()

    _key_args = args
    func_arg_names = list(inspect.signature(func).parameters.keys())
    if len(args) > 0 and len(func_arg_names) > 0 and func_arg_names[0] == 'self':
        _key_args = (args[0].__class__,) + args[1:]

    _key = key if isinstance(key, str) else await _exec_func(key, func.__qualname__, *_key_args, **kwargs)

    if await _has_cache(cache=cache, key=_key):
        return (await _get_cache(cache=cache, key=_key)).value

    result = await _exec_func(func, *args, **kwargs)
    _ttl = ttl if isinstance(ttl, int) else await _exec_func(ttl, result=result, *args, **kwargs)

    cache_item = CacheItem(
        key=_key,
        value=result,
        ttl=_ttl,
        tags=tags
    )

    await _save_cache(cache=cache, cache_item=cache_item)
    return cache_item.value

async def _exec_func(func, *args, **kwargs):
    """
    执行函数
    """
    if asyncio.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    
    return func(*args, **kwargs)

async def _has_cache(cache: Cache, key: str):
    """
    检查缓存是否存在
    """
    if isinstance(cache, AsyncCache):
        return await cache.has(key=key)
    
    return cache.has(key=key)

async def _save_cache(cache: Cache, cache_item: CacheItem):
    """
    保存缓存
    """
    if isinstance(cache, AsyncCache):
        return await cache.save(cache_item=cache_item)
    
    return cache.save(cache_item=cache_item)

async def _get_cache(cache: Cache, key: str):
    """
    获取缓存
    """
    if isinstance(cache, AsyncCache):
        return await cache.get(key=key)
    
    return cache.get(key=key)