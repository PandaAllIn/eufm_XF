# EUFM Assistant
![CI](https://github.com/PandaAllIn/eufm/actions/workflows/ci.yml/badge.svg)

## Project Overview
The EUFM Assistant is a multi-agent system designed to streamline preparation of Horizon Europe proposals.
It automates project documentation, partner research, and monitoring so teams can focus on strategy rather than administration.

## Features
- **Proposal generation** for draft submissions and documentation.
- **Multi-agent collaboration** coordinating research, drafting, and monitoring tasks.
- **Research agent** for partner and data discovery.
- **Monitoring tools** to track deadlines and project health.
- **Extensible architecture** built with Python and Flask.

## System Architecture
See [docs/system_architecture.md](docs/system_architecture.md) for a comprehensive overview of the current architecture and developer guidelines.

## Getting Started
1. **Install Poetry** (if not already installed):
   ```bash
   pip install poetry
   ```
2. **Install dependencies**:
   ```bash
   poetry install
   ```
3. **Run the unified CLI**:
   ```bash
   poetry run eufm --help
   ```

## Usage Examples
- **Route a task to an agent**
  ```bash
  poetry run eufm route "Find partners in Italy"
  ```
- **Run the research agent**
  ```bash
  poetry run eufm research "Find partners in Italy"
  ```
- **Generate proposal content**
  ```bash
  poetry run eufm propose
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

## Perplexity Sonar Integration
The research agent uses the [Perplexity API](https://docs.perplexity.ai/docs/getting-started) for plan generation. 
Set your API key in the environment:
```bash
export PERPLEXITY_API_KEY="your-key"
```

When querying, you can select from models such as `sonar`, `sonar-reasoning` (default), or `sonar-deep-research`. The
`PerplexityService` in `app/utils/services/perplexity_service.py` wraps these calls.