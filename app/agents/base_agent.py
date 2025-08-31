from abc import ABC, abstractmethod
from typing import Dict, Any
import logging
from enum import Enum

class AgentStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

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

    def get_status(self) -> Dict[str, Any]:
        """Returns the current status and result of the agent."""
        return {
            "agent_id": self.agent_id,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
        }
