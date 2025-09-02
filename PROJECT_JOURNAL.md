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
- `2025-09-01 00:12:08`: Integrated the new journal system into the CoordinatorAgent.
- `2025-09-01 00:12:08`: Implemented the failed 'Milestone Archive' task.
- `2025-09-01 00:12:08`: Merged all successful branches from the overnight initiative into the main branch.
- `YYYY-MM-DD HH:MM:SS`: Initializing the project journal.
- `2025-09-02 00:00:00`: Added Stage 2 research pipeline powered by Perplexity Sonar Deep Research.

## Stage 2 Research Pipeline
Use the Stage2ResearchAgent to create multi-step research plans with citations.

```bash
python -m app.pipelines.stage2_research_pipeline "<your topic>" --output stage2
```

The generated `research_plan.json` file will be stored in the specified output directory.

## Router POC integrated
- Added automatic agent routing via SmartTaskRouter.
- Introduced CLI usage with `python -m scripts.route "prompt"` to inspect routing decisions.

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