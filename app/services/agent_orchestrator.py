"""Agent task orchestration and status broadcasting."""

from __future__ import annotations

import asyncio
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import logging
from typing import Any, Deque, Dict, Optional

try:
    from flask_socketio import SocketIO
except Exception:  # pragma: no cover - fallback if socketio not installed
    SocketIO = Any  # type: ignore

from app.services.agent_factory import AgentFactory


class TaskStatus(Enum):
    """Enumeration of possible task states."""

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class AgentTask:
    """Simple in-memory representation of an agent task."""

    id: str
    agent_name: str
    parameters: Dict[str, Any]
    status: TaskStatus = TaskStatus.QUEUED
    progress: float = 0.0
    message: str = ""
    result: Any | None = None
    error: str | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class AgentOrchestrator:
    """Coordinates agent task execution and broadcasts status updates."""

    def __init__(
        self,
        ai_manager: Any,
        socketio: Optional[SocketIO] = None,
        max_concurrent_tasks: int = 5,
    ) -> None:
        self.ai_manager = ai_manager
        self.socketio = socketio
        self.agent_factory = AgentFactory(ai_manager, {})
        self.task_queue: asyncio.Queue[str] = asyncio.Queue()
        self.active_tasks: Dict[str, asyncio.Task] = {}
        self.max_concurrent_tasks = max_concurrent_tasks
        self.executor = ThreadPoolExecutor(max_workers=max_concurrent_tasks)
        self.logger = logging.getLogger(__name__)
        self.tasks: Dict[str, AgentTask] = {}
        self.status_history: Deque[Dict[str, Any]] = deque(maxlen=200)

    async def create_task(
        self,
        agent_type: str,
        parameters: Dict[str, Any],
        priority: str = "normal",
    ) -> AgentTask:
        """Create a new task and enqueue it for execution."""
        task_id = str(len(self.tasks) + 1)
        task = AgentTask(id=task_id, agent_name=agent_type, parameters=parameters)
        self.tasks[task_id] = task
        await self.task_queue.put(task_id)
        await self._broadcast_status(task, "task queued")
        await self._process_queue()
        return task

    async def _process_queue(self) -> None:
        """Launch queued tasks while respecting concurrency limits."""
        while (
            len(self.active_tasks) < self.max_concurrent_tasks
            and not self.task_queue.empty()
        ):
            task_id = await self.task_queue.get()
            coro = self._execute_task(task_id)
            self.active_tasks[task_id] = asyncio.create_task(coro)

    async def _execute_task(self, task_id: str) -> None:
        """Execute a single queued task."""
        task = self.tasks.get(task_id)
        if not task:
            return
        try:
            task.status = TaskStatus.RUNNING
            await self._broadcast_status(task, "task started")

            agent = self.agent_factory.create_agent(
                task.agent_name, agent_id=task_id, agent_config={}
            )
            loop = asyncio.get_running_loop()
            result = await loop.run_in_executor(
                self.executor, agent.run, task.parameters
            )
            task.result = result
            task.status = TaskStatus.COMPLETED
            task.progress = 1.0
            await self._broadcast_status(task, "task completed")
        except Exception as exc:  # pragma: no cover - defensive
            task.status = TaskStatus.FAILED
            task.error = str(exc)
            await self._broadcast_status(task, f"task failed: {exc}")
        finally:
            self.active_tasks.pop(task_id, None)
            await self._process_queue()

    async def cancel_task(self, task_id: str) -> bool:
        """Cancel a running or queued task."""
        if task_id in self.active_tasks:
            self.active_tasks[task_id].cancel()
        task = self.tasks.get(task_id)
        if task and task.status in {TaskStatus.QUEUED, TaskStatus.RUNNING}:
            task.status = TaskStatus.CANCELLED
            await self._broadcast_status(task, "task cancelled")
            return True
        return False

    def get_task_status(self, task_id: str) -> Optional[AgentTask]:
        """Return current status for a task."""
        return self.tasks.get(task_id)

    def get_status_history(self) -> list[Dict[str, Any]]:
        """Return recent status updates for consumers."""
        return list(self.status_history)

    def get_system_status(self) -> Dict[str, Any]:
        """Return high-level system metrics."""
        return {
            "active_tasks": len(self.active_tasks),
            "queue_size": self.task_queue.qsize(),
            "available_capacity": self.max_concurrent_tasks - len(self.active_tasks),
            "agent_types": self.agent_factory.list_available_agents(),
        }

    async def _broadcast_status(
        self, task: AgentTask, message: str, progress: Optional[float] = None
    ) -> None:
        """Emit a status update via Socket.IO and record it."""
        if progress is not None:
            task.progress = progress
        task.message = message
        task.updated_at = datetime.utcnow()
        payload = {
            "task_id": task.id,
            "agent": task.agent_name,
            "status": task.status.value,
            "progress": task.progress,
            "message": task.message,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat(),
        }
        self.status_history.append(payload)
        if self.socketio:
            self.socketio.emit("agent_status_update", payload, namespace="/ws")
