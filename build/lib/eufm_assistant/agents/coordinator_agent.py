import yaml
import re
import pathlib

# The project root is 3 levels up from this file's directory
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[3]


class CoordinatorAgent:
    def __init__(self, wbs_file_path=None, proposal_path=None):
        """
        Initializes the CoordinatorAgent.
        """
        self.wbs_file_path = wbs_file_path or PROJECT_ROOT / "wbs" / "wbs.yaml"
        self.proposal_path = proposal_path or PROJECT_ROOT / "Horizon_Xilella.md"
        self.wbs = self._load_wbs()
        self.proposal_content = self._load_proposal()

    def _load_wbs(self):
        """Loads the WBS data from the YAML file."""
        try:
            with open(self.wbs_file_path, "r") as file:
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
            with open(self.proposal_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            print(f"Error: Proposal file not found at {self.proposal_path}")
            return ""

    def determine_next_task(self):
        """
        Determines the next high-level task based on the current state of the WBS.
        """
        if not self.wbs or "wbs" not in self.wbs:
            return "WBS is not loaded or is in an invalid format. Cannot determine next task."

        wbs_data = self.wbs.get("wbs", {})

        for wp_id, items in wbs_data.items():
            if not items:
                return f"Next Action: Define tasks for Work Package '{wp_id}'."

        return "All work packages seem to have tasks defined. Project is on track."

    def create_proposal_checklist(self):
        """
        Parses the proposal document and creates a checklist of sections.
        """
        if not self.proposal_content:
            return "Proposal document not loaded. Cannot create checklist."

        headers = re.findall(
            r"^(Part\s+[IVX]+:.*|^\d+\.\d+\s+.*)", self.proposal_content, re.MULTILINE
        )
        if not headers:
            return "No headers found in the proposal document."

        checklist = "--- Proposal Section Checklist ---\n"
        for title in headers:
            indent = "  " if not title.strip().startswith("Part") else ""
            checklist += f"{indent}- [ ] {title.strip()}\n"

        checklist += "---------------------------------"
        return checklist

    def run(self, task="wbs_status"):
        """
        Runs the coordinator agent to perform a specific task.
        """
        if task == "proposal_checklist":
            result = self.create_proposal_checklist()
        else:
            result = self.determine_next_task()

        return result
