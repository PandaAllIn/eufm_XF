**Assigned To:** Jules AI
**Task ID:** JULES-AUTOGEN-02
**Title:** Build Asynchronous TaskQueue Utility

**Objective:**
Provide a priority-aware queue to manage pending agent tasks before execution.

**Detailed Instructions:**
1.  Create a new file at `eufm/app/utils/task_queue.py`.
2.  Implement a `TaskQueue` class using `asyncio.PriorityQueue`.
    *   Method `__init__(self)` should initialize an internal `PriorityQueue`.
    *   Method `async enqueue(self, task_id: str, priority: str)` should map priority strings (`'high'`, `'normal'`, `'low'`) to numerical values and put `(priority_value, task_id)` into the queue.
    *   Method `async dequeue(self) -> Optional[str]` should return the next `task_id` or `None` if the queue is empty.
    *   Method `size(self) -> int` should return the current queue size.
3.  Include docstrings and type hints for all methods.
4.  Update `eufm/app/utils/__init__.py` to export `TaskQueue`.

**Context:**
Utilities live under `eufm/app/utils`. This queue will be consumed by the upcoming `AgentOrchestrator` service.

**Deliverable:**
Submit your work as a single Pull Request against the `main` branch including the new utility module and package export.
