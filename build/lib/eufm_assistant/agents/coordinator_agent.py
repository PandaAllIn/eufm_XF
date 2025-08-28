import yaml

class CoordinatorAgent:
    def __init__(self, wbs_file_path='src/eufm_assistant/docs/project_wbs.yaml'):
        """
        Initializes the CoordinatorAgent.

        Args:
            wbs_file_path (str): The path to the Work Breakdown Structure YAML file.
        """
        self.wbs_file_path = wbs_file_path
        self.wbs = self._load_wbs()

    def _load_wbs(self):
        """Loads the WBS data from the YAML file."""
        try:
            with open(self.wbs_file_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            print(f"Error: WBS file not found at {self.wbs_file_path}")
            return None
        except yaml.YAMLError as e:
            print(f"Error parsing WBS YAML file: {e}")
            return None

    def determine_next_task(self):
        """
        Determines the next high-level task based on the current state of the WBS.

        Returns:
            str: A string describing the suggested next action.
        """
        if not self.wbs or 'work_packages' not in self.wbs:
            return "WBS is not loaded or is invalid. Cannot determine next task."

        # Rule 1: Find a leader for any work package where the leader is 'TBD'.
        for wp in self.wbs['work_packages']:
            if wp.get('leader') == 'TBD':
                return f"Next Action: Find a partner for Work Package '{wp['id']}: {wp['title']}'."

        # Rule 2: If all leaders are defined, check for empty task lists.
        for wp in self.wbs['work_packages']:
            if not wp.get('tasks'): # Check for empty list or missing key
                return f"Next Action: Define tasks for Work Package '{wp['id']}: {wp['title']}'."

        # If all rules pass, the project is well-defined for now.
        return "All work packages have leaders and tasks defined. Project is on track."

    def run(self):
        """
        Runs the coordinator agent to determine and report the next course of action.
        """
        print("CoordinatorAgent is running...")
        next_action = self.determine_next_task()
        print("--- Coordinator Agent Analysis ---")
        print(next_action)
        print("---------------------------------")
        return next_action
