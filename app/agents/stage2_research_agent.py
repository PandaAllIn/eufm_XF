import json
from pathlib import Path
from typing import Any, Dict, List

from app.agents.base_agent import AgentStatus, BaseAgent
from app.utils.ai_services import AIServices


class Stage2ResearchAgent(BaseAgent):
    """Generates structured research tasks with citations for the Stage 2 proposal."""

    def __init__(self, agent_id: str, config: Dict[str, Any], ai_services: AIServices):
        super().__init__(agent_id, config)
        self.ai_services = ai_services

    def _build_prompt(self, query: str) -> str:
        return (
            "Generate a multi-step research plan for the following query. "
            "Return JSON with a 'tasks' list. Each task must include a 'task' field "
            "and a 'citations' list of objects with 'text' and 'url'. Query: "
            f"{query}"
        )

    def _parse_response(self, response: str) -> List[Dict[str, Any]]:
        try:
            data = json.loads(response)
        except (json.JSONDecodeError, TypeError):
            self.logger.error("Invalid JSON from research model")
            return []
        tasks = data.get("tasks")
        if not isinstance(tasks, list):
            self.logger.error("Response missing 'tasks' list")
            return []
        return tasks

    def generate_tasks(self, query: str) -> List[Dict[str, Any]]:
        prompt = self._build_prompt(query)
        response_str = self.ai_services.query("sonar-deep-research", prompt)
        return self._parse_response(response_str)

    def run(self, parameters: Dict[str, Any]) -> Any:
        self.status = AgentStatus.RUNNING
        query = parameters.get("query")
        if not query:
            self.status = AgentStatus.FAILED
            self.error = "Missing 'query' parameter"
            raise ValueError(self.error)
        tasks = self.generate_tasks(query)
        self.result = tasks
        self.status = AgentStatus.COMPLETED
        return tasks


def save_research_tasks(tasks: List[Dict[str, Any]], output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    path = output_dir / "research_plan.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump({"tasks": tasks}, f, indent=2)
    return path
