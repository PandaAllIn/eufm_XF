"""Smart Task Router proof-of-concept.

This module provides a simple keyword-based router that recommends
which agent in the task force should handle a user's request.
"""

from typing import Iterable
import hashlib
import json
from uuid import uuid4
from datetime import datetime

from config.logging import get_logger


logger = get_logger(__name__)


# Mapping of agent keys to keywords that should trigger them.
_ROUTING_TABLE = {
    "research": {"research", "find", "analyze", "summarize"},
    "document": {"document", "write", "draft", "edit"},
    "proposal": {"proposal", "strategy", "plan", "review"},
    "coordinator": {"coordinate", "system", "execute", "run"},
}


def route_task(prompt: str, run_id: Optional[str] = None, task_id: Optional[str] = None) -> str:
    """Suggest the most suitable agent for the given prompt and log the decision."""

    prompt_lower = prompt.lower()
    return any(keyword in prompt_lower for keyword in keywords)


def route_task(prompt: str) -> tuple[str, str]:
    """Suggest the most suitable agent for the given prompt.

    Args:
        prompt: The user's task description.

    Returns:
        Tuple of the recommended agent key and the routing reason.
    """

    prompt_lower = prompt.lower()
    for agent, keywords in _ROUTING_TABLE.items():
        matched = [kw for kw in keywords if kw in prompt_lower]
        if matched:
            return agent, f"Matched keywords: {', '.join(matched)}"

    # Fallback agent if nothing matches.
    return "document", "No keywords matched; using default"


def log_routing_decision(prompt: str, chosen_agent: str, reason: str) -> dict:
    """Log a routing decision and return the record."""

    record = {
        "run_id": str(uuid4()),
        "prompt_hash": hashlib.sha1(prompt.encode("utf-8")).hexdigest(),
        "chosen_agent": chosen_agent,
        "reason": reason,
        "ts": datetime.utcnow().isoformat(),
    }
    logger.info(json.dumps(record))
    return record
