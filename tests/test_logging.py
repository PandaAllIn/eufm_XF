import json
import logging

from config.logging import setup_logging, get_logger, log_event


def _parse_log(output: str) -> dict:
    return json.loads(output.strip().splitlines()[-1])


def test_log_event_includes_fields(capsys):
    setup_logging()
    logger = get_logger("test")
    log_event(
        logger,
        logging.INFO,
        "AGENT_START",
        "starting",
        run_id="run123",
        task_id="task456",
    )
    log = _parse_log(capsys.readouterr().out)
    assert log["event_category"] == "AGENT_START"
    assert log["run_id"] == "run123"
    assert log["task_id"] == "task456"
    assert log["error_code"] is None


def test_log_event_error_code(capsys):
    setup_logging()
    logger = get_logger("test")
    log_event(
        logger,
        logging.ERROR,
        "AGENT_ERROR",
        "boom",
        run_id="run123",
        task_id="task456",
        error_code="E123",
    )
    log = _parse_log(capsys.readouterr().out)
    assert log["event_category"] == "AGENT_ERROR"
    assert log["error_code"] == "E123"
