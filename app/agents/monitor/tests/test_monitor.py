import unittest

from app.agents.monitor.monitor import calculate_compliance_score


class TestMonitor(unittest.TestCase):
    def setUp(self):
        self.sample_wbs_data = {
            "work_packages": [
                {
                    "id": "WP1",
                    "title": "Project Management",
                    "leader": "Alice",
                    "tasks": [
                        {
                            "name": "Task 1",
                            "end_date": "2099-12-31T00:00:00Z",
                            "status": "In Progress",
                        }
                    ],
                },
                {"id": "WP2", "title": "Research", "leader": "Bob", "tasks": []},
                {
                    "id": "WP3",
                    "title": "Development",
                    "leader": None,
                    "tasks": [
                        {
                            "name": "Task 2",
                            "end_date": "2023-01-01T00:00:00Z",
                            "status": "Pending",
                        }
                    ],
                },
            ]
        }

    def test_calculate_compliance_score(self):
        self.assertEqual(calculate_compliance_score(self.sample_wbs_data), 81)

    def test_calculate_compliance_score_no_data(self):
        self.assertEqual(calculate_compliance_score(None), 0)
        self.assertEqual(calculate_compliance_score({}), 0)
