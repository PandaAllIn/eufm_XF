import json

from app.agents.stage2_research_agent import Stage2ResearchAgent, save_research_tasks
from app.pipelines.stage2_research_pipeline import run_stage2_research_pipeline


class DummyAIServices:
    def __init__(self, response: str):
        self.response = response

    def query(self, model: str, prompt: str) -> str:
        assert model == "sonar-deep-research"
        return self.response


def test_agent_parses_and_returns_tasks(tmp_path):
    response = json.dumps(
        {
            "tasks": [
                {
                    "task": "Investigate X",
                    "citations": [{"text": "Source", "url": "https://example.com"}],
                }
            ]
        }
    )
    ai_services = DummyAIServices(response)
    agent = Stage2ResearchAgent("s2", {}, ai_services)
    tasks = agent.run({"query": "X"})
    assert tasks[0]["task"] == "Investigate X"
    path = save_research_tasks(tasks, tmp_path)
    assert path.exists()
    saved = json.loads(path.read_text())
    assert saved["tasks"][0]["citations"][0]["url"] == "https://example.com"


def test_pipeline_stores_plan(tmp_path):
    response = json.dumps({"tasks": [{"task": "A", "citations": []}]})
    ai_services = DummyAIServices(response)
    tasks = run_stage2_research_pipeline("query", tmp_path, ai_services)
    assert tasks[0]["task"] == "A"
    assert (tmp_path / "research_plan.json").exists()


def test_invalid_response_handled_gracefully():
    ai_services = DummyAIServices("not json")
    agent = Stage2ResearchAgent("s2", {}, ai_services)
    tasks = agent.run({"query": "topic"})
    assert tasks == []
