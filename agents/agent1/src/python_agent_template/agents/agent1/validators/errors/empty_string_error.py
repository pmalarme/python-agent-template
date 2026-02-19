"""Exception raised for empty string values."""

from __future__ import annotations


class EmptyStringError(ValueError):
    """Raised when a string is empty after trimming whitespace."""

    __slots__ = ()

    def __init__(self, parameter: str) -> None:
        """Initialize the error with parameter context."""
        message: str = f"param '{parameter}' must be non-empty."
        super().__init__(message)
