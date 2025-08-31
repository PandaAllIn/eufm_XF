**Assigned To:** Jules AI
**Task ID:** JULES-20250831-001
**Title:** Design and Implement the "Project Journal" (Long-Term Memory)

**Objective:**
As an expert AI Systems Architect, your task is to design and implement a system that provides our AI Task Force with a shared long-term memory and a clear, auditable project history. This is critical for maintaining context across different sessions and agents.

**Component 1: The Project Journal (Long-Term Memory)**
1.  **Design:** Create a specification for a structured Markdown file named `PROJECT_JOURNAL.md` in the project root (`eufm/`). This journal will be the single source of truth for our strategic decisions. It should contain sections for:
    *   `Last Known Status`: A brief summary of the project's state.
    *   `Active Strategic Goals`: What are the high-level objectives we are currently working on?
    *   `Key Decisions Log`: A timestamped log of important decisions made (e.g., "Decided to use Poetry for dependency management").
    *   `Open Questions & Blockers`: What are the current challenges or questions we need to address?
2.  **Implement:** Create a new Python script at `eufm/app/utils/journal.py`. This script should contain functions to programmatically interact with the journal, such as:
    *   `log_decision(message: str)`
    *   `update_status(status: str)`
    *   `add_blocker(blocker: str)`

**Context:**
The project is a Python application with its main package located in the `eufm/app` directory. All new Python code should be placed within this structure. Configuration is managed via `eufm/config/settings.py`.

**Deliverable:**
Submit your work as a single Pull Request against the `main` branch on the GitHub repository. The PR should include the new `PROJECT_JOURNAL.md` file and the `journal.py` script.
