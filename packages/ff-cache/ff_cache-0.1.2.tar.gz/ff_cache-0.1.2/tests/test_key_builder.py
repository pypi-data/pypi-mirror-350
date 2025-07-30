import warnings
from ff_cache.key_builder import md5_key_builder


def test_md5_key_builder_deprecation_warning():
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")  # 确保警告被捕获
        md5_key_builder("a")

        # 验证捕获到警告数量为1
        assert len(w) == 1

        # 验证捕获到的警告类型是 DeprecationWarning 或其子类
        assert issubclass(w[0].category, DeprecationWarning)

        # 验证警告信息包含指定的 reason
        assert "use ff_cache.functions.md5_key_builder instead" in str(w[0].message)