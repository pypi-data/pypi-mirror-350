import inspect
from ff_cache.cache import *


class AsyncCache(Cache):
    
    def __init_subclass__(cls, **kwargs):
        """
        判断子类方法是否是async方法
        """
        super().__init_subclass__(**kwargs)
        super_names = [name for name, _ in Cache.__dict__.items()]

        for name, method in cls.__dict__.items():
            if (
                name not in super_names
                or not callable(method) 
                or name.startswith("__") 
                or inspect.iscoroutinefunction(method)
            ):
                continue
            raise TypeError(f"{cls.__name__} cannot define non-async method '{name}'")
