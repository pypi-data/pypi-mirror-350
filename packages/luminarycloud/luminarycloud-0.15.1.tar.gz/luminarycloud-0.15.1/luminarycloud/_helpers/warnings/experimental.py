# mypy: ignore-errors

import warnings
from functools import wraps
from typing import Callable, TypeVar

C = TypeVar("C")


def experimental(f: C) -> C:
    """Mark a function or class as experimental."""
    if isinstance(f, Callable):
        return _experimental_function(f)
    else:
        return _experimental_class(f)


def _experimental_class(cls: type[C]) -> type[C]:
    old_init = cls.__init__

    @wraps(old_init)
    def new_init(self, *args, **kwargs):
        warnings.warn(
            f"{cls.__name__} is an experimental feature and may change or be removed without notice.",
            category=FutureWarning,
            stacklevel=2,
        )
        return old_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls


def _experimental_function(f: Callable) -> Callable:
    @wraps(f)
    def new_func(*args, **kwargs):
        warnings.warn(
            f"{f.__name__}() is an experimental feature and may change or be removed without notice.",
            category=FutureWarning,
            stacklevel=2,
        )
        return f(*args, **kwargs)

    return new_func
