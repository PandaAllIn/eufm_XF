import argparse
import os
import sys
from typing import Dict, List, Optional

import yaml
from github import Github


ISSUE_TITLE_FMT = "[{wp}] {id} — {title}"
LABEL_COLOR = "0366d6"  # WP labels


def load_yaml(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def ensure_label(repo, name: str, color: str = LABEL_COLOR):
    try:
        return repo.get_label(name)
    except Exception:
        return repo.create_label(
            name=name, color=color, description=f"Work Package {name}"
        )


def owner_to_username(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    # Accept '@user' or 'user'
    return raw.lstrip("@").strip() or None


def find_issue_by_wbs_id(gh: Github, repo_full: str, wbs_id: str):
    # Search across open+closed issues by exact WBS token in title
    query = f'repo:{repo_full} is:issue in:title "{wbs_id}"'
    for item in gh.search_issues_and_pull_requests(query):
        return item  # first match
    return None


def build_body(item: Dict) -> str:
    due = item.get("due")
    due_str = str(due) if due else "—"
    owner = item.get("owner", "—")
    acceptance = item.get("acceptance") or []
    acc_lines = "\n".join(f"- {a}" for a in acceptance) or "- (not specified)"
    return (
        f"**WBS ID:** {item['id']}\n"
        f"**Due:** {due_str}\n"
        f"**Owner (role):** {owner}\n\n"
        f"### Acceptance Criteria\n{acc_lines}\n"
    )


def create_or_update_issue(
    gh: Github,
    repo,
    repo_full: str,
    wp: str,
    item: Dict,
    assignee_username: Optional[str],
    dry_run: bool,
) -> Dict:
    title = ISSUE_TITLE_FMT.format(wp=wp, id=item["id"], title=item["title"])
    body = build_body(item)

    existing = find_issue_by_wbs_id(gh, repo_full, item["id"])
    if existing:
        number = existing.number
        if dry_run:
            return {"action": "update(dry)", "number": number, "title": title}
        issue = repo.get_issue(number=number)
        issue.edit(title=title, body=body)
        if assignee_username:
            try:
                issue.add_to_assignees(assignee_username)
            except Exception:
                pass
        ensure_label(repo, wp)
        try:
            issue.add_to_labels(wp)
        except Exception:
            pass
        return {"action": "update", "number": number, "title": title}

    if dry_run:
        return {"action": "create(dry)", "title": title}

    issue = repo.create_issue(
        title=title, body=body, assignee=assignee_username or None
    )
    ensure_label(repo, wp)
    try:
        issue.add_to_labels(wp)
    except Exception:
        pass
    return {"action": "create", "number": issue.number, "title": title}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Seed/update GitHub issues from WBS")
    ap.add_argument(
        "--apply",
        action="store_true",
        help="Actually create/update issues (default: dry-run)",
    )
    args = ap.parse_args(argv)

    token = os.getenv("GITHUB_TOKEN")
    repo_full = os.getenv("GITHUB_REPOSITORY")
    if not token or not repo_full:
        print("Missing GITHUB_TOKEN or GITHUB_REPOSITORY", file=sys.stderr)
        sys.exit(2)

    gh = Github(token)
    repo = gh.get_repo(repo_full)

    root = os.path.dirname(os.path.abspath(__file__))  # scripts/
    root = os.path.dirname(root)  # project root

    wbs = load_yaml(os.path.join(root, "wbs", "wbs.yaml"))
    owners = load_yaml(os.path.join(root, "wbs", "owners.yaml"))

    results: List[Dict] = []
    for wp, items in (wbs.get("wbs") or {}).items():
        for it in items:
            role = it.get("owner")
            assignee = owner_to_username(owners.get(role)) if role else None
            results.append(
                create_or_update_issue(
                    gh=gh,
                    repo=repo,
                    repo_full=repo_full,
                    wp=wp,
                    item=it,
                    assignee_username=assignee,
                    dry_run=(not args.apply),
                )
            )

    print("Backlog seeding summary:")
    for r in results:
        number = f"#{r['number']}" if "number" in r else ""
        print(f"- {r['action']} {number} {r['title']}")


if __name__ == "__main__":
    main()
