**Assigned To:** OpenAI Codex
**Task ID:** CODEX-20250831-002
**Title:** Implement a "Smart Task Router" Proof-of-Concept

**Objective:**
As a Senior Python Developer, your task is to create a proof-of-concept for a "Smart Task Router" to improve our internal collaboration, based on the research from Task C1.

**Task:**
1.  **Create a new Python module** at `eufm/app/services/task_router.py`.
2.  **Functionality:** The module should contain a function `route_task(prompt: str) -> str`. This function will perform a basic analysis of a user's prompt and suggest which agent in our task force is best suited to handle it.
3.  **Logic:** The routing logic can be simple for this proof-of-concept. For example:
    *   If the prompt contains keywords like "research," "find," "analyze," or "summarize," it should recommend "Perplexity Sonar".
    *   If the prompt contains keywords like "code," "implement," "refactor," or "script," it should recommend "OpenAI Codex" or "Jules AI".
    *   If the prompt contains keywords like "strategy," "review," "plan," or "supervise," it should recommend "Claude Code".
    *   If the prompt is about system operations or execution, it should recommend "Gemini CLI".

**Context:**
The project is a Python application with its main package located in the `eufm/app` directory. The new module should be placed within this structure.

**Deliverable:**
Submit your work as a single Pull Request against the `main` branch with the new `task_router.py` module.
