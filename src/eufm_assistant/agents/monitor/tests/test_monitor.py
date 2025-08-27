import unittest
from unittest.mock import patch
import yaml
from eufm_assistant.agents.monitor.monitor import calculate_compliance_score

class TestMonitor(unittest.TestCase):

    def setUp(self):
        self.sample_wbs_data = {
            'work_packages': [
                {'id': 'WP1', 'title': 'Project Management', 'leader': 'Alice', 'tasks': [{'name': 'Task 1', 'end_date': '2099-12-31T00:00:00Z', 'status': 'In Progress'}]},
                {'id': 'WP2', 'title': 'Research', 'leader': 'Bob', 'tasks': []},
                {'id': 'WP3', 'title': 'Development', 'leader': None, 'tasks': [{'name': 'Task 2', 'end_date': '2023-01-01T00:00:00Z', 'status': 'Pending'}]}
            ]
        }

    def test_calculate_compliance_score(self):
        """
        Tests the compliance score calculation with a mix of compliant and non-compliant data.
        """
        # Let's re-calculate the expected score based on the logic in monitor.py
        #
        # WP1:
        # - base: 1, leader: 1, tasks: 1 = 3 points
        # - task1: not overdue = 1 point
        # - WP1 total = 4
        # - WP1 possible = 3 (base) + 1 (task) = 4
        #
        # WP2:
        # - base: 1, leader: 1, tasks: 1 = 3 points
        # - WP2 total = 3
        # - WP2 possible = 3 (base) = 3
        #
        # WP3:
        # - base: 1, leader: 0, tasks: 1 = 2 points
        # - task2: overdue = 0 points
        # - WP3 total = 2
        # - WP3 possible = 3 (base) + 1 (task) = 4
        #
        # Totals:
        # - current_score = 4 + 3 + 2 = 9
        # - total_possible_score = 4 + 3 + 4 = 11
        # - percentage = (9 / 11) * 100 = 81.81... -> int() = 81
        wbs_data = self.sample_wbs_data
        score = calculate_compliance_score(wbs_data)
        self.assertEqual(score, 81)

    def test_calculate_compliance_score_no_data(self):
        """
        Tests that the score is 0 if no data is provided.
        """
        score = calculate_compliance_score(None)
        self.assertEqual(score, 0)
        score = calculate_compliance_score({})
        self.assertEqual(score, 0)

if __name__ == '__main__':
    unittest.main()
