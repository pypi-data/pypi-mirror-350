"""This module contains a set of utility functions for dictionaries."""

import collections.abc
from decimal import Decimal
from typing import Any, Dict, List, Optional, Union, cast

import numpy as np

from . import LOG

Numeric = Union[
    bool,
    int,
    float,
    np.int16,
    np.int32,
    np.int64,
    np.float16,
    np.float32,
    np.float64,
    str,
]
INT_TYPES = (int, np.integer)
FLOAT_TYPES = (float, np.floating)


def update(src: Dict[str, Any], upd: Dict[str, Any]) -> Dict[str, Any]:
    """Recursive update of dictionaries.

    See stackoverflow:

        https://stackoverflow.com/questions/3232943/
        update-value-of-a-nested-dictionary-of-varying-depth

    """
    for key, val in upd.items():
        if isinstance(val, collections.abc.Mapping):
            src[key] = update(src.get(key, {}), cast(Dict[str, Any], val))
        else:
            src[key] = val
    return src


def convert(src: Dict[Any, Any]) -> Dict[str, Any]:
    """Recursive conversion to basic data types."""

    new_src: Dict[str, Any] = {}
    for key, val in src.items():
        nkey = convert_key(key)
        if not isinstance(nkey, str):
            nkey = str(nkey)
        if isinstance(val, collections.abc.Mapping):
            new_src[key] = convert(cast(Dict[Any, Any], val))
        elif isinstance(val, list):
            new_src[key] = convert_list(val)
        elif isinstance(val, np.ndarray):
            if val.shape:
                new_src[key] = convert_list(val.tolist())
            else:
                new_src[key] = convert_val(val.item())
        else:
            new_src[key] = convert_val(val)

    return new_src


def convert_list(old_list: List[Any]) -> List[Any]:
    new_list = list()
    for val in old_list:
        if isinstance(val, collections.abc.Mapping):
            new_list.append(convert(cast(Dict[str, Any], val)))
        elif isinstance(val, (list, tuple, np.ndarray)):
            new_list.append(convert_list(list(val)))
        else:
            new_list.append(convert_val(val))
    return new_list


def convert_key(val: Any) -> str:
    converted = convert_val(val)
    return str(converted) if converted is not None else val


def convert_val(
    val: Optional[Numeric],
) -> Optional[Union[bool, int, float, str]]:
    if val is None or val == "None":
        return None
    if isinstance(val, bool):
        return val
    if isinstance(val, INT_TYPES):
        return int(val)
    if isinstance(val, FLOAT_TYPES):
        return float(Decimal(str(val)))

    try:
        return strtobool(val)
    except (ValueError, TypeError, AttributeError):
        pass
    try:
        return int(val)
    except (ValueError, TypeError):
        pass
    try:
        return float(val)
    except (ValueError, TypeError):
        pass
    try:
        return str(val)
    except (ValueError, TypeError):
        LOG.info("Unable to convert value %s", val)

    return "MISSING_VALUE"


def strtobool(val: str) -> bool:
    """Convert a string representation of truth to true or false.

    True values are 'y', 'yes', 't', 'true', 'on', and '1'; false
    values are 'n', 'no', 'f', 'false', 'off', and '0'. Raises
    ValueError if 'val' is anything else.

    This is mostly the implementation of the now deprecated
    distutils package. However, it is change in that regard that an
    actual bool type value is returned instead of 1 or 0.

    """
    val = val.lower()
    if val in ("y", "yes", "t", "true", "on", "1"):
        return True
    elif val in ("n", "no", "f", "false", "off", "0"):
        return False
    else:
        raise ValueError(f"Invalid truth value {val}")


def tobool(val: Union[bool, int, float, str]) -> bool:
    """Convert any basic type representation to true or false"""

    if isinstance(val, bool):
        return val

    elif isinstance(val, int):
        return val != 0

    elif isinstance(val, float):
        return val != 0.0

    elif isinstance(val, str):
        return strtobool(val)

    else:
        raise ValueError(
            f"Cannot convert value {val} of type {type(val)} to bool."
        )


def bool_from_dict(d: Dict[str, Any], key: str, default: bool = False) -> bool:
    val = d.get(key, default)
    try:
        val = bool(strtobool(val))
    except AttributeError:
        pass
    return val


def set_default_bool(
    d: Dict[str, Any], key: str, default: bool = False
) -> bool:
    val = bool_from_dict(d, key, default)
    d.setdefault(key, val)
    return val


def set_default_float(
    d: Dict[str, Any], key: str, default: float = 0.0
) -> float:
    val = d.get(key, default)
    d[key] = float(Decimal(str(val)))
    return val


def set_default_int(d: Dict[str, Any], key: str, default: int = 0) -> int:
    val = d.get(key, default)
    d[key] = int(val)
    return val
