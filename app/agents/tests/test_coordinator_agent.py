import unittest
from unittest.mock import patch

from app.agents.coordinator_agent import CoordinatorAgent


class TestCoordinatorAgent(unittest.TestCase):
    @patch(
        "app.agents.coordinator_agent.CoordinatorAgent._load_proposal", return_value=""
    )
    @patch("app.agents.coordinator_agent.CoordinatorAgent._load_wbs")
    def test_determine_next_task_wbs_logic(self, mock_load_wbs, _mock_load_proposal):
        """
        Tests that the agent correctly identifies the need to define tasks
        when a WP has an empty task list in the new WBS format.
        """
        mock_wbs_data = {
            "wbs": {"WP1": [{"id": "T1.1", "title": "Task 1.1"}], "WP2": []}
        }
        mock_load_wbs.return_value = mock_wbs_data

        agent = CoordinatorAgent("c1", {})
        agent.wbs = mock_wbs_data

        expected_action = "Next Action: Define tasks for Work Package 'WP2'."
        self.assertEqual(agent.determine_next_task(), expected_action)

    @patch("app.agents.coordinator_agent.CoordinatorAgent._load_proposal")
    @patch("app.agents.coordinator_agent.CoordinatorAgent._load_wbs", return_value={})
    def test_create_proposal_checklist(self, _mock_load_wbs, mock_load_proposal):
        """
        Tests that the agent can correctly parse a markdown proposal
        and create a checklist.
        """
        mock_proposal_content = (
            "Part I: The Vision\n"
            "1.1 The Problem\n"
            "1.2 The Solution\n"
            "Part II: The Plan\n"
            "2.1 The Team\n"
        )
        mock_load_proposal.return_value = mock_proposal_content

        agent = CoordinatorAgent("c1", {})

        expected_checklist = (
            "--- Proposal Section Checklist ---\n"
            "- [ ] Part I: The Vision\n"
            "- [ ] 1.1 The Problem\n"
            "- [ ] 1.2 The Solution\n"
            "- [ ] Part II: The Plan\n"
            "- [ ] 2.1 The Team\n"
            "---------------------------------"
        )
        self.assertEqual(agent.create_proposal_checklist(), expected_checklist)


if __name__ == "__main__":
    unittest.main()
