import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.services.agent_factory import AgentFactory
from app.utils.ai_services import AIServices
from app.agents.research_agent import ResearchAgent


def test_agent_factory_auto_selects_research():
    factory = AgentFactory(ai_services=AIServices(settings={}), base_config={})
    agent = factory.create_agent("auto", "agent-1", {"prompt": "research climate"})
    assert isinstance(agent, ResearchAgent)
