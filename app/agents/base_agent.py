from abc import ABC, abstractmethod
from typing import Dict, Any
import logging
from enum import Enum
from uuid import uuid4
from datetime import datetime

from app.utils.logging import log_event


class AgentStatus(Enum):
    IDLE = "idle"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BaseAgent(ABC):
    """Abstract base class for all AI agents in the EUFM system."""

    def __init__(self, agent_id: str, config: Dict[str, Any]):
        self.agent_id = agent_id
        self.config = config
        self.status = AgentStatus.IDLE
        self.result: Any = None
        self.error: str | None = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.run_id = str(uuid4())
        self.started_at: datetime | None = None
        self.ended_at: datetime | None = None
        self.duration_ms: int | None = None

    @abstractmethod
    def run(self, parameters: Dict[str, Any]) -> Any:
        """The main entry point for the agent's execution logic."""
        pass

    def on_start(self):
        """Lifecycle hook called when the agent starts running."""
        pass

    def on_success(self):
        """Lifecycle hook called when the agent completes successfully."""
        pass

    def on_failure(self, error: Exception):
        """Lifecycle hook called when the agent fails."""
        pass

    def execute(self, parameters: Dict[str, Any]) -> Any:
        """Wraps the run method with lifecycle hooks and logging."""
        task_id = str(uuid4())
        self.status = AgentStatus.RUNNING
        self.started_at = datetime.utcnow()
        log_event(self.run_id, task_id, self.agent_id, self.status.value, "start")
        self.on_start()

        try:
            params_with_ids = {**parameters, "run_id": self.run_id, "task_id": task_id}
            result = self.run(params_with_ids)
            self.result = result
            self.status = AgentStatus.COMPLETED
            self.ended_at = datetime.utcnow()
            self.duration_ms = int(
                (self.ended_at - self.started_at).total_seconds() * 1000
            )
            self.on_success()
            log_event(self.run_id, task_id, self.agent_id, self.status.value, "success")
            return result
        except Exception as e:  # pragma: no cover - re-raise after logging
            self.error = str(e)
            self.status = AgentStatus.FAILED
            self.ended_at = datetime.utcnow()
            self.duration_ms = int(
                (self.ended_at - self.started_at).total_seconds() * 1000
            )
            self.on_failure(e)
            log_event(
                self.run_id,
                task_id,
                self.agent_id,
                self.status.value,
                "failure",
                self.error,
            )
            raise

    def get_status(self) -> Dict[str, Any]:
        """Returns the current status and result of the agent."""
        return {
            "agent_id": self.agent_id,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
        }
