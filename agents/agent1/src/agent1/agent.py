"""Minimal example agent to illustrate the template."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AgentConfig:
    """Configuration for the example agent."""

    greeting: str = "hello"


class MissingNameError(ValueError):
    """Raised when a name argument is missing."""

    def __init__(self) -> None:
        """Initialize the missing-name error with a default message."""
        super().__init__("name required")


class ExampleAgent:
    """Simple greeter agent."""

    def __init__(self, config: AgentConfig | None = None) -> None:
        """Initialize the agent with optional config."""
        self.config = config or AgentConfig()

    def run(self, name: str) -> str:
        """Return a greeting for the provided name."""
        if not name:
            raise MissingNameError
        return f"{self.config.greeting}, {name}!"
