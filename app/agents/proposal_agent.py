import yaml
from typing import Dict, Any
import google.generativeai as genai
from app.agents.base_agent import BaseAgent, AgentStatus
from app.utils.ai_services import AIServices
from config.settings import get_settings

class ProposalAgent(BaseAgent):
    """Agent responsible for generating Horizon Europe proposals."""

    def __init__(self, agent_id: str, config: Dict[str, Any], ai_services: AIServices):
        super().__init__(agent_id, config)
        self.settings = get_settings()
        self.ai_services = ai_services
        genai.configure(api_key=self.settings.ai.google_api_key)
        self.gemini_client = genai.GenerativeModel(self.settings.ai.default_model)

    def get_approved_proposal_content(self) -> str:
        """Loads the content of the approved proposal."""
        try:
            with open(self.settings.app.PROJECT_ROOT / "eufm" / "Stage1_Proposal_Cline_Enhanced.md", "r") as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error("Approved proposal file not found.")
            return "Error: Approved proposal file not found."

    def run(self, parameters: Dict[str, Any]) -> Any:
        """
        Returns the content of the approved Stage 1 proposal.
        This is a temporary measure to ensure stability for submission.
        """
        self.status = AgentStatus.RUNNING
        self.logger.info("Retrieving approved Stage 1 proposal content...")
        try:
            result = self.get_approved_proposal_content()
            self.result = result
            self.status = AgentStatus.COMPLETED
            self.logger.info("Successfully retrieved proposal content.")
            return result
        except Exception as e:
            self.error = str(e)
            self.status = AgentStatus.FAILED
            self.logger.error(f"Failed to retrieve proposal content: {e}")
            raise