"""Decorator for validating non-empty string parameters."""

from __future__ import annotations

import inspect
from collections.abc import Callable
from functools import wraps
from typing import Any, ParamSpec, TypeVar

from .errors import EmptyStringError, MissingParameterError, NoneNotAllowedError, StringTypeError

P = ParamSpec("P")
R = TypeVar("R")


def _validate_string_is_not_blank(
    value: Any,
    parameter_name: str,
) -> None:
    """Validate that a string is non-blank.

    Args:
        value: The value to validate.
        parameter_name: The name of the parameter being validated.

    Raises:
        NoneNotAllowedError: If the value is None.
        StringTypeError: If the value is not a string.
        EmptyStringError: If the string is empty.
    """
    if value is None:
        raise NoneNotAllowedError(parameter_name)

    if not isinstance(value, str):
        raise StringTypeError(parameter_name)

    trimmed = value.strip()
    if not trimmed:
        raise EmptyStringError(parameter_name)


def require_non_blank_strings(
    *parameter_names: str,
    use_partial_bind: bool = True,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Ensure specified parameters are non-blank strings.

    Args:
        *parameter_names: Parameter names to validate.
        use_partial_bind: When true, uses signature.bind_partial. When false, uses signature.bind to mirror normal call
            validation.

    Raises:
        MissingParameterError: If a specified parameter is missing from the call.
        NoneNotAllowedError: If a parameter value is None.
        StringTypeError: If a parameter value is not a string.
        EmptyStringError: If a parameter value is empty.
    """
    names = tuple(dict.fromkeys(parameter_names))

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        sig = inspect.signature(func)
        binder = sig.bind_partial if use_partial_bind else sig.bind
        func_name = func.__name__

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> R:
            bound = binder(*args, **kwargs)
            bound.apply_defaults()

            for name in names:
                if name not in bound.arguments:
                    raise MissingParameterError(name, func_name)

                value = bound.arguments[name]

                _validate_string_is_not_blank(
                    value,
                    parameter_name=name,
                )

            return func(*bound.args, **bound.kwargs)

        return wrapper

    return decorator


def validate_string_is_not_blank(
    value: str,
    parameter_name: str,
) -> None:
    """Validate that a string is non-blank.

    Args:
        value: The string to validate.
        parameter_name: The name of the parameter being validated.

    Raises:
        NoneNotAllowedError: If the value is None.
        EmptyStringError: If the string is empty.
    """
    _validate_string_is_not_blank(
        value,
        parameter_name,
    )
