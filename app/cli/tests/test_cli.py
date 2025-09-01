import json
from typing import Dict, Any

import pytest

from app.cli.main import main
from app.agents.base_agent import BaseAgent
from app.services.agent_factory import AgentFactory


class DummyAgent(BaseAgent):
    def run(self, parameters: Dict[str, Any]) -> Any:  # type: ignore[override]
        return {"received": parameters}


def dummy_create_agent(self, agent_type: str, agent_id: str, agent_config=None):  # type: ignore[override]
    return DummyAgent(agent_id, agent_config or {})


def test_help_message(capsys):
    with pytest.raises(SystemExit):
        main(["--help"])
    captured = capsys.readouterr()
    assert "Unified command-line interface" in captured.out


def test_route_subcommand(capsys):
    main(["route", "find collaborators"])
    captured = capsys.readouterr()
    assert "Perplexity Sonar" in captured.out


def test_run_agent_subcommand(monkeypatch, capsys):
    monkeypatch.setattr(AgentFactory, "create_agent", dummy_create_agent)
    params = json.dumps({"query": "test"})
    main(["run-agent", "research", "--params", params])
    captured = capsys.readouterr()
    assert "query" in captured.out
