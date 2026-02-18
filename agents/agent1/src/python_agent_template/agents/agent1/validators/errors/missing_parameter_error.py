"""Exception raised when a required parameter is missing."""

from __future__ import annotations


class MissingParameterError(TypeError):
    """Raised when a required parameter is missing."""

    __slots__ = ()

    def __init__(self, parameter: str, func_name: str) -> None:
        """Initialize the error with parameter context."""
        super().__init__(f"{func_name}(): missing param '{parameter}'.")
