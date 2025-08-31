**Assigned To:** Jules AI
**Task ID:** JULES-AUTOGEN-04
**Title:** Expose Agent Task Management API Endpoints

**Objective:**
Provide REST endpoints that allow clients to create, monitor, cancel, and inspect agent tasks through the AgentOrchestrator.

**Detailed Instructions:**
1.  Create `eufm/app/api/agent_tasks.py` defining a Flask `Blueprint` named `agent_tasks_bp`.
2.  Implement the following routes:
    *   `POST /agent-tasks` → parse JSON for `agent_type`, `parameters`, optional `priority`; call `await app.agent_orchestrator.create_task(...)`; return `{"task_id": <id>}`.
    *   `GET /agent-tasks/<task_id>` → return serialized task status from `get_task_status`.
    *   `POST /agent-tasks/<task_id>/cancel` → invoke `cancel_task`; return success flag.
    *   `GET /agent-tasks/system-status` → return `get_system_status` dictionary.
3.  Since Flask view functions are synchronous, wrap orchestrator calls with `asyncio.run` or use `async` views if the project uses `Quart` or Flask async support.
4.  Register the blueprint in `eufm/app/__init__.py` after app creation (e.g., `app.register_blueprint(agent_tasks_bp, url_prefix="/api")`).
5.  Document each endpoint with docstrings explaining request and response structures.

**Context:**
API modules live under `eufm/app/api`. The orchestrator instance should be accessible via `app.agent_orchestrator` or similar initialization in `create_app`.

**Deliverable:**
Submit your work as a single Pull Request against `main` including the new API module and the updated application factory.
