from openai import OpenAI
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent, AgentStatus
from config.settings import get_settings
from app.exceptions import ValidationError, AgentExecutionError

class DocumentAgent(BaseAgent):
    """An agent for drafting documents, such as outreach emails."""

    def __init__(self, agent_id: str, config: Dict[str, Any]):
        super().__init__(agent_id, config)
        self.settings = get_settings()
        self.client = OpenAI(api_key=self.settings.ai.openai_api_key)
        self.knowledge_base_path = self.settings.app.PROJECT_ROOT / "eufm" / "Horizon_Xilella.md"

    def get_project_context(self) -> str:
        try:
            with open(self.knowledge_base_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            self.logger.error(f"Knowledge base file not found at {self.knowledge_base_path}")
            return "Project context not found."

    def draft_outreach_emails(self, partner_data: List[Dict[str, Any]]) -> List[str]:
        project_context = self.get_project_context()
        emails = []
        for partner in partner_data:
            prompt = f"""
            You are a professional project manager for a Horizon Europe project focused on curing Xylella fastidiosa.
            Your task is to draft a personalized outreach email to a potential collaborator.
            **Project Context:**
            {project_context[:4000]}...
            **Collaborator Information:**
            - Organisation: {partner.get("organisation_name", "N/A")}
            - Country: {partner.get("country", "N/A")}
            - Relevant Project: {partner.get("project_title", "N/A")} ({partner.get("project_acronym", "N/A")})
            - Summary: {partner.get("summary", "N/A")}
            - Contact Person: {partner.get("contact_person", "N/A")}
            **Instructions:**
            - The email should be formal, professional, and concise.
            - It should introduce our project and express interest in their work.
            - It should highlight the synergy between our project and their previous work on {partner.get("project_acronym", "their relevant project")}.
            - The goal is to initiate a conversation about potential collaboration.
            - Address the email to the contact person if available, otherwise use a generic greeting.
            """
            response = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a project manager drafting outreach emails."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
            )
            email_content = response.choices[0].message.content
            emails.append(email_content)
        return emails

    def run(self, parameters: Dict[str, Any]) -> Any:
        """
        Runs the document agent. Expects 'partner_data' in parameters.
        """
        self.status = AgentStatus.RUNNING
        partner_data = parameters.get("partner_data")
        if not partner_data or not isinstance(partner_data, list):
            self.error = "Missing or invalid 'partner_data' parameter."
            self.status = AgentStatus.FAILED
            self.logger.error(
                f"{ValidationError.__name__}: {self.error}"
            )
            raise ValidationError(self.error)

        self.logger.info(f"Drafting outreach emails for {len(partner_data)} partner(s).")
        
        try:
            result = self.draft_outreach_emails(partner_data)
            self.result = result
            self.status = AgentStatus.COMPLETED
            self.logger.info("Successfully drafted outreach emails.")
            return result
        except Exception as e:  # pragma: no cover - network errors not deterministic
            self.error = str(e)
            self.status = AgentStatus.FAILED
            self.logger.error(
                f"Failed to draft emails: {e.__class__.__name__}: {e}"
            )
            raise AgentExecutionError(
                f"Failed to draft outreach emails: {e}",
                agent_type="document",
                agent_id=self.agent_id,
            ) from e
