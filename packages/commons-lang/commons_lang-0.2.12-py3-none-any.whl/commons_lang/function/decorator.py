import time as t
from functools import wraps
from typing import Callable, Optional

from loguru import logger


def elapsed(func) -> Callable:
    def decorator(*args, **kwargs):
        start_time = t.time()
        result = func(*args, **kwargs)
        end_time = t.time()
        logger.debug(f"{func.__name__} elapsed time: {end_time - start_time:.4f} s")
        return result

    return decorator


def deprecated(reason: Optional[str] = None) -> Callable:
    def decorator(func) -> Callable:
        original_func = func.__func__ if isinstance(func, staticmethod) or isinstance(func, classmethod) else func

        @wraps(original_func)
        def decorated_function(*args, **kwargs):
            msg = f"Call to deprecated function {original_func.__name__}"
            if reason:
                msg += f": {reason}"
            if not msg.endswith("."):
                msg += "."
            logger.warning(msg, category=DeprecationWarning, stacklevel=2)
            return original_func(*args, **kwargs)

        if isinstance(func, staticmethod):
            return staticmethod(decorated_function)
        elif isinstance(func, classmethod):
            return classmethod(decorated_function)
        else:
            return decorated_function

    return decorator


def once(method):
    method_name = method.__name__
    method_executed_flag = f"__{method_name}_executed__"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        if hasattr(self, method_executed_flag) and getattr(self, method_executed_flag):
            logger.debug(f"{method_name} has been executed.")
            return None

        with once_lock:
            if hasattr(self, method_executed_flag) and getattr(self, method_executed_flag):
                logger.debug(f"{method_name} has been executed after once lock.")
                return None

            result = method(self, *args, **kwargs)
            setattr(self, method_executed_flag, True)
            return result

    return wrapper
