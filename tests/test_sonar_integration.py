import json
from unittest.mock import MagicMock, patch

from app.agents.research_agent import ResearchAgent
from app.utils.ai_services import AIServices
from app.utils.services.perplexity_service import PerplexityService


class DummySettings(dict):
    pass


def _make_agent() -> ResearchAgent:
    services = AIServices({"perplexity_api_key": "test"})
    return ResearchAgent("r1", {}, services)


def test_perplexity_service_handles_success_and_error():
    service = PerplexityService(api_key="key")
    fake_client = MagicMock()
    fake_resp = MagicMock()
    fake_resp.choices = [MagicMock(message=MagicMock(content="ok"))]
    fake_client.chat.completions.create.return_value = fake_resp
    service.client = fake_client
    result = service.query("prompt")
    assert result == {"content": "ok", "error": None}

    fake_client.chat.completions.create.side_effect = Exception("boom")
    error_result = service.query("prompt")
    assert error_result["content"] is None
    assert "boom" in error_result["error"]


def test_generate_research_plan_valid_and_invalid_json():
    agent = _make_agent()
    valid_response = {
        "content": json.dumps({"steps": [{"tool": "google_search", "query": "x"}]}),
        "error": None,
    }
    invalid_json = {"content": "not json", "error": None}
    missing_steps = {"content": json.dumps({"foo": "bar"}), "error": None}
    error_response = {"content": None, "error": "fail"}

    with patch.object(PerplexityService, "query", return_value=valid_response):
        plan = agent.generate_research_plan("topic")
        assert plan == [{"tool": "google_search", "query": "x"}]

    with patch.object(PerplexityService, "query", return_value=invalid_json):
        plan = agent.generate_research_plan("topic")
        assert plan == []

    with patch.object(PerplexityService, "query", return_value=missing_steps):
        plan = agent.generate_research_plan("topic")
        assert plan == []

    with patch.object(PerplexityService, "query", return_value=error_response):
        plan = agent.generate_research_plan("topic")
        assert plan == []


def test_execute_research_plan_calls_helpers():
    agent = _make_agent()
    plan = [
        {"tool": "google_search", "query": "q"},
        {"tool": "view_text_website", "query": "http://example.com"},
    ]
    with (
        patch(
            "app.agents.research_agent.perform_google_search", return_value={"a": 1}
        ) as mock_search,
        patch(
            "app.agents.research_agent.fetch_page_text", return_value={"b": 2}
        ) as mock_fetch,
    ):
        results = agent.execute_research_plan(plan)
        mock_search.assert_called_once_with("q")
        mock_fetch.assert_called_once_with("http://example.com")
        assert results == [{"a": 1}, {"b": 2}]
