"""Tests for ExampleAgent."""

import pytest

from agent1 import AgentConfig, ExampleAgent
from agent1.agent import MissingNameError


def test_run_greets_name() -> None:
    """Agent returns greeting with provided name."""
    agent = ExampleAgent(AgentConfig(greeting="hi"))
    assert agent.run("Ada") == "hi, Ada!"


def test_run_requires_name() -> None:
    """Agent raises when name is missing."""
    agent = ExampleAgent()
    with pytest.raises(MissingNameError, match="name"):
        agent.run("")
