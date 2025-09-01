import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock

from app.agents.research_agent import ResearchAgent


class TestResearchAgent(unittest.TestCase):
    def test_generate_research_plan_uses_ai_services(self):
        ai_services = SimpleNamespace()
        ai_services.query_perplexity_sonar = AsyncMock(return_value='{"steps": []}')
        agent = ResearchAgent(agent_id="res", config={}, ai_services=ai_services)
        plan = agent.generate_research_plan("test")
        self.assertEqual(plan, [])
        ai_services.query_perplexity_sonar.assert_called()


if __name__ == "__main__":
    unittest.main()
