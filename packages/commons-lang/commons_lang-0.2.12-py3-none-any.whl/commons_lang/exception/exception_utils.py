from typing import Type


def raise_exception(exception_message, exception_type: Optional[Type[Exception]] = None):
    if exception_type is None:
        raise Exception(exception_message)
    raise exception_type(exception_message)
