from datetime import date, timedelta

from agents.monitor import monitor


def test_compliance_and_risk():
    today = date(2024, 1, 1)
    items = [
        {
            "id": "good",
            "due": (today + timedelta(days=30)).strftime("%Y-%m-%d"),
            "acceptance": ["doc"],
        },
        {
            "id": "overdue",
            "due": (today - timedelta(days=40)).strftime("%Y-%m-%d"),
            "acceptance": [],
        },
        {
            "id": "soon",
            "due": (today + timedelta(days=3)).strftime("%Y-%m-%d"),
            "acceptance": ["x"],
        },
    ]
    compliance_rules = monitor.load_yaml(
        monitor.ROOT / "agents" / "monitor" / "rules" / "compliance_rules.yaml"
    )
    risk_rules = monitor.load_yaml(
        monitor.ROOT / "agents" / "monitor" / "rules" / "risk_rules.yaml"
    )

    score = monitor.evaluate_compliance(items, compliance_rules, today)
    assert score == 67

    assert monitor.evaluate_risk(items[0], risk_rules, today) is None
    assert monitor.evaluate_risk(items[1], risk_rules, today) == "high"
    assert monitor.evaluate_risk(items[2], risk_rules, today) == "medium"
