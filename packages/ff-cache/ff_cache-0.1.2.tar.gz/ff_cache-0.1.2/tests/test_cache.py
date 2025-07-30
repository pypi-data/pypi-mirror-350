from . import stubs
from ff_cache.memory_cache import MemoryCache


def test_cache():
    stubs.TestCase.run_test(cache=MemoryCache())