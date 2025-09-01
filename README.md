# EUFM Assistant

## Project Overview
The EUFM Assistant is a multi-agent system designed to streamline preparation of Horizon Europe proposals.
It automates project documentation, partner research, and monitoring so teams can focus on strategy rather than administration.

## Features
- **Proposal generation** for draft submissions and documentation.
- **Multi-agent collaboration** coordinating research, drafting, and monitoring tasks.
- **Research agent** for partner and data discovery.
- **Monitoring tools** to track deadlines and project health.
- **Extensible architecture** built with Python and Flask.
- **Centralized structured logging** with event categories and optional error codes for improved observability.

## Architecture Diagram
```
eufm/
├── app/               # Core application package
│   ├── agents/        # Research, proposal, and monitor agents
│   ├── api/           # REST API endpoints
│   ├── models/        # Database models
│   └── services/      # Business logic
├── config/            # Configuration files
├── docs/              # Project documentation
├── scripts/           # Utility scripts
└── launch_eufm.py     # Entry point for the web dashboard
```

## Getting Started
1. **Install Poetry** (if not already installed):
   ```bash
   pip install poetry
   ```
2. **Install dependencies**:
   ```bash
   poetry install
   ```
3. **Run the application**:
   ```bash
   poetry run python launch_eufm.py
   ```

## Usage Examples
- **Generate a proposal draft**
  ```bash
  poetry run python generate_proposal.py
  ```
- **Run the research agent**
  ```bash
  poetry run python app/agents/research_agent.py "Find partners in Italy"
  ```
- **Execute the monitoring system in dry-run mode**
  ```bash
  poetry run python app/agents/monitor/monitor.py --dry-run
  ```
