"""Smart Task Router proof-of-concept.

This module provides a simple keyword-based router that recommends
which agent in the task force should handle a user's request.
"""

import hashlib
from typing import Optional

from app.utils.telemetry import telemetry_logger


# Mapping of agent names to keywords that should trigger them.
_ROUTING_TABLE = {
    "Perplexity Sonar": {"research", "find", "analyze", "summarize"},
    "OpenAI Codex": {"code", "implement", "refactor", "script"},
    "Claude Code": {"strategy", "review", "plan", "supervise"},
    "Gemini CLI": {"system", "operations", "execute", "run"},
}


def route_task(prompt: str, run_id: Optional[str] = None, task_id: Optional[str] = None) -> str:
    """Suggest the most suitable agent for the given prompt and log the decision."""

    prompt_lower = prompt.lower()
    chosen_agent = "OpenAI Codex"
    reason = "no keyword matched"
    for agent, keywords in _ROUTING_TABLE.items():
        for keyword in keywords:
            if keyword in prompt_lower:
                chosen_agent = agent
                reason = f"keyword '{keyword}'"
                break
        if chosen_agent == agent and reason != "no keyword matched":
            break

    prompt_hash = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    telemetry_logger.log(
        run_id=run_id,
        task_id=task_id,
        agent_id=None,
        event_type="router_decision",
        prompt_hash=prompt_hash,
        chosen_agent=chosen_agent,
        reason=reason,
    )
    return chosen_agent
