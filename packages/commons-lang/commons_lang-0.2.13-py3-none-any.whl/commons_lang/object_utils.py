from typing import Union, List


def is_none(obj: any) -> bool:
    return obj is None


def is_not_none(obj: any) -> bool:
    return obj is not None


def is_empty(value: Union[List, str, dict, object]) -> bool:
    if isinstance(value, list) or isinstance(value, dict):
        return value is None or len(value) == 0
    if isinstance(value, str):
        return value is None or value.strip() == ""
    return is_none(value)


def is_not_empty(value: Union[List, str, dict, object]) -> bool:
    return not is_empty(value)


def get(obj: object | dict, attr_path: Union[str, List[str]], default=None):
    if obj is None:
        return default

    if isinstance(attr_path, str):
        keys = attr_path.split(".")
    else:
        keys = attr_path

    def get_value(_obj, _key):
        if isinstance(_obj, dict):
            return _obj.get(_key, default)
        else:
            return getattr(_obj, _key, default)

    current = obj
    if keys is not None:
        for key in keys:
            try:
                if isinstance(current, dict):
                    current = current[key]
                else:
                    current = get_value(current, key)
            except (KeyError, AttributeError, TypeError):
                return default
    else:
        current = get_value(current, keys)

    return current


def assign_default(target_dict, default_dict):
    if isinstance(target_dict, dict) and isinstance(default_dict, dict):
        for key, default_value in default_dict.items():
            if key in target_dict:
                target_dict[key] = assign_default(target_dict[key], default_value)
            else:
                target_dict[key] = default_value
    return target_dict
