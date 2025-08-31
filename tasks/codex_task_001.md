**Assigned To:** OpenAI Codex
**Task ID:** CODEX-20250831-001
**Title:** Research and Implement a "Synergy & Upgrade" Proof-of-Concept

**Objective:**
As an AI Workflow Specialist and Senior Python Developer, your task is to research how different AI models and agents can work together more effectively and then implement a proof-of-concept for a "Smart Task Router" to improve our internal collaboration.

**Phase 1: Research**
1.  **Sources:** Conduct a thorough search on developer forums and communities, with a focus on:
    *   Reddit (specifically r/LocalLLaMA, r/LangChain, r/GPT3)
    *   Hacker News
    *   Other relevant software engineering blogs or communities.
2.  **Topics:** Your research should focus on patterns and techniques for:
    *   Multi-agent collaboration between different LLMs (e.g., workflows combining Claude, Gemini, and OpenAI models).
    *   AI agent orchestration frameworks (e.g., AutoGen, CrewAI).
    *   "Agent Router" or "Task Dispatcher" patterns, where a primary agent decides which specialized agent is best suited for a given task.
3.  **Deliverable (Research):** Create a new Markdown file at `eufm/docs/multi_agent_research.md` summarizing your findings. The summary should include links to the most insightful discussions and an analysis of the most promising techniques for our project.

**Phase 2: Proof-of-Concept Implementation**
1.  **Task:** Based on your research, create a new Python module at `eufm/app/services/task_router.py`.
2.  **Functionality:** The module should contain a function `route_task(prompt: str) -> str`. This function will perform a basic analysis of a user's prompt and suggest which agent in our task force is best suited to handle it.
3.  **Logic:** The routing logic can be simple for this proof-of-concept. For example:
    *   If the prompt contains keywords like "research," "find," "analyze," or "summarize," it should recommend "Perplexity Sonar".
    *   If the prompt contains keywords like "code," "implement," "refactor," or "script," it should recommend "OpenAI Codex" or "Jules AI".
    *   If the prompt contains keywords like "strategy," "review," "plan," or "supervise," it should recommend "Claude Code".
    *   If the prompt is about system operations or execution, it should recommend "Gemini CLI".

**Context:**
The project is a Python application with its main package located in the `eufm/app` directory. The new module should be placed within this structure.

**Deliverable (Implementation):**
Submit your work as a single Pull Request against the `main` branch. The PR should include the new `multi_agent_research.md` file and the `task_router.py` module.
