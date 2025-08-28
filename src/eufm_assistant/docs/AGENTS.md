# EUFM Assistant Agent Instructions

This document provides guidance for AI agents working on the EUFM Assistant project.

## Project Structure

The project is structured as a standard Python package. All source code is located in the `src/eufm_assistant` directory.

- `src/eufm_assistant/agents/`: Contains the core logic for the different AI agents (e.g., `research_agent.py`, `document_agent.py`).
- `src/eufm_assistant/ai_assistant/`: Contains the main orchestrator and entry point for the AI assistant (`main.py`).
- `src/eufm_assistant/dashboard/`: Contains the Flask web application for the user-facing dashboard.
- `src/eufm_assistant/docs/`: Contains all project documentation, including this file, the architectural design, and the core project proposal.

## Development Workflow

1.  **Installation:** The project uses `pyproject.toml` for dependency management. To install the project and its dependencies, run `pip install -e .` from the root directory.
2.  **Imports:** All Python imports must be absolute, following the `src/eufm_assistant` root. For example, to import the research agent in `main.py`, use `from eufm_assistant.agents import research_agent`.
3.  **Testing:** The primary tests for the monitor agent are located in `src/eufm_assistant/agents/monitor/tests/`. Run tests using `pytest` from the root directory.

## Agent Responsibilities

- **Research Agent:** Responsible for conducting research based on high-level goals. It can use web search tools to find information and should return structured data.
- **Document Agent:** Responsible for creating documents, such as outreach emails or reports, based on structured data provided by other agents. It should use the project's core documentation (e.g., `Horizon_Xilella.md`) for context.
- **Coordinator Agent (To Be Implemented):** This will be the central agent responsible for orchestrating the other agents to achieve complex project goals based on the Work Breakdown Structure (WBS) defined in `project_wbs.yaml`.
- **Monitor Agent:** Responsible for compliance and risk monitoring based on the project's WBS and a set of predefined rules.
