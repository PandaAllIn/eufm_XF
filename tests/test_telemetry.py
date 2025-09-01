import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.utils.telemetry import TelemetryLogger


def read_jsonl(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def test_logger_writes_entries(tmp_path, monkeypatch):
    monkeypatch.setenv("TELEMETRY_ENABLED", "true")
    logger = TelemetryLogger(log_dir=tmp_path)
    logger.log(run_id="r1", event_type="test", agent_id="a1")
    log_file = next(tmp_path.iterdir())
    data = read_jsonl(log_file)
    assert data[0]["run_id"] == "r1"
    assert data[0]["event_type"] == "test"


def test_rotation_by_date(tmp_path, monkeypatch):
    monkeypatch.setenv("TELEMETRY_ENABLED", "true")
    logger = TelemetryLogger(log_dir=tmp_path)

    first = tmp_path / "2024-01-01.jsonl"
    second = tmp_path / "2024-01-02.jsonl"
    monkeypatch.setattr(logger, "_current_log_path", lambda: first)
    logger.log(run_id="r1", event_type="one")
    monkeypatch.setattr(logger, "_current_log_path", lambda: second)
    logger.log(run_id="r2", event_type="two")

    assert first.exists()
    assert second.exists()


def test_disabled_logger(tmp_path, monkeypatch):
    monkeypatch.delenv("TELEMETRY_ENABLED", raising=False)
    logger = TelemetryLogger(log_dir=tmp_path)
    logger.log(run_id="r1", event_type="test")
    assert not any(tmp_path.iterdir())
