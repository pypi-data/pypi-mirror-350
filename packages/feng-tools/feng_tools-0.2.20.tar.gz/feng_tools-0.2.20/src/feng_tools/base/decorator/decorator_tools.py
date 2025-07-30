"""
装饰器工具
"""
from typing import Callable, Any


def run_func(func: Callable, *args, **kwargs):
    """运行函数"""
    if isinstance(func, Callable):
        return func(*args, **kwargs)
    else:
        return func.__func__(*args, **kwargs)


async def run_async_func(func: Callable, *args, **kwargs):
    """运行异步函数"""
    if isinstance(func, Callable):
        return await func(*args, **kwargs)
    else:
        return await func.__func__(*args, **kwargs)


def append_decorator_info(func: Callable, decorator_name: str):
    """添加装饰器信息（装饰器中内部函数需要有装饰器：@wraps(func)）"""
    if hasattr(func, '__decorators__'):
        getattr(func, '__decorators__').append(decorator_name)
    else:
        setattr(func, '__decorators__', [decorator_name])


def append_func_info(func: Callable, key: str, value: Any):
    """通过装饰器添加函数信息（装饰器中内部函数需要有装饰器：@wraps(func)）"""
    setattr(func, key, value)


def get_func_by_decorator(module, decorator_name) -> dict[str, Callable]:
    """获取模块中具有某个装饰器的函数列表"""
    func_members = {}
    for tmp_key in dir(module):
        if tmp_key.startswith('__'):
            continue
        tmp_value = module.__dict__[tmp_key]
        if isinstance(tmp_value, Callable) and hasattr(tmp_value, '__decorators__') and decorator_name in getattr(tmp_value, '__decorators__'):
            func_members[tmp_key] = tmp_value
    return func_members
