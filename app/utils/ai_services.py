"""Central asynchronous interface for external AI services."""

from __future__ import annotations

import asyncio
import warnings
from typing import Any, Sequence

import google.generativeai as genai
from openai import AsyncOpenAI

from config.settings import get_settings, Settings



class AIServices:
    """Wrapper around third party AI providers.

    The class exposes async methods so agents can await calls when running
    inside an event loop. Synchronous agents may use ``asyncio.run`` to invoke
    these helpers.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._openai = AsyncOpenAI(api_key=self.settings.ai.openai_api_key)
        self._perplexity = AsyncOpenAI(
            api_key=self.settings.ai.perplexity_api_key,
            base_url="https://api.perplexity.ai",
        )
        genai.configure(api_key=self.settings.ai.google_api_key)
        self._gemini_model = self.settings.ai.default_model

    async def chat_completion(
        self,
        messages: Sequence[dict[str, str]],
        model: str | None = None,
        **kwargs: Any,
    ) -> str:
        """Query OpenAI's chat completion endpoint."""
        chosen_model = model or "gpt-4-turbo"
        response = await self._openai.chat.completions.create(
            model=chosen_model, messages=list(messages), **kwargs
        )
        return response.choices[0].message.content

    async def generate_gemini_content(self, prompt: str, **kwargs: Any) -> str:
        """Generate content using Google's Gemini models."""
        model = genai.GenerativeModel(self._gemini_model)
        # Gemini client is synchronous; run in a thread for async support.
        return await asyncio.to_thread(
            lambda: model.generate_content(prompt, **kwargs).text
        )

    async def query_perplexity_sonar(
        self, prompt: str, model: str = "sonar-deep-research"
    ) -> str:
        """Send a query to the Perplexity Sonar API."""
        messages = [
            {
                "role": "system",
                "content": "You are an expert research assistant for a Horizon Europe project.",
            },
            {"role": "user", "content": prompt},
        ]
        response = await self._perplexity.chat.completions.create(
            model=model, messages=messages
        )
        return response.choices[0].message.content

    # ------------------------------------------------------------------
    # Legacy helpers
    # ------------------------------------------------------------------
    def query_openai_codex(
        self, *args: Any, **kwargs: Any
    ) -> str:  # pragma: no cover - deprecated
        warnings.warn(
            "query_openai_codex is deprecated; use chat_completion instead",
            DeprecationWarning,
            stacklevel=2,
        )
        return "Generated code from OpenAI Codex."  # placeholder

    def query_jules_ai(
        self, *args: Any, **kwargs: Any
    ) -> str:  # pragma: no cover - deprecated
        warnings.warn(
            "query_jules_ai is deprecated and will be removed",
            DeprecationWarning,
            stacklevel=2,
        )
        return "Response from Jules AI."


def get_ai_services(settings: Settings | None = None) -> AIServices:
    """Factory for :class:`AIServices`. Reads settings if not provided."""
    return AIServices(settings)
