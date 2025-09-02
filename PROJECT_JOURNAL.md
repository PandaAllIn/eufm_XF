# Project Journal

## Last Known Status
*   Overnight AI Task Force initiative complete. All systems refactored and new capabilities integrated.
*   A new, unified CLI has been implemented.
*   A new CI workflow has been added.

## Active Strategic Goals
- Establish a shared long-term memory for the AI Task Force.
- Create a clear, auditable project history.
- Ensure all new code meets quality standards via automated checks.

## Key Decisions Log
- `2025-09-01 00:35:49`: CoordinatorAgent initialized.
- `2025-09-01 00:35:49`: CoordinatorAgent initialized.
- `2025-09-01 00:35:36`: CoordinatorAgent initialized.
- `2025-09-01 00:35:36`: CoordinatorAgent initialized.
- `2025-09-01 00:12:08`: Integrated the new journal system into the CoordinatorAgent.
- `2025-09-01 00:12:08`: Implemented the failed 'Milestone Archive' task.
- `2025-09-01 00:12:08`: Merged all successful branches from the overnight initiative into the main branch.
- `YYYY-MM-DD HH:MM:SS`: Initializing the project journal.
- `YYYY-MM-DD HH:MM:SS`: Unified CLI entrypoints and deprecated legacy launcher.

## Open Questions & Blockers
- The `poetry install` command is still failing in the CI environment. This needs to be addressed.

## Continuous Integration
- A GitHub Actions workflow (`ci.yml`) now runs `ruff check .` and `pytest -q` on each push and pull request.
- Run locally with:
  ```bash
  poetry install
  poetry run ruff check .
  poetry run pytest -q
  ```