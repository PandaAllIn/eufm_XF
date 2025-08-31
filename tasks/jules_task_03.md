**Assigned To:** Jules AI
**Task ID:** JULES-20250831-003
**Title:** Enhance the `BaseAgent` Class

**Objective:**
As a Senior Software Engineer, your task is to enhance the core agent abstraction for smoother interaction and better status tracking.

**Task:**
Modify the `eufm/app/agents/base_agent.py` file to include:
1.  More detailed `AgentStatus` enums. The current enums are `IDLE`, `RUNNING`, `COMPLETED`, `FAILED`. Please add `QUEUED` and `CANCELLED`.
2.  Lifecycle hooks. Add the following abstract methods to the `BaseAgent` class, which can be overridden by subclasses:
    *   `on_start(self)`
    *   `on_success(self)`
    *   `on_failure(self, error: Exception)`

**Context:**
The `BaseAgent` class is an abstract base class that all other agents inherit from. These changes should be backward-compatible with the existing agents.

**Deliverable:**
Submit your work as a single Pull Request against the `main` branch with the modified `base_agent.py` file.
