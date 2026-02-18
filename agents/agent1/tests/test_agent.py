"""Tests for ExampleAgent."""

import pytest

from python_agent_template.agents.agent1 import AgentConfig, ExampleAgent
from python_agent_template.agents.agent1.validators.errors import EmptyStringError


def test_run_greets_name() -> None:
    """Agent returns greeting with provided name."""
    agent = ExampleAgent(AgentConfig(greeting="hi"))
    assert agent.run("Ada") == "hi, Ada!"


def test_run_requires_name() -> None:
    """Agent raises when name is missing."""
    agent = ExampleAgent()
    with pytest.raises(EmptyStringError, match="name"):
        agent.run("")


def test_run_rejects_whitespace_only_name() -> None:
    """Agent validates whitespace-only names via decorator guard."""
    agent = ExampleAgent()
    with pytest.raises(EmptyStringError, match="name"):
        agent.run("   ")
