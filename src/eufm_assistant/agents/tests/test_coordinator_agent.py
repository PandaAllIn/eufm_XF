import unittest
from unittest.mock import patch
from eufm_assistant.agents.coordinator_agent import CoordinatorAgent

class TestCoordinatorAgent(unittest.TestCase):

    @patch('eufm_assistant.agents.coordinator_agent.CoordinatorAgent._load_wbs')
    def test_determine_next_task_find_partner(self, mock_load_wbs):
        """
        Tests that the agent correctly identifies the need to find a partner
        for a WP with a 'TBD' leader.
        """
        mock_wbs_data = {
            'work_packages': [
                {'id': 'WP1', 'title': 'Management', 'leader': 'Alice', 'tasks': [{'name': 'Task 1'}]},
                {'id': 'WP7', 'title': 'Ethics and Data Management', 'leader': 'TBD', 'tasks': []}
            ]
        }
        mock_load_wbs.return_value = mock_wbs_data

        agent = CoordinatorAgent()
        agent.wbs = mock_wbs_data # Directly set wbs for testing

        expected_action = "Next Action: Find a partner for Work Package 'WP7: Ethics and Data Management'."
        self.assertEqual(agent.determine_next_task(), expected_action)

    @patch('eufm_assistant.agents.coordinator_agent.CoordinatorAgent._load_wbs')
    def test_determine_next_task_define_tasks(self, mock_load_wbs):
        """
        Tests that the agent correctly identifies the need to define tasks
        when all leaders are assigned but a WP has an empty task list.
        """
        mock_wbs_data = {
            'work_packages': [
                {'id': 'WP1', 'title': 'Management', 'leader': 'Alice', 'tasks': [{'name': 'Task 1'}]},
                {'id': 'WP2', 'title': 'Research', 'leader': 'Bob', 'tasks': []}
            ]
        }
        mock_load_wbs.return_value = mock_wbs_data

        agent = CoordinatorAgent()
        agent.wbs = mock_wbs_data

        expected_action = "Next Action: Define tasks for Work Package 'WP2: Research'."
        self.assertEqual(agent.determine_next_task(), expected_action)

    @patch('eufm_assistant.agents.coordinator_agent.CoordinatorAgent._load_wbs')
    def test_determine_next_task_all_ok(self, mock_load_wbs):
        """
        Tests that the agent correctly identifies that the project is on track
        when all WPs have leaders and tasks.
        """
        mock_wbs_data = {
            'work_packages': [
                {'id': 'WP1', 'title': 'Management', 'leader': 'Alice', 'tasks': [{'name': 'Task 1'}]},
                {'id': 'WP2', 'title': 'Research', 'leader': 'Bob', 'tasks': [{'name': 'Task 2'}]}
            ]
        }
        mock_load_wbs.return_value = mock_wbs_data

        agent = CoordinatorAgent()
        agent.wbs = mock_wbs_data

        expected_action = "All work packages have leaders and tasks defined. Project is on track."
        self.assertEqual(agent.determine_next_task(), expected_action)

    @patch('eufm_assistant.agents.coordinator_agent.CoordinatorAgent._load_proposal')
    @patch('eufm_assistant.agents.coordinator_agent.CoordinatorAgent._load_wbs')
    def test_create_proposal_checklist(self, mock_load_wbs, mock_load_proposal):
        """
        Tests that the agent can correctly parse a markdown proposal
        and create a checklist.
        """
        mock_load_wbs.return_value = {} # WBS not needed for this test

        mock_proposal_content = (
            "Part I: The Vision\n"
            "1.1 The Problem\n"
            "1.2 The Solution\n"
            "Part II: The Plan\n"
            "2.1 The Team\n"
        )
        mock_load_proposal.return_value = mock_proposal_content

        agent = CoordinatorAgent()

        expected_checklist = (
            "--- Proposal Section Checklist ---\n"
            "- [ ] Part I: The Vision\n"
            "  - [ ] 1.1 The Problem\n"
            "  - [ ] 1.2 The Solution\n"
            "- [ ] Part II: The Plan\n"
            "  - [ ] 2.1 The Team\n"
            "---------------------------------"
        )
        self.assertEqual(agent.create_proposal_checklist(), expected_checklist)

if __name__ == '__main__':
    unittest.main()
