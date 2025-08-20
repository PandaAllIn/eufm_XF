import argparse
import os
import pathlib
import sys
from datetime import date, datetime

import yaml
from github import Github  # third-party

ROOT = pathlib.Path(__file__).resolve().parents[2]


def load_yaml(p):
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def gar_for_due(due_val):
    try:
        if isinstance(due_val, date):
            due = due_val
        else:
            due = datetime.strptime(str(due_val), "%Y-%m-%d").date()
    except Exception:
        return "grey"
    today = datetime.utcnow().date()
    if due < today:
        return "red"
    if (due - today).days <= 14:
        return "amber"
    return "green"


def evaluate_risk(item, rules, today=None):
    today = today or datetime.utcnow().date()
    try:
        val = item.get("due", "")
        if isinstance(val, date):
            due = val
        else:
            due = datetime.strptime(str(val), "%Y-%m-%d").date()
    except Exception:
        return None
    delta = (due - today).days
    for rule in (rules or {}).values():
        if "days_overdue" in rule and delta < -int(rule.get("days_overdue", 0)):
            return rule.get("severity")
        if "days_until_due" in rule and 0 <= delta <= int(
            rule.get("days_until_due", 0)
        ):
            return rule.get("severity")
    return None


def evaluate_compliance(items, rules, today=None):
    today = today or datetime.utcnow().date()
    total = 0.0
    passed = 0.0
    for it in items:
        try:
            val = it.get("due", "")
            if isinstance(val, date):
                due = val
            else:
                due = datetime.strptime(str(val), "%Y-%m-%d").date()
        except Exception:
            due = None
        r = (rules or {}).get("deadline", {})
        w = float(r.get("weight", 1))
        total += w
        if due and due >= today:
            passed += w
        r = (rules or {}).get("evidence", {})
        w = float(r.get("weight", 1))
        total += w
        if it.get("acceptance"):
            passed += w
    if total == 0:
        return 100
    return int(round(100 * passed / total))


def render_summary():
    w = load_yaml(ROOT / "wbs" / "wbs.yaml") or {}
    compliance_rules = (
        load_yaml(ROOT / "agents" / "monitor" / "rules" / "compliance_rules.yaml") or {}
    )
    risk_rules = (
        load_yaml(ROOT / "agents" / "monitor" / "rules" / "risk_rules.yaml") or {}
    )
    lines = ["# Monitor A — GAR Summary", ""]
    all_items = []
    for wp, items in (w.get("wbs") or {}).items():
        lines.append(f"## {wp}")
        for it in items:
            all_items.append(it)
            due = it.get("due", "?")
            gar = gar_for_due(due)
            risk = evaluate_risk(it, risk_rules)
            risk_str = f" — RISK: {risk.upper()}" if risk else ""
            lines.append(
                f"- **{it.get('id', '?')}** {it.get('title', '')} — due {due} — GAR: **{gar.upper()}**{risk_str}"
            )
        lines.append("")
    score = evaluate_compliance(all_items, compliance_rules)
    lines.append(f"Compliance score: {score}")
    return "\n".join(lines), score


def post_comment_to_latest_pr(body: str) -> int:
    token = os.getenv("GITHUB_TOKEN")
    repo_full = os.getenv("GITHUB_REPOSITORY")
    if not token or not repo_full:
        print("[post] missing GITHUB_TOKEN or GITHUB_REPOSITORY", file=sys.stderr)
        return 1
    gh = Github(token)
    repo = gh.get_repo(repo_full)
    pulls = repo.get_pulls(state="open", sort="created", direction="desc")
    try:
        pr = next(iter(pulls))
    except StopIteration:
        print("[post] no open PRs to comment on", file=sys.stderr)
        return 0
    pr.create_issue_comment(body)
    print(f"[post] commented on PR #{pr.number}", file=sys.stderr)
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run", action="store_true", help="Print summary to stdout"
    )
    parser.add_argument(
        "--emit-status", action="store_true", help="Alias of --dry-run for CI"
    )
    parser.add_argument(
        "--post-comments",
        action="store_true",
        help="Post GAR to the latest open PR",
    )
    args = parser.parse_args(argv)

    summary, _score = render_summary()
    print(summary)

    if args.post_comments:
        post_comment_to_latest_pr(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
