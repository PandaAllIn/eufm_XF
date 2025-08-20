# EUFM — Xylella (bootstrap)
This repository is scaffolded for the Monitor A agent and project WBS.
See `AGENTS.md` and `MONITOR.md` to get started.

## Next Steps
- Review the [diagnosis](DIAGNOSIS.md).
- Follow the [remediation plan](FIX_PLAN.md).
- Configure the remote using [push instructions](PUSH_INSTRUCTIONS.md).

## Backlog seeder

Use the backlog seeder to create or update GitHub issues from the WBS.

- **Dry-run** (default): prints the actions it would take without touching GitHub.
- **Apply**: pass `--apply` or trigger the workflow with `apply: true` to create/update issues for real.

Required environment variables:

- `GITHUB_TOKEN` – token with permission to create issues
- `GITHUB_REPOSITORY` – repository in `owner/name` format

See [`.github/workflows/seed_backlog.yml`](.github/workflows/seed_backlog.yml) for the automation workflow.
