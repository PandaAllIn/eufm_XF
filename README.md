# EUFM — Xylella (bootstrap)
This repository is scaffolded for the Monitor A agent and project WBS.
See `AGENTS.md` and `MONITOR.md` to get started.

## Next Steps
- Review the [diagnosis](DIAGNOSIS.md).
- Follow the [remediation plan](FIX_PLAN.md).
- Configure the remote using [push instructions](PUSH_INSTRUCTIONS.md).

## Dashboard

The monitoring dashboard summarizes each work package in a table showing
GAR flags, upcoming 14-day deadlines, and any current blockers. Run
`python agents/monitor/monitor.py --dry-run` to generate the dashboard
locally.
