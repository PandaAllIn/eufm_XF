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

## Configuration

Agents interact with external providers via the unified `ai_services` module.
API keys are read from environment variables using Pydantic settings. Set the
following variables before running agents:

- `OPENAI_API_KEY`
- `GOOGLE_API_KEY`
- `PERPLEXITY_API_KEY`

The `ai_services` helpers are asynchronous; synchronous agents call them using
`asyncio.run`.
