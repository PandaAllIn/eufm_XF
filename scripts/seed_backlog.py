# Stub for seeding GitHub issues from /wbs/*.yaml
# Usage: python scripts/seed_backlog.py --dry-run
import argparse
import json
import pathlib

import yaml


ROOT = pathlib.Path(__file__).resolve().parents[1]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    w = yaml.safe_load((ROOT / "wbs" / "wbs.yaml").read_text(encoding="utf-8"))
    owners = yaml.safe_load((ROOT / "wbs" / "owners.yaml").read_text(encoding="utf-8"))
    out = []
    for wp, items in (w.get("wbs") or {}).items():
        for it in items:
            due = it.get("due")
            out.append(
                {
                    "title": f"[{wp}] {it['id']} — {it['title']}",
                    "labels": [wp],
                    "assignee": owners.get(it.get("owner", ""), ""),
                    "due": str(due) if due else None,
                    "body": f"WBS ID: {it['id']}\nDue: {due}\nOwner: {it.get('owner')}",
                }
            )
    if args.dry_run:
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print("Non-dry-run mode not implemented yet.")


if __name__ == "__main__":
    main()
