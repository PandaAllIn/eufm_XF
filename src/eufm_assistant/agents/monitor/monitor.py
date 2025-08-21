import argparse
import os
import pathlib
import sys

from github import Github

from eufm_assistant.agents.monitor.core import (
    calculate_compliance_score,
    gar_for_due,
    load_yaml,
)

# The project root is now 4 levels up from this file's directory
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[4]


def render_summary():
    wbs_file = PROJECT_ROOT / "wbs" / "wbs.yaml"
    rules_file = PROJECT_ROOT / "src" / "eufm_assistant" / "agents" / "monitor" / "rules" / "compliance_rules.yaml"

    w = load_yaml(wbs_file) or {}
    rules = load_yaml(rules_file) or {}

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
    # To run this script directly, you must be in the project root and run
    # `python -m src.eufm_assistant.agents.monitor.monitor`
    main()
