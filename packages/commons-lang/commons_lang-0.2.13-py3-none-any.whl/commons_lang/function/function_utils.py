import inspect
import platform
from types import MethodType
from typing import Optional, List, Any, Type

_IS_PY3 = platform.python_version_tuple()[0] == "3"


def __get_self(func):
    if _IS_PY3:
        return func.__self__ if hasattr(func, "__self__") else None
    else:
        return func.im_self if hasattr(func, "im_self") else None


def __has_self(func):
    return __get_self(func) is not None


def __resolve_cls(func) -> Optional[Type]:
    module = inspect.getmodule(func)
    qualname_parts = func.__qualname__.split(".")
    if len(qualname_parts) <= 1:
        return None
    class_name = qualname_parts[-2]
    cls = getattr(module, class_name, None)
    if not cls or not inspect.isclass(cls):
        return None
    if not hasattr(cls, func.__name__):
        return None
    return cls


def __resolve_args(func) -> List[Any]:
    sig = inspect.signature(func)
    args = list(sig.parameters.keys())
    return args


def __resolve_first_source_line(func) -> str:
    source_lines = inspect.getsourcelines(func)
    line0: str = source_lines[0][0]
    return line0.replace(" ", "")


def is_bound_method(func) -> bool:
    return isinstance(func, MethodType) and __has_self(func)


def is_lambda(func) -> bool:
    return callable(func) and func.__name__ == "<lambda>"


def is_abstract_method(func) -> bool:
    if not hasattr(func, "__qualname__"):
        return False
    if is_lambda(func):
        return False
    return hasattr(func, "__isabstractmethod__") and func.__isabstractmethod__


def is_instance_method(func) -> bool:
    if not hasattr(func, "__qualname__"):
        return False
    if is_lambda(func):
        return False
    if is_abstract_method(func):
        return False
    if is_bound_method(func):
        return not inspect.isclass(func.__self__)
    cls = __resolve_cls(func)
    if not cls:
        return False
    args = __resolve_args(func)
    return len(args) > 0 and args[0] == "self"


def is_class_method(func) -> bool:
    if isinstance(func, classmethod):
        return True
    if not hasattr(func, "__qualname__"):
        return False
    first_source_line = __resolve_first_source_line(func)
    if first_source_line.startswith("@classmethod"):
        return True
    if is_lambda(func):
        return False
    if is_abstract_method(func):
        return False
    if is_instance_method(func):
        return False
    if is_bound_method(func):
        return inspect.isclass(func.__self__)
    cls = __resolve_cls(func)
    if not cls:
        return False
    args = __resolve_args(func)
    return len(args) > 0 and args[0] == "cls"


def is_static_method(func) -> bool:
    """
    Check if a function is a static method.
    TODO 暂时无法判断使用classmethod()函数转换的情况
    """
    if isinstance(func, staticmethod):
        return True
    if not hasattr(func, "__qualname__"):
        return False
    first_source_line = __resolve_first_source_line(func)
    if first_source_line.startswith("@staticmethod"):
        return True
    if is_lambda(func):
        return False
    if is_abstract_method(func):
        return False
    if is_instance_method(func):
        return False
    if is_class_method(func):
        return False
    if is_bound_method(func):
        return inspect.isclass(func.__self__)
    return False
