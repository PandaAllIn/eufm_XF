**Assigned To:** Jules AI
**Task ID:** JULES-AUTOGEN-03
**Title:** Implement AgentOrchestrator Service

**Objective:**
Create the service that schedules, executes, and tracks agent tasks using the TaskQueue and AgentTask model.

**Detailed Instructions:**
1.  Create `eufm/app/services/agent_orchestrator.py`.
2.  Define class `AgentOrchestrator` with constructor `__init__(self, ai_manager, max_concurrent_tasks: int = 5)` that sets up:
    *   an `AgentFactory` instance
    *   a `TaskQueue` instance
    *   a dictionary `active_tasks: Dict[str, asyncio.Task]`
    *   a `ThreadPoolExecutor` limited by `max_concurrent_tasks`
3.  Implement method `async create_task(self, agent_type: str, parameters: Dict[str, Any], priority: str = 'normal') -> AgentTask`:
    *   create and persist an `AgentTask` with `status=TaskStatus.QUEUED`
    *   enqueue the task ID via `TaskQueue`
    *   trigger `_process_queue`
4.  Implement private method `async _process_queue(self)` to launch queued tasks while concurrency allows.
5.  Implement private method `async _execute_task(self, task_id: str)` to:
    *   load `AgentTask` from the database
    *   update status to `RUNNING`
    *   create agent via `AgentFactory` and call `await agent.run(task.parameters)`
    *   store result and mark status `COMPLETED`, or on exception record `FAILED` and `error`
    *   remove task from `active_tasks` and continue processing the queue
6.  Implement `get_task_status(self, task_id: str) -> Optional[AgentTask]`.
7.  Implement `async cancel_task(self, task_id: str) -> bool` to cancel active or queued tasks.
8.  Implement `get_system_status(self) -> Dict[str, Any]` returning counts of active tasks, queue size, remaining capacity, and available agent types.
9.  Ensure appropriate logging statements for task lifecycle events.

**Context:**
Service modules live in `eufm/app/services`. This orchestrator will be called from Flask endpoints and must be fully asynchronous.

**Deliverable:**
Submit your work as a single Pull Request against `main` including the new service module.
