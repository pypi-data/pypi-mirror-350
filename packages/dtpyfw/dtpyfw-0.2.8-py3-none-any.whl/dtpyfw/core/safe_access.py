from typing import Callable, Any


__all__ = (
    'safe_access',
    'convert_to_int_or_float',
)


def safe_access(func: Callable, default_value: Any = None):
    try:
        return func()
    except:
        return default_value


def convert_to_int_or_float(string_num: str) -> int | float:
    try:
        float_num = float(string_num)
        if float_num.is_integer():
            return int(float_num)
        else:
            return float_num
    except ValueError:
        return None
