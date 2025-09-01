from abc import ABC, abstractmethod
from enum import Enum
import logging
from typing import Any, Dict, Optional

from app.utils.telemetry import telemetry_logger

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

    def execute(
        self,
        parameters: Dict[str, Any],
        run_id: Optional[str] = None,
        task_id: Optional[str] = None,
    ) -> Any:
        """Execute the agent with telemetry and status management."""
        self.status = AgentStatus.RUNNING
        self.on_start()
        telemetry_logger.log(
            run_id=run_id,
            task_id=task_id,
            agent_id=self.agent_id,
            event_type="start",
            status=self.status.value,
        )
        try:
            self.result = self.run(parameters)
            self.status = AgentStatus.COMPLETED
            self.on_success()
            telemetry_logger.log(
                run_id=run_id,
                task_id=task_id,
                agent_id=self.agent_id,
                event_type="success",
                status=self.status.value,
            )
            return self.result
        except Exception as exc:  # pragma: no cover - simple wrapper
            self.status = AgentStatus.FAILED
            self.error = str(exc)
            self.on_failure(exc)
            telemetry_logger.log(
                run_id=run_id,
                task_id=task_id,
                agent_id=self.agent_id,
                event_type="failure",
                status=self.status.value,
                error=self.error,
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

    def execute(self, parameters: Dict[str, Any]) -> Any:
        """Public method to execute the agent with lifecycle hooks."""
        try:
            self.on_start()
            result = self.run(parameters)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure(e)
            raise
