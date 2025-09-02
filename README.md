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
- **Centralized structured logging** with event categories and optional error codes for improved observability.

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

## Testing
Run the integration test suite to exercise the full agent workflow:
```bash
poetry run pytest tests/integration -q
```
