import pytest

from app.cli import main as cli_main
from app.agents.base_agent import BaseAgent
from app.services.agent_factory import AgentFactory


class DummyAgent(BaseAgent):
    def run(self, parameters):
        return "done"


def test_help(capsys):
    with pytest.raises(SystemExit):
        cli_main.main(["--help"])
    out = capsys.readouterr().out
    assert "Unified CLI for EUFM Assistant" in out


def test_route_command(capsys):
    cli_main.main(["route", "research something"])
    out = capsys.readouterr().out
    assert "Perplexity Sonar" in out


def test_run_agent_invokes_execute(monkeypatch, capsys):
    def fake_create_agent(self, agent_type, agent_id, agent_config=None):
        return DummyAgent(agent_id, {})

    monkeypatch.setattr(AgentFactory, "create_agent", fake_create_agent)
    cli_main.main(["run-agent", "dummy"])
    out = capsys.readouterr().out
    assert "done" in out
