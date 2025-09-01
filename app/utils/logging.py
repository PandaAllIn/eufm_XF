import json
import logging
from typing import Optional


def log_event(
    run_id: str,
    task_id: str,
    agent_id: str,
    status: str,
    event: str,
    error: Optional[str] = None,
) -> None:
    """Emit a structured JSON log line for agent events."""
    record = {
        "run_id": run_id,
        "task_id": task_id,
        "agent_id": agent_id,
        "status": status,
        "event": event,
    }
    if error:
        record["error"] = error
    logging.getLogger("agent").info(json.dumps(record))
