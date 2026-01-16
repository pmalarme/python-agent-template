"""CLI entry point for agent1."""

from __future__ import annotations

import argparse
import logging

from python_agent_template.agents.agent1.agent import AgentConfig, ExampleAgent

logger = logging.getLogger(__name__)


def main() -> None:
    """Parse arguments and emit a greeting."""
    parser = argparse.ArgumentParser(description="Run agent1 example.")
    parser.add_argument("name", help="Name to greet")
    parser.add_argument("--greeting", default="hello", help="Greeting prefix")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")
    agent = ExampleAgent(config=AgentConfig(greeting=args.greeting))
    logger.info(agent.run(args.name))


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
