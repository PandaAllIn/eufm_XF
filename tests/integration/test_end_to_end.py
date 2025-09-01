from typing import Any, Dict

import pytest

from app.services.task_router import route_task
from app.services.agent_factory import AgentFactory


class DummyAIServices:
    """Stub implementation of AIServices for testing."""

    def query_perplexity_sonar(
        self, prompt: str, model: str = "sonar-reasoning"
    ) -> str:
        return '{"steps": [{"tool": "google_search", "query": "test"}]}'


ROUTER_TO_AGENT_TYPE = {
    "Perplexity Sonar": "research",
    "OpenAI Codex": "document",
    "Claude Code": "proposal",
    "Gemini CLI": "coordinator",
}


@pytest.fixture
def ai_services() -> DummyAIServices:
    return DummyAIServices()


@pytest.fixture
def telemetry() -> list[Dict[str, Any]]:
    return []


@pytest.fixture
def agent_factory(ai_services: DummyAIServices) -> AgentFactory:
    return AgentFactory(ai_services=ai_services, base_config={})


def _attach_telemetry(agent, telemetry, run_id: str, task_id: str) -> None:
    original_info = agent.logger.info
    original_error = agent.logger.error

    def info_with_telemetry(msg: str, *args, **kwargs):
        category = "complete" if "completed" in msg else "start"
        telemetry.append(
            {
                "run_id": run_id,
                "task_id": task_id,
                "event_category": category,
                "message": msg,
            }
        )
        original_info(msg, *args, **kwargs)

    def error_with_telemetry(msg: str, *args, **kwargs):
        telemetry.append(
            {
                "run_id": run_id,
                "task_id": task_id,
                "event_category": "error",
                "message": msg,
            }
        )
        original_error(msg, *args, **kwargs)

    agent.logger.info = info_with_telemetry  # type: ignore
    agent.logger.error = error_with_telemetry  # type: ignore


def test_research_agent_end_to_end_success(agent_factory: AgentFactory, telemetry):
    prompt = "Please research partners in Italy"
    routed = route_task(prompt)
    assert routed == "Perplexity Sonar"

    agent_type = ROUTER_TO_AGENT_TYPE[routed]
    agent = agent_factory.create_agent(agent_type, agent_id="agent-1")

    run_id, task_id = "run-123", "task-456"
    _attach_telemetry(agent, telemetry, run_id, task_id)

    result = agent.run({"query": "bioresources"})

    assert isinstance(result, list)
    status = agent.get_status()
    assert status["status"] == "completed"

    assert telemetry and telemetry[-1]["event_category"] == "complete"
    assert telemetry[-1]["run_id"] == run_id
    assert telemetry[-1]["task_id"] == task_id


def test_research_agent_end_to_end_failure(agent_factory: AgentFactory, telemetry):
    prompt = "Please research partners in Spain"
    routed = route_task(prompt)
    assert routed == "Perplexity Sonar"

    agent_type = ROUTER_TO_AGENT_TYPE[routed]
    agent = agent_factory.create_agent(agent_type, agent_id="agent-2")

    run_id, task_id = "run-789", "task-000"
    _attach_telemetry(agent, telemetry, run_id, task_id)

    with pytest.raises(ValueError):
        agent.run({})

    status = agent.get_status()
    assert status["status"] == "failed"
    assert telemetry[-1]["event_category"] == "error"
    assert telemetry[-1]["run_id"] == run_id
    assert telemetry[-1]["task_id"] == task_id
