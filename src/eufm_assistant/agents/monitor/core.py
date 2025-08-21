import pathlib
from datetime import datetime, timezone
import yaml

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
