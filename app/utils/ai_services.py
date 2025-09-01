"""
This module provides a centralized interface for interacting with various AI services.
"""

import warnings
from typing import Any

from app.utils.services.perplexity_service import PerplexityService


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
        """Deprecated: use ``PerplexityService.query`` instead."""
        warnings.warn(
            "query_perplexity_sonar is deprecated; use PerplexityService.query",
            DeprecationWarning,
            stacklevel=2,
        )
        result = self.perplexity_service.query(
            prompt, model=model, max_tokens=max_tokens
        )
        if result["error"]:
            return f"Error: {result['error']}"
        return result["content"]


def get_ai_services(settings):
    """
    Factory function to get an instance of AIServices.
    """
    return AIServices(settings)
