import pytest

from app.exceptions import (
    ConfigurationError,
    ValidationError,
    AgentExecutionError,
    AIServiceError,
)
from app.services.agent_factory import AgentFactory
from app.agents.research_agent import ResearchAgent
from app.utils.ai_services import AIServices
from app.utils import ai_services as ai_module


def test_agent_factory_unknown_type_raises_configuration_error():
    factory = AgentFactory(ai_services=AIServices({}), base_config={})
    with pytest.raises(ConfigurationError):
        factory.create_agent("unknown", "agent-1")


def test_research_agent_missing_query_raises_validation_error():
    agent = ResearchAgent(agent_id="r1", config={}, ai_services=AIServices({}))
    with pytest.raises(ValidationError):
        agent.run({})


def test_query_perplexity_sonar_raises_ai_service_error(monkeypatch):
    services = AIServices({"perplexity_api_key": "key"})

    class DummyClient:
        class chat:
            class completions:
                @staticmethod
                def create(*args, **kwargs):
                    raise RuntimeError("boom")

    monkeypatch.setattr(ai_module, "OpenAI", lambda *args, **kwargs: DummyClient())

    with pytest.raises(AIServiceError):
        services.query_perplexity_sonar("prompt")


def test_research_agent_ai_service_failure_raises_agent_execution_error():
    class FailingAIServices(AIServices):
        def query_perplexity_sonar(self, *args, **kwargs):
            raise AIServiceError("down", service_name="Perplexity Sonar")

    agent = ResearchAgent(agent_id="r1", config={}, ai_services=FailingAIServices({}))
    with pytest.raises(AgentExecutionError):
        agent.run({"query": "test"})
