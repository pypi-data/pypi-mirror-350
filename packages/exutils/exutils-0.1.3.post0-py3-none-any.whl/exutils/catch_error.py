import functools
import inspect
import traceback
from typing import Callable, TypeVar, ParamSpec, cast, Sequence, Iterable, Optional, Union, overload, Any

try:
    import pandas as _pd
except ModuleNotFoundError:
    _pd = None

T = TypeVar('T')
P = ParamSpec('P')


@overload
def catch_exception(func: Callable[P, T]) -> Callable[P, T]: ...


@overload
def catch_exception(
        *, return_value: Any = ..., suppress: bool = ..., show: bool = ...
) -> Callable[[Callable[P, T]], Callable[P, T]]: ...


def catch_exception(
        _func: Optional[Callable[P, T]] = None,
        *,
        return_value: Any = None,
        suppress: bool = True,
        show: bool = True
) -> Union[Callable[[Callable[P, T]], Callable[P, T]], Callable[..., T]]:
    """
    装饰器：捕获异常并打印堆栈，可控制是否抑制异常。

    用法支持：
    @catch_exception
    @catch_exception(return_value=None, suppress=True, show=True)

    参数：
    - return_value：函数出错时返回的默认值（例如 None、False 等）
    - suppress：是否抑制异常（True 表示异常不再向外抛出）
    - show：是否显示报错详细堆栈

    返回：
    - 一个装饰后的函数，类型与原函数一致
    """

    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"[异常捕获] {func.__name__} 出错：{e}")
                try:
                    sig = inspect.signature(func)
                    bound = sig.bind(*args, **kwargs)
                    bound.apply_defaults()
                    for name, val in bound.arguments.items():
                        if _pd is not None and isinstance(val, (_pd.DataFrame, _pd.Series)):
                            print(f"[参数] {name} \n{val.head()!r}")
                        elif isinstance(val, str):
                            print(f"[参数] {name}={val[:100]!r}..." if len(val) > 100 else f"[参数] {name}={val!r}")
                        elif isinstance(val, dict):
                            sliced = dict(list(val.items())[:5]) if len(val) > 20 else val
                            print(f"[参数] {name}={sliced!r}..." if len(val) > 20 else f"[参数] {name}={val!r}")
                        elif isinstance(val, Sequence):
                            print(f"[参数] {name}={val[:5]!r}..." if len(val) > 20 else f"[参数] {name}={val!r}")
                        elif isinstance(val, Iterable):
                            try:
                                preview = list(val)[:5]
                                print(f"[参数] {name}=迭代器预览: {preview!r}...")
                            except Exception as e:
                                print(f"[参数] {name}=<可迭代对象，无法预览：{e}>")
                        else:
                            print(f"[参数] {name}={val!r}")
                except Exception as bind_err:
                    print(f"[调试参数失败]：{bind_err}")
                    print(f"[args] {args}")
                    print(f"[kwargs] {kwargs}")

                if show:
                    traceback.print_exc()
                if suppress:
                    return cast(T, return_value)
                else:
                    raise

        return cast(Callable[P, T], wrapper)

    if _func is None:
        return decorator
    else:
        return decorator(_func)
