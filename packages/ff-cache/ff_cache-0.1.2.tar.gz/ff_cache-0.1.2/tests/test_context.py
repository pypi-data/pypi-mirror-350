import pytest

from ff_cache.context import ContextManager
from ff_cache.memory_cache import MemoryCache


@pytest.fixture(scope="module", autouse=True)
def setup_module():
    ContextManager._instance = None
    ContextManager.init(cache=MemoryCache())
    yield
    ContextManager._instance = None


def test_context_manager_execptions():
    with pytest.raises(Exception, match="CacheManager has been initialized."):
        ContextManager.init(cache=MemoryCache())

    ContextManager._instance = None

    with pytest.raises(Exception, match="CacheManager has not been initialized, please initialize CacheManager first."):
        ContextManager.get_cache()

    with pytest.raises(Exception, match="CacheManager has not been initialized, please initialize CacheManager first."):
        ContextManager.get_key_builder()

    with pytest.raises(Exception, match="CacheManager has not been initialized, please initialize CacheManager first."):
        ContextManager.get_ttl()
