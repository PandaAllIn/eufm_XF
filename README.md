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

## Telemetry

JSONL telemetry logging is disabled by default. To enable it, set
the `TELEMETRY_ENABLED` environment variable to `true` when running the
application:

```bash
TELEMETRY_ENABLED=true poetry run python launch_eufm.py
```

When enabled, routing decisions and agent lifecycle events are written to
daily rotated JSONL files in the `.logs/` directory at the project root.
Each entry includes identifiers (run/task/agent) and a SHA-256 hash of
any prompts instead of raw text to help protect sensitive data.
