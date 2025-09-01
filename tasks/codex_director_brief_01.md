**Assigned To:** OpenAI Codex
**Task ID:** CODEX-DIRECTOR-20250831-01
**Title:** Act as AI Tech Lead: Decompose the Sonar Refactoring Plan into Actionable Tasks for Jules AI

**Objective:**
You are the AI Tech Lead for the EUFM project. Your primary input is the expert-level refactoring plan located at `eufm/docs/system_optimization_plan.md`.

Your mission is to act as a project manager and create a series of detailed, atomic, and actionable tasks for a junior-to-mid-level AI Software Engineer named Jules. Jules is proficient in Python and Flask but requires very specific instructions.

**Your Task:**
1.  **Analyze the Plan:** Thoroughly read and understand the `system_optimization_plan.md` document.
2.  **Decompose the Work:** Break down the "Agent Orchestration and Task Management" section of the plan into 3 to 6 logical, sequential tasks. Each task should represent a single, mergeable unit of work.
3.  **Generate Task Files:** For each task you've identified, create a new, separate Markdown file in the `eufm/tasks/` directory. Name them sequentially: `jules_task_autogen_01.md`, `jules_task_autogen_02.md`, etc.

**Requirements for Each Task File:**
*   **Clear Title:** A descriptive title for the task.
*   **Specific Objective:** A one-sentence summary of what the task should accomplish.
*   **Detailed Instructions:** Provide step-by-step instructions. This should include the exact file paths to create or modify, the specific classes and methods to implement, and even high-level code snippets or pseudocode where appropriate.
*   **Context:** Remind Jules of the project's structure (e.g., "All new code should be in the `eufm/app` directory").
*   **Deliverable:** Clearly state that the deliverable is a single Pull Request against the `main` branch.

**Example of a good task you might create for Jules:**
*   **Title:** Implement Database Models for Agent Tasks
*   **Objective:** Create the SQLAlchemy models required to store agent task information in the database.
*   **Instructions:**
    1.  Create a new file at `eufm/app/models/agent_task.py`.
    2.  In this file, define a new SQLAlchemy model class named `AgentTask`.
    3.  The model should include columns for `id`, `agent_type`, `status`, `parameters` (as a JSON field), `result` (as a JSON field), `created_at`, and `updated_at`.
    4.  Ensure the model inherits from the `BaseModel` in `eufm/app/models/base.py`.