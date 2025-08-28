import yaml
import re

class CoordinatorAgent:
    def __init__(self, wbs_file_path='src/eufm_assistant/docs/project_wbs.yaml', proposal_path='src/eufm_assistant/docs/Horizon_Xilella.md'):
        """
        Initializes the CoordinatorAgent.
        """
        self.wbs_file_path = wbs_file_path
        self.proposal_path = proposal_path
        self.wbs = self._load_wbs()
        self.proposal_content = self._load_proposal()

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

    def _load_proposal(self):
        """Loads the proposal markdown file."""
        try:
            with open(self.proposal_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: Proposal file not found at {self.proposal_path}")
            return ""

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

    def create_proposal_checklist(self):
        """
        Parses the proposal document and creates a checklist of sections.
        It looks for lines starting with 'Part [Roman Numeral]:' or 'd.d ' as section headers.
        """
        if not self.proposal_content:
            return "Proposal document not loaded. Cannot create checklist."

        # Regex to find headers like "Part I: ..." or "1.1 ..."
        headers = re.findall(r'^(Part\s+[IVX]+:.*|^\d+\.\d+\s+.*)', self.proposal_content, re.MULTILINE)

        if not headers:
            return "No headers found in the proposal document."

        checklist = "--- Proposal Section Checklist ---\n"
        for title in headers:
            # Simple indentation for now, can be improved if header levels are needed
            indent = ""
            if title.strip().startswith("Part"):
                indent = ""
            else:
                indent = "  "
            checklist += f"{indent}- [ ] {title.strip()}\n"

        checklist += "---------------------------------"
        return checklist

    def run(self, task='wbs_status'):
        """
        Runs the coordinator agent to perform a specific task.

        Args:
            task (str): The task to perform. Can be 'wbs_status' or 'proposal_checklist'.
        """
        print(f"CoordinatorAgent running task: {task}")

        if task == 'proposal_checklist':
            checklist = self.create_proposal_checklist()
            print(checklist)
            return checklist

        # Default to 'wbs_status'
        next_action = self.determine_next_task()
        print(f"--- Coordinator Agent Analysis ---")
        print(next_action)
        print("---------------------------------")
        return next_action
