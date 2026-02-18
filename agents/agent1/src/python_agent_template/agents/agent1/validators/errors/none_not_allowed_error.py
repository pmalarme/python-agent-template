"""Exception raised when None is not allowed for a parameter."""

from __future__ import annotations


class NoneNotAllowedError(TypeError):
    """Raised when a parameter is None but disallowed."""

    __slots__ = ()

    def __init__(self, parameter: str) -> None:
        """Initialize the error with parameter context."""
        message: str = f"param '{parameter}' cannot be None."
        super().__init__(message)
