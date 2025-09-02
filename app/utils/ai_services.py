"""Centralized interface for interacting with various AI services."""

from openai import OpenAI
from app.utils.horizon_guide import query_guide


class AIServices:
    def __init__(self, settings: Any):
        self.settings = settings
        self.perplexity_service = PerplexityService(
            api_key=self.settings.get("perplexity_api_key")
        )

    def query_jules_ai(self, prompt):
        """
        Sends a query to Jules AI and returns the response.
        (Placeholder implementation)
        """
        print(f"--- Querying Jules AI with prompt: {prompt[:50]}... ---")
        # In a real implementation, this would make an API call to Jules AI.
        return "Response from Jules AI."

    def query_openai_codex(self, prompt, language="python"):
        """
        Sends a query to OpenAI Codex and returns the response.
        (Placeholder implementation)
        """
        print(
            f"--- Querying OpenAI Codex for {language} with prompt: {prompt[:50]}... ---"
        )
        # In a real implementation, this would make an API call to OpenAI Codex.
        return "Generated code from OpenAI Codex."

    def query_perplexity_sonar(self, prompt, model="sonar-reasoning", max_tokens=None):
        """Sends a query to the Perplexity Sonar API and returns the response."""
        result = self.perplexity_service.query(
            prompt, model=model, max_tokens=max_tokens
        )
        if result["error"]:
            raise AIServiceError(result["error"], service_name="Perplexity Sonar")
        return result["content"]


    def query_programme_guide(self, topic: str) -> str:
        """Search the Horizon Europe Programme Guide summary for a topic."""
        return query_guide(topic)

def get_ai_services(settings):
    """
    Factory function to get an instance of AIServices.
    """
    return AIServices(settings)