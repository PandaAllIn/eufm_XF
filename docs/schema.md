# Planning Schema

## Work Breakdown Structure (`wbs/wbs.yaml`)

```yaml
wbs:
  WP1:
    - id: WP1-T1.1
      title: Example task
      type: task|deliverable
      due: YYYY-MM-DD
      owner: owner-id
      depends: [WP1-T0]        # optional
      acceptance: [criteria]   # optional
```

- The root key `wbs` maps work package codes (e.g. `WP1`) to a list of items.
- Each item must define:
  - `id` – unique identifier.
  - `title` – short description.
  - `type` – `task` or `deliverable`.
  - `due` – ISO date (YYYY-MM-DD).
  - `owner` – owner code from `owners.yaml`.
  - `depends` – optional list of task ids.
  - `acceptance` – optional list of acceptance criteria.

## Milestones (`wbs/milestones.yaml`)

```yaml
milestones:
  - id: STAGE1
    title: Milestone name
    date: YYYY-MM-DD
    gate_rules:
      - condition 1
      - condition 2
```

- The root key `milestones` holds a list of milestone entries.
- Each milestone requires `id`, `title`, `date`, and a `gate_rules` list.
