import json
import logging

import pytest
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.agents.base_agent import BaseAgent, AgentStatus


class SuccessAgent(BaseAgent):
    def run(self, parameters):
        return "success"


class FailingAgent(BaseAgent):
    def run(self, parameters):
        raise RuntimeError("failure")


def test_execute_success(caplog):
    agent = SuccessAgent("test", {})
    with caplog.at_level(logging.INFO, logger="agent"):
        result = agent.execute({})
    assert result == "success"
    assert agent.status == AgentStatus.COMPLETED
    records = [json.loads(r.message) for r in caplog.records if r.name == "agent"]
    assert any(rec["event"] == "start" for rec in records)
    success = next(rec for rec in records if rec["event"] == "success")
    assert success["run_id"] == agent.run_id
    assert "task_id" in success


def test_execute_failure(caplog):
    agent = FailingAgent("test", {})
    with caplog.at_level(logging.INFO, logger="agent"):
        with pytest.raises(RuntimeError):
            agent.execute({})
    assert agent.status == AgentStatus.FAILED
    records = [json.loads(r.message) for r in caplog.records if r.name == "agent"]
    failure = next(rec for rec in records if rec["event"] == "failure")
    assert failure["error"] == "failure"
    assert failure["status"] == "failed"
