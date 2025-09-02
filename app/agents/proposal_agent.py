import asyncio
import warnings
from typing import Dict, Any

from app.agents.base_agent import BaseAgent, AgentStatus
from app.utils.ai_services import AIServices, get_ai_services
from config.settings import get_settings
from config.logging import log_event



class ProposalAgent(BaseAgent):
    """Agent responsible for generating Horizon Europe proposals."""

    def __init__(
        self,
        agent_id: str,
        config: Dict[str, Any],
        ai_services: AIServices | None = None,
    ):
        super().__init__(agent_id, config)
        self.settings = get_settings()
        self.ai_services = ai_services or get_ai_services(self.settings)

    def get_approved_proposal_content(self) -> str:
        """Loads the content of the approved proposal."""
        try:
            with open(
                self.settings.app.PROJECT_ROOT
                / "eufm"
                / "Stage1_Proposal_Cline_Enhanced.md",
                "r",
            ) as f:
                return f.read()
        except FileNotFoundError:
            log_event(
                self.logger,
                logging.ERROR,
                "AGENT_ERROR",
                "Approved proposal file not found.",
                error_code="PROPOSAL_NOT_FOUND",
            )
            return "Error: Approved proposal file not found."

    async def generate_proposal_outline(self, prompt: str) -> str:
        return await self.ai_services.generate_gemini_content(prompt)

    def generate_proposal_outline_direct(
        self, prompt: str
    ) -> str:  # pragma: no cover - deprecated
        warnings.warn(
            "generate_proposal_outline_direct is deprecated; use generate_proposal_outline",
            DeprecationWarning,
            stacklevel=2,
        )
        return asyncio.run(self.generate_proposal_outline(prompt))

    def run(self, parameters: Dict[str, Any]) -> Any:
        """
        Returns the content of the approved Stage 1 proposal.
        This is a temporary measure to ensure stability for submission.
        """
        self.status = AgentStatus.RUNNING
        run_id = parameters.get("run_id")
        task_id = parameters.get("task_id")
        log_event(
            self.logger,
            logging.INFO,
            "AGENT_START",
            "Retrieving approved Stage 1 proposal content...",
            run_id,
            task_id,
        )
        try:
            result = self.get_approved_proposal_content()
            self.result = result
            self.status = AgentStatus.COMPLETED
            log_event(
                self.logger,
                logging.INFO,
                "AGENT_SUCCESS",
                "Successfully retrieved proposal content.",
                run_id,
                task_id,
            )
            return result
        except Exception as e:
            self.error = str(e)
            self.status = AgentStatus.FAILED
            self.logger.error(f"Failed to retrieve proposal content: {e}")
            raise
