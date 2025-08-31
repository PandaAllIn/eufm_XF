"""Smart Task Router proof-of-concept.

This module provides a simple keyword-based router that recommends
which agent in the task force should handle a user's request.
"""

from typing import Iterable


# Mapping of agent names to keywords that should trigger them.
_ROUTING_TABLE = {
    "Perplexity Sonar": {"research", "find", "analyze", "summarize"},
    "OpenAI Codex": {"code", "implement", "refactor", "script"},
    "Claude Code": {"strategy", "review", "plan", "supervise"},
    "Gemini CLI": {"system", "operations", "execute", "run"},
}


def _contains_keyword(prompt: str, keywords: Iterable[str]) -> bool:
    """Check if any keyword appears in the prompt.

    The comparison is case-insensitive.
    """

    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in keywords)


def route_task(prompt: str) -> str:
    """Suggest the most suitable agent for the given prompt.

    Args:
        prompt: The user's task description.

    Returns:
        The name of the recommended agent.
    """

    for agent, keywords in _ROUTING_TABLE.items():
        if _contains_keyword(prompt, keywords):
            return agent

    # Fallback agent if nothing matches.
    return "OpenAI Codex"
