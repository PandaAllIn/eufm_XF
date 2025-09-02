"""Centralized interface for interacting with various AI services."""

import logging
from typing import Any

from openai import OpenAI

from app.exceptions import AIServiceError
from app.utils.services.perplexity_service import PerplexityService

logger = logging.getLogger(__name__)


class AIServices:
    def __init__(self, settings: Any):
        self.settings = settings
        self.perplexity_service = PerplexityService(
            api_key=self.settings.get("perplexity_api_key"),
            client_cls=OpenAI,
        )

    def query_jules_ai(self, prompt: str) -> str:
        """Sends a query to Jules AI and returns the response."""
        print(f"--- Querying Jules AI with prompt: {prompt[:50]}... ---")
        return "Response from Jules AI."

    def query_openai_codex(self, prompt: str, language: str = "python") -> str:
        """Sends a query to OpenAI Codex and returns the response."""
        print(
            f"--- Querying OpenAI Codex for {language} with prompt: {prompt[:50]}... ---"
        )
        return "Generated code from OpenAI Codex."

    def query_perplexity_sonar(
        self, prompt: str, model: str = "sonar-reasoning", max_tokens: Any = None
    ) -> str:
        """Sends a query to the Perplexity Sonar API and returns the content."""
        result = self.perplexity_service.query(
            prompt, model=model, max_tokens=max_tokens
        )
        if result["error"]:
            raise AIServiceError(result["error"], service_name="Perplexity Sonar")
        return result["content"]  # type: ignore[return-value]


def get_ai_services(settings: Any) -> AIServices:
    """Factory function to get an instance of AIServices."""
    return AIServices(settings)
