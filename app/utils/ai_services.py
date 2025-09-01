"""Centralized interface for interacting with various AI services."""

import logging
from openai import OpenAI
from app.exceptions import AIServiceError

logger = logging.getLogger(__name__)

class AIServices:
    def __init__(self, settings):
        self.settings = settings

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
        print(f"--- Querying OpenAI Codex for {language} with prompt: {prompt[:50]}... ---")
        # In a real implementation, this would make an API call to OpenAI Codex.
        return "Generated code from OpenAI Codex."

    def query_perplexity_sonar(self, prompt, model="sonar-deep-research"):
        """
        Sends a query to the Perplexity Sonar API and returns the response.
        """
        print(f"--- Querying Perplexity Sonar ({model}) with prompt: {prompt[:50]}... ---")

        client = OpenAI(
            api_key=self.settings.get("perplexity_api_key"),
            base_url="https://api.perplexity.ai",
        )
        
        messages = [
            {"role": "system", "content": "You are an expert research assistant for a Horizon Europe project."},
            {"role": "user", "content": prompt},
        ]
        
        try:
            response = client.chat.completions.create(
                model=model,
                messages=messages,
            )
            return response.choices[0].message.content
        except Exception as e:  # pragma: no cover - network errors not deterministic
            logger.error(
                f"Error querying Perplexity Sonar: {e.__class__.__name__}: {e}"
            )
            raise AIServiceError(
                "Could not get a response from Perplexity Sonar", "Perplexity Sonar"
            ) from e

def get_ai_services(settings):
    """
    Factory function to get an instance of AIServices.
    """
    return AIServices(settings)
