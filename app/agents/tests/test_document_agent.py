import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock

from app.agents.document_agent import DocumentAgent


class TestDocumentAgent(unittest.TestCase):
    def test_draft_outreach_emails_uses_ai_services(self):
        ai_services = SimpleNamespace()
        ai_services.chat_completion = AsyncMock(return_value="Hello")
        agent = DocumentAgent(agent_id="doc", config={}, ai_services=ai_services)
        emails = agent.draft_outreach_emails([{"organisation_name": "Org"}])
        self.assertEqual(emails, ["Hello"])
        ai_services.chat_completion.assert_called()


if __name__ == "__main__":
    unittest.main()
