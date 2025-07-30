from typing import get_origin, Generic, get_args


def get_generic_types(cls):
    """获取类中定义的泛型类型参数"""
    # 方法1: 直接访问 __parameters__
    if hasattr(cls, '__parameters__'):
        return cls.__parameters__

    # 方法2: 检查基类
    for base in cls.__bases__:
        if get_origin(base) is Generic:
            return get_args(base)

    # 方法3: 检查 __orig_bases__
    if hasattr(cls, '__orig_bases__'):
        for base in cls.__orig_bases__:
            if get_origin(base) is Generic:
                return get_args(base)

    return None


if __name__ == '__main__':
    from typing import Generic, TypeVar
    _M = TypeVar('_M')
    _F = TypeVar('_F')
    class BaseSettings:
        pass

    class BaseModelAdminSettings(BaseSettings, Generic[_M, _F]):
        pass

    # 使用示例
    generic_types = get_generic_types(BaseModelAdminSettings)
    print(generic_types)  # 输出: (_M, _F)
