"""Tests for blank string validator utilities."""

from __future__ import annotations

import pytest

from python_agent_template.agents.agent1.validators.blank_string_validator import (
    require_non_blank_strings,
    validate_string_is_not_blank,
)
from python_agent_template.agents.agent1.validators.errors import (
    EmptyStringError,
    MissingParameterError,
    NoneNotAllowedError,
    StringTypeError,
)


def test_validate_string_is_not_blank_accepts_non_blank() -> None:
    """Allows non-blank strings."""
    validate_string_is_not_blank("Ada", "name")


def test_validate_string_is_not_blank_rejects_none() -> None:
    """Raises when value is None."""
    with pytest.raises(NoneNotAllowedError, match="name"):
        validate_string_is_not_blank(None, "name")  # type: ignore[arg-type]


def test_validate_string_is_not_blank_rejects_empty() -> None:
    """Raises when string is empty."""
    with pytest.raises(EmptyStringError, match="name"):
        validate_string_is_not_blank("", "name")


def test_decorator_raises_missing_parameter() -> None:
    """Decorator raises when required arg is missing."""

    @require_non_blank_strings("first")  # type: ignore[untyped-decorator]
    def greet(*, first: str) -> str:
        return f"hi {first}"

    with pytest.raises(MissingParameterError, match="first"):
        greet()  # type: ignore[call-arg]


def test_decorator_rejects_none_and_non_string() -> None:
    """Decorator rejects None and non-string values."""

    @require_non_blank_strings("first", "last")  # type: ignore[untyped-decorator]
    def greet(first: str, last: str) -> str:
        return f"{first} {last}"

    with pytest.raises(NoneNotAllowedError, match="first"):
        greet(None, "Doe")  # type: ignore[arg-type]

    with pytest.raises(StringTypeError, match="last"):
        greet("John", 123)  # type: ignore[arg-type]


def test_decorator_rejects_blank_and_allows_deduped_order() -> None:
    """Decorator rejects blanks and dedupes parameter list order."""

    @require_non_blank_strings("first", "first", "last")  # type: ignore[untyped-decorator]
    def greet(first: str, last: str) -> str:
        return f"{first} {last}"

    with pytest.raises(EmptyStringError, match="first"):
        greet("   ", "Doe")

    assert greet("Ada", "Lovelace") == "Ada Lovelace"
