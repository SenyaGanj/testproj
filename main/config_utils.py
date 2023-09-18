import os
from typing import List, Callable, Any


def get_option(section: str, option_name: str, option_default_value: Any = None, cast_type: Callable = None):
    """
    Retrieve option by key env, and cast to `cast_type`
    If value does not specified type casting will be skipped.
    """
    opt = option_default_value
    opt = os.environ.get(f'TESTPROJ_{section.upper()}_{option_name.upper()}', opt)
    if cast_type and opt is not None:
        opt = cast_type(opt)
    return opt


def string_as_bool(opt: str):
    """
    Return True if opt equals to `True` othervise False
    """
    return opt == 'True'


def list_of_strings(raw: str) -> List[str]:
    """
    comma separated list of strings
    """
    return [sub.strip() for sub in raw.split(',') if sub]
