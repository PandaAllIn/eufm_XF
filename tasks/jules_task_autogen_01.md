**Assigned To:** Jules AI
**Task ID:** JULES-AUTOGEN-01
**Title:** Implement AgentTask Model and TaskStatus Enum

**Objective:**
Create the SQLAlchemy model and enumeration needed to persist and track agent task execution.

**Detailed Instructions:**
1.  Create a new file at `eufm/app/models/agent_task.py`.
2.  Define an `Enum` named `TaskStatus` with members: `QUEUED`, `RUNNING`, `COMPLETED`, `FAILED`, `CANCELLED`.
3.  Define a model class `AgentTask` inheriting from the project's base SQLAlchemy model (`db.Model` or `BaseModel`). Include columns:
    *   `id` (UUID primary key)
    *   `agent_type` (string)
    *   `parameters` (JSON)
    *   `result` (JSON, nullable)
    *   `status` (`TaskStatus`)
    *   `priority` (string, default `'normal'`)
    *   `error` (text, nullable)
    *   `created_at` and `updated_at` timestamps
4.  Implement a `save(self) -> None` method that commits the record and a `to_dict(self) -> dict` helper for serialization.
5.  Update `eufm/app/models/__init__.py` to export `AgentTask` and `TaskStatus`.

**Context:**
All models reside under `eufm/app/models`. The application uses Flask and SQLAlchemy; follow existing patterns for session management.

**Deliverable:**
Submit your work as a single Pull Request against the `main` branch including the new model file and updated package exports.
