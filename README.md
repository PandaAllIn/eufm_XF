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
└── launch_eufm.py     # Legacy entry point (delegates to CLI)
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
3. **Explore the unified CLI**:
   ```bash
   poetry run eufm --help
   ```

## Usage Examples
- **Route a task to the best agent**
  ```bash
  poetry run eufm route "Research funding opportunities"
  ```
- **Run a specific agent**
  ```bash
  poetry run eufm run-agent research --param query="Find partners in Italy"
  ```
- **Use specialized shortcuts**
  ```bash
  poetry run eufm research "Find partners in Italy"
  poetry run eufm propose
  ```
