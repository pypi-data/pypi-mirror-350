from functools import wraps
from threading import RLock

instances = {}
singleton_lock = RLock()


def singleton(cls):
    @wraps(cls)
    def create_instance(*args, **kwargs):
        if cls not in instances:
            with singleton_lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    create_instance.original_cls = cls
    return create_instance
