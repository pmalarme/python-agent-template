"""Tests for ExampleAgent."""

import pytest

from agent1 import AgentConfig, ExampleAgent


def test_run_greets_name() -> None:
    """Agent returns greeting with provided name."""
    agent = ExampleAgent(AgentConfig(greeting="hi"))
    assert agent.run("Ada") == "hi, Ada!"


def test_run_requires_name() -> None:
    """Agent raises when name is missing."""
    agent = ExampleAgent()
    with pytest.raises(ValueError, match="name"):
        agent.run("")
