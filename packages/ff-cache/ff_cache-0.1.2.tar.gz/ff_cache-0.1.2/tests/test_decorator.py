import pytest
from time import time, sleep
from ff_cache.memory_cache import MemoryCache
from ff_cache.decorator import cache, ContextManager


@pytest.fixture(scope="module", autouse=True)
def setup_module():
    ContextManager._instance = None
    ContextManager.init(cache=MemoryCache())
    yield
    ContextManager._instance = None


@cache()
def get_time():
    return time()

def test_cache_func():
    res = get_time()
    sleep(1)
    assert res == get_time()


class Service():

    @cache()
    def test_method(self):
        return f"Service::test_method call, timestamp: {time()}"
    
    @classmethod
    @cache()
    def test_cls_method(cls):
        return f"Service::test_cls_method call, timestamp: {time()}"
    
    @staticmethod
    @cache()
    def test_static_method():
        return f"Service::test_static_method call, timestamp: {time()}"

def test_cache_class_method():
    service = Service()

    instance_res = service.test_method()
    sleep(1)
    assert instance_res == service.test_method()

    cls_res = Service.test_cls_method()
    sleep(1)
    assert cls_res == Service.test_cls_method()

    static_res = Service.test_static_method()
    sleep(1)
    assert static_res == Service.test_static_method()
