# EUFM — Xylella Monitoring Agent ("Monitor A")
Version: 0.1 (initial scaffolding)

## Purpose & Outcomes
Monitor A tracks the Xylella project end-to-end by knowing the full work breakdown in advance, projecting timelines, and checking daily that reality matches the plan. It opens/updates issues, nudges owners, assembles deliverable evidence, and surfaces risks early.

## Operating Rhythm
- Daily: Action runs; GAR summary posted; alerts for <14-day deadlines.
- Weekly: PM reviews monitor report; updates owners.yaml; resolves blockers.
- Per Milestone: Gate checks; evidence binder updated.

## Rule semantics

### Compliance rules
- **deadline** – items past their due date reduce the compliance score.
- **evidence** – missing acceptance evidence reduces the compliance score.
The overall compliance score is the percentage of rule weights satisfied across all WBS items (0–100).

### Risk rules
- **due_soon** (medium) – item due within 7 days.
- **overdue_high** (high) – item overdue by more than 30 days.
