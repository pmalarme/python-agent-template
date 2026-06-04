"""Minimal example agent to illustrate the template."""

from __future__ import annotations

from dataclasses import dataclass

from .validators.blank_string_validator import require_non_blank_strings


@dataclass
class AgentConfig:
    """Configuration for the example agent."""

    greeting: str = "hello"


class ExampleAgent:
    """Simple greeter agent."""

    def __init__(self, config: AgentConfig | None = None) -> None:
        """Initialize the agent with optional config."""
        self.config = config or AgentConfig()

    @require_non_blank_strings("name", use_partial_bind=False)
    def run(self, name: str) -> str:
        """Return a greeting for the provided name."""
        return f"{self.config.greeting}, {name}!"
