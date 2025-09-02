import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.services.task_router import route_task


def test_route_task_keyword():
    agent, reason = route_task("Please research and summarize the topic")
    assert agent == "research"
    assert "Matched keywords" in reason


def test_route_task_default():
    agent, reason = route_task("No matching words here")
    assert agent == "document"
    assert "default" in reason.lower()
