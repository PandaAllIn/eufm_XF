# EUFM Assistant - Architectural Design

## 1. Vision and Goals

The EUFM Assistant is a proactive, multi-agent AI system designed to support a small startup in managing a complex Horizon Europe research project. The primary goal is to automate and streamline project management tasks, including research, documentation, compliance monitoring, and reporting, thereby increasing the project's chances of success.

## 2. System Architecture

The system follows a **multi-agent architecture**, orchestrated by a central controller. This design allows for modularity, scalability, and clear separation of concerns.

### 2.1. Core Components

-   **Main Controller (`ai_assistant/main.py`):** The central entry point of the application. It parses command-line arguments, initializes the necessary agents, and orchestrates the overall workflow.
-   **Web Dashboard (`dashboard/app.py`):** A Flask-based web application that provides a user-friendly interface for interacting with the AI assistant. It allows users to trigger workflows, view results, and monitor project status.
-   **AI Agents (`agents/`):** A collection of specialized AI agents, each responsible for a specific task.

### 2.2. Technology Stack

-   **Backend:** Python 3.12
-   **AI/LLM Interaction:** OpenAI API (`openai` library)
-   **Web Framework:** Flask
-   **Dependency Management:** `pyproject.toml` and `pip`
-   **Data Serialization:** YAML (`pyyaml`) for configuration and project data.
-   **Code Quality:** `ruff` for linting and formatting.
-   **Testing:** `pytest` for unit and integration tests.

## 3. Agent Design

Each agent is a Python class designed to be autonomous and specialized.

### 3.1. Research Agent

-   **Purpose:** To conduct research on specific topics (e.g., finding potential project partners, gathering information on a scientific topic).
-   **Workflow:**
    1.  Receives a high-level research goal.
    2.  Uses an LLM to break down the goal into a multi-step research plan.
    3.  Executes the plan, which may involve using tools like web search (e.g., `google_search`, `view_text_website`).
    4.  Parses the search results to extract structured information.
    5.  Returns the structured data as its final output.

### 3.2. Document Agent

-   **Purpose:** To generate professional, context-aware documents.
-   **Workflow:**
    1.  Receives structured data from another agent (e.g., the Research Agent's output).
    2.  Receives a template or a goal for the document to be created (e.g., "draft an outreach email").
    3.  Reads the main project context document (`Horizon_Xilella.md`) to understand the project's goals and tone.
    4.  Uses an LLM to synthesize the information and draft the document.
    5.  Returns the final document text.

### 3.3. Coordinator Agent (Future)

-   **Purpose:** To act as the "project manager" agent, orchestrating the other agents to achieve high-level project goals.
-   **Workflow:**
    1.  Reads the project's Work Breakdown Structure (WBS) from `project_wbs.yaml`.
    2.  Identifies the current tasks and their requirements.
    3.  Delegates tasks to the appropriate specialized agents (e.g., tells the Research Agent to find partners for an upcoming work package).
    4.  Monitors the progress of tasks and manages the overall project state.

### 3.4. Monitor Agent

-   **Purpose:** To monitor project compliance and risks.
-   **Workflow:**
    1.  Reads the project WBS and a set of predefined compliance rules (`compliance_rules.yaml`).
    2.  Calculates a `compliance_score` based on the project's current state.
    3.  Displays the project status and compliance score on the web dashboard.

## 4. Data Management

-   **Project Proposal (`Horizon_Xilella.md`):** The primary knowledge base for the project's strategic goals, scientific background, and overall context. This document is used by agents to ensure their outputs are aligned with the project's mission.
-   **Work Breakdown Structure (`project_wbs.yaml`):** A structured YAML file that defines all work packages, tasks, deliverables, and timelines for the project. This file drives the project management logic.
-   **Configuration Files (`config.yaml`, `settings.yaml`):** Used for storing settings, API keys, and other configuration parameters.

## 5. Project Structure (Post-Refactoring)

The project has been refactored into a standard, installable Python package.

```
.
├── pyproject.toml
└── src
    └── eufm_assistant
        ├── agents
        │   ├── __init__.py
        │   ├── coordinator_agent.py
        │   ├── document_agent.py
        │   ├── monitor
        │   └── research_agent.py
        ├── ai_assistant
        │   ├── __init__.py
        │   └── main.py
        ├── dashboard
        │   ├── __init__.py
        │   ├── app.py
        │   ├── static
        │   └── templates
        └── docs
            ├── AGENTS.md
            ├── ARCHITECTURAL_DESIGN.md
            └── Horizon_Xilella.md
```

This structure ensures clean, absolute imports and aligns with best practices for Python project development.
