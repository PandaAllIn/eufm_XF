# Deliverables, Issues, and Risks

This guide explains how to use the templates in [`templates/`](../../templates) to track project deliverables, tasks, and risks.

## Deliverables
Copy [`DELIVERABLE_TEMPLATE.md`](../../templates/DELIVERABLE_TEMPLATE.md) to `docs/deliverables/<WBS-ID>.md` and fill in the fields.

Example:

```
# Deliverable
- **WBS ID**: [WP1-D1.1](../../wbs/wbs.yaml#L4)
- **Title**: Project handbook & quality plan
- **Owner**: pm
- **Due**: 2025-10-15
- **Acceptance Criteria**: handbook in /docs; quality gates defined and enforced by CI
- **Evidence Links**: [Issue #12](https://github.com/example/eufm/issues/12)
```

## Issues
When creating a GitHub issue, use [`ISSUE_TEMPLATE.md`](../../templates/ISSUE_TEMPLATE.md). Include links back to the related WBS item and deliverable document.

Example:

```
### Task
- **WBS ID**: [WP1-D1.1](../../wbs/wbs.yaml#L4)
- **Owner**: pm
- **Due**: 2025-10-15
- **Acceptance Criteria**: Handbook drafted

### Links
- Deliverable/PRs/Docs: [Deliverable Doc](./WP1-D1.1.md)
- GitHub Issue: [#34](https://github.com/example/eufm/issues/34)

### Risk & Mitigation (optional)
```

## Risks
To record a risk, copy [`RISK_TEMPLATE.md`](../../templates/RISK_TEMPLATE.md) and complete the fields.

Example:

```
### Risk
- **ID**: R-1
- **Description**: Documentation may fall behind schedule.
- **Impact**: Med
- **Likelihood**: Low
- **Owner**: pm
- **Mitigation**: Weekly review
- **Trigger**: No update for two weeks
```
