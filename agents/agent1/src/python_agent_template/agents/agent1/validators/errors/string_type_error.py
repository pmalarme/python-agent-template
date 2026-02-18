"""Exception raised when a parameter is not a string."""

from __future__ import annotations


class StringTypeError(TypeError):
    """Raised when a parameter is not a string."""

    __slots__ = ()

    def __init__(self, parameter: str) -> None:
        """Initialize the error with parameter context."""
        message: str = f"param '{parameter}' must be str."
        super().__init__(message)
