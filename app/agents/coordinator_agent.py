import logging
import yaml
import re
from typing import Dict, Any
from app.agents.base_agent import BaseAgent, AgentStatus
from config.settings import get_settings
from config.logging import log_event

from app.utils.journal import log_decision
from app.exceptions import AgentExecutionError


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
            log_event(
                self.logger,
                logging.ERROR,
                "AGENT_ERROR",
                f"WBS file not found at {self.wbs_file_path}: {e}",
                error_code="WBS_NOT_FOUND",
            )
            return None
        except yaml.YAMLError as e:
            log_event(
                self.logger,
                logging.ERROR,
                "AGENT_ERROR",
                f"Error parsing WBS YAML file: {e}",
                error_code="WBS_PARSE_ERROR",
            )
            return None

    def _load_proposal(self):
        """Loads the proposal markdown file."""
        try:
            with open(self.proposal_path, "r") as file:
                return file.read()
        except FileNotFoundError as e:
            log_event(
                self.logger,
                logging.ERROR,
                "AGENT_ERROR",
                f"Proposal file not found at {self.proposal_path}: {e}",
                error_code="PROPOSAL_NOT_FOUND",
            )
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
        """
        Runs the coordinator agent to perform a specific task.
        Supported tasks: 'wbs_status', 'proposal_checklist'
        """
        self.status = AgentStatus.RUNNING
        run_id = parameters.get("run_id")
        task_id = parameters.get("task_id")
        task = parameters.get("task", "wbs_status")
        log_event(
            self.logger,
            logging.INFO,
            "AGENT_START",
            f"Executing task: {task}",
            run_id,
            task_id,
        )

        try:
            if task == "proposal_checklist":
                result = self.create_proposal_checklist()
            else:
                result = self.determine_next_task()

            self.result = result
            self.status = AgentStatus.COMPLETED
            log_event(
                self.logger,
                logging.INFO,
                "AGENT_SUCCESS",
                f"Task '{task}' completed successfully.",
                run_id,
                task_id,
            )
            return result
        except Exception as e:
            self.error = str(e)
            self.status = AgentStatus.FAILED
            log_event(
                self.logger,
                logging.ERROR,
                "AGENT_ERROR",
                f"Task '{task}' failed: {e}",
                run_id,
                task_id,
                error_code="TASK_FAILED",
            )
            raise
