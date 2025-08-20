from datetime import datetime, timedelta

import pytest
import yaml

from agents.monitor import monitor


@pytest.fixture
def temp_wbs(tmp_path, monkeypatch):
    """Create a temporary WBS structure and patch ROOT."""
    data = {
        "wbs": {
            "WPX": [
                {
                    "id": "WPX-T1",
                    "title": "Task X1",
                    "due": "2099-01-01",
                }
            ],
            "WPY": [
                {
                    "id": "WPY-D1",
                    "title": "Deliverable Y1",
                    "due": "2099-01-03",
                }
            ],
        }
    }
    wbs_dir = tmp_path / "wbs"
    wbs_dir.mkdir()
    (wbs_dir / "wbs.yaml").write_text(yaml.safe_dump(data))
    monkeypatch.setattr(monitor, "ROOT", tmp_path)
    return data


def test_gar_for_due_classification():
    today = datetime.utcnow().date()
    past = (today - timedelta(days=1)).strftime("%Y-%m-%d")
    soon = (today + timedelta(days=7)).strftime("%Y-%m-%d")
    future = (today + timedelta(days=30)).strftime("%Y-%m-%d")

    assert monitor.gar_for_due(past) == "red"
    assert monitor.gar_for_due(soon) == "amber"
    assert monitor.gar_for_due(future) == "green"


def test_render_summary(temp_wbs):
    summary = monitor.render_summary()
    assert "# Monitor A — GAR Summary" in summary
    assert "## WPX" in summary
    assert "- **WPX-T1** Task X1 — due 2099-01-01 — GAR: **GREEN**" in summary
    assert "## WPY" in summary
    assert "- **WPY-D1** Deliverable Y1 — due 2099-01-03 — GAR: **GREEN**" in summary


def test_post_comment_missing_env(monkeypatch, capsys):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GITHUB_REPOSITORY", raising=False)

    ret = monitor.post_comment_to_latest_pr("body")
    captured = capsys.readouterr()

    assert ret == 1
    assert "missing GITHUB_TOKEN or GITHUB_REPOSITORY" in captured.err
