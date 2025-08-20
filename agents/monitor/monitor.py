import argparse
import os
import pathlib
import sys
from datetime import datetime, timezone

import yaml
from github import Github  # third-party

ROOT = pathlib.Path(__file__).resolve().parents[2]


def load_yaml(p):
    with open(p, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def gar_for_due(due_str):
    try:
        due = datetime.strptime(str(due_str), "%Y-%m-%d").date()
    except Exception:
        return "grey"
    today = datetime.now(timezone.utc).date()
    if due < today:
        return "red"
    if (due - today).days <= 14:
        return "amber"
    return "green"


def calculate_compliance_score(wbs_data, rules_data):
    rules = rules_data.get("rules", [])
    if not rules:
        return 100

    wbs_items_must_have_owner_rule = next(
        (
            rule
            for rule in rules
            if rule["id"] == "wbs_items_must_have_owner" and rule["enabled"]
        ),
        None,
    )

    if not wbs_items_must_have_owner_rule:
        return 100

    total_items = 0
    items_with_owner = 0

    for wp, items in (wbs_data.get("wbs") or {}).items():
        for item in items:
            total_items += 1
            if item.get("owner"):
                items_with_owner += 1

    if total_items == 0:
        return 100

    return (items_with_owner / total_items) * 100


def render_summary():
    w = load_yaml(ROOT / "wbs" / "wbs.yaml") or {}
    rules = (
        load_yaml(ROOT / "agents" / "monitor" / "rules" / "compliance_rules.yaml") or {}
    )
    compliance_score = calculate_compliance_score(w, rules)

    lines = ["# Monitor A — GAR Summary", ""]
    lines.append(f"**Compliance Score**: {compliance_score:.2f}%")
    lines.append("")

    for wp, items in (w.get("wbs") or {}).items():
        lines.append(f"## {wp}")
        for it in items:
            due = it.get("due", "?")
            gar = gar_for_due(due)
            lines.append(
                f"- **{it.get('id', '?')}** {it.get('title', '')} — due {due} — GAR: **{gar.upper()}**"
            )
        lines.append("")
    return "\n".join(lines)


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
        "--post-comments", action="store_true", help="Post GAR to the latest open PR"
    )
    args = parser.parse_args(argv)

    summary = render_summary()
    print(summary)

    if args.post_comments:
        post_comment_to_latest_pr(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
