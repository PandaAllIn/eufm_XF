from typing import Any, Dict, Optional, Type

from openai import OpenAI


class PerplexityService:
    """Service wrapper for interacting with the Perplexity Sonar API."""

    def __init__(
        self,
        api_key: Optional[str],
        base_url: str = "https://api.perplexity.ai",
        client_cls: Type[OpenAI] = OpenAI,
    ) -> None:
        self.client: Optional[OpenAI]
        if api_key:
            self.client = client_cls(api_key=api_key, base_url=base_url)
        else:  # pragma: no cover - simple guard
            self.client = None

    def query(
        self,
        prompt: str,
        model: str = "sonar-reasoning",
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Optional[str]]:
        """Query the Perplexity Sonar API."""
        if not self.client:
            return {"content": None, "error": "API key not configured"}

        messages = [
            {
                "role": "system",
                "content": "You are an expert research assistant for a Horizon Europe project.",
            },
            {"role": "user", "content": prompt},
        ]
        params: Dict[str, Any] = {"model": model, "messages": messages}
        if max_tokens is not None:
            params["max_tokens"] = max_tokens
        try:
            response = self.client.chat.completions.create(**params)
            content = response.choices[0].message.content
            return {"content": content, "error": None}
        except Exception as exc:  # pragma: no cover - depends on network
            return {"content": None, "error": str(exc)}
