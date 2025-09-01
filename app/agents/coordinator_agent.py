import yaml
import re
from typing import Dict, Any
from app.agents.base_agent import BaseAgent
from config.settings import get_settings

from app.utils.journal import log_decision


class CoordinatorAgent(BaseAgent):
    """An agent responsible for project coordination and status checks."""

    def __init__(self, agent_id: str, config: Dict[str, Any]):
        super().__init__(agent_id, config)
        self.settings = get_settings()
        self.wbs_file_path = self.settings.app.WBS_DIR / "wbs.yaml"
        self.proposal_path = (
            self.settings.app.PROJECT_ROOT
            / "eufm"
            / "Stage1_Proposal_Cline_Enhanced.md"
        )
        self.wbs = self._load_wbs()
        self.proposal_content = self._load_proposal()
        log_decision("CoordinatorAgent initialized.")

    def _load_wbs(self):
        """Loads the WBS data from the YAML file."""
        try:
            with open(self.wbs_file_path, "r") as file:
                return yaml.safe_load(file)
        except FileNotFoundError as e:
            self.logger.error(f"WBS file not found at {self.wbs_file_path}: {e}")
            return None
        except yaml.YAMLError as e:
            self.logger.error(f"Error parsing WBS YAML file: {e}")
            return None

    def _load_proposal(self):
        """Loads the proposal markdown file."""
        try:
            with open(self.proposal_path, "r") as file:
                return file.read()
        except FileNotFoundError as e:
            self.logger.error(f"Proposal file not found at {self.proposal_path}: {e}")
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
            checklist += f"- [ ] {title.strip()}\n"

        checklist += "---------------------------------"
        return checklist

    def run(self, parameters: Dict[str, Any]) -> Any:
        """Runs the coordinator agent to perform a specific task."""
        task = parameters.get("task", "wbs_status")
        self.logger.info(f"Executing task: {task}")

        if task == "proposal_checklist":
            return self.create_proposal_checklist()
        return self.determine_next_task()
