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
