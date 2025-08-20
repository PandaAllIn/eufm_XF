from datetime import datetime, timezone
from agents.monitor.monitor import gar_for_due, calculate_compliance_score


class MockDateTime(datetime):
    @classmethod
    def now(cls, tz=None):
        return datetime(2025, 8, 20, tzinfo=timezone.utc)


def test_gar_for_due(monkeypatch):
    monkeypatch.setattr("agents.monitor.monitor.datetime", MockDateTime)

    # Test green case (more than 14 days in the future)
    assert gar_for_due("2025-09-04") == "green"  # 15 days

    # Test amber case (14 days or less in the future)
    assert gar_for_due("2025-09-03") == "amber"  # 14 days
    assert gar_for_due("2025-08-20") == "amber"  # 0 days

    # Test red case (in the past)
    assert gar_for_due("2025-08-19") == "red"

    # Test grey case (invalid date)
    assert gar_for_due("not a date") == "grey"
    assert gar_for_due(None) == "grey"


def test_calculate_compliance_score():
    rules = {"rules": [{"id": "wbs_items_must_have_owner", "enabled": True}]}

    # Test case with all items having an owner
    wbs_all_owners = {
        "wbs": {
            "WP1": [{"id": "T1", "owner": "a"}, {"id": "T2", "owner": "b"}],
            "WP2": [{"id": "T3", "owner": "c"}],
        }
    }
    assert calculate_compliance_score(wbs_all_owners, rules) == 100.0

    # Test case with some items missing an owner
    wbs_missing_owners = {
        "wbs": {
            "WP1": [{"id": "T1", "owner": "a"}, {"id": "T2"}],
            "WP2": [{"id": "T3", "owner": "c"}],
        }
    }
    assert calculate_compliance_score(wbs_missing_owners, rules) == (2 / 3) * 100

    # Test case with no items
    wbs_no_items = {"wbs": {}}
    assert calculate_compliance_score(wbs_no_items, rules) == 100.0

    # Test case with no rules
    assert calculate_compliance_score(wbs_all_owners, {"rules": []}) == 100.0

    # Test case with rule disabled
    rules_disabled = {"rules": [{"id": "wbs_items_must_have_owner", "enabled": False}]}
    assert calculate_compliance_score(wbs_missing_owners, rules_disabled) == 100.0
