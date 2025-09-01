import json
from typing import Dict, Any, List

from app.agents.base_agent import BaseAgent, AgentStatus
from app.utils.ai_services import AIServices


def perform_google_search(query: str) -> Dict[str, Any]:
    """Perform a Google Custom Search request.

    TODO: Implement actual Google Custom Search API integration.
    """
    return {"search": query, "results": []}


def fetch_page_text(url: str) -> Dict[str, Any]:
    """Fetch the text content of a web page.

    TODO: Implement real page fetching and parsing.
    """
    return {"url": url, "content": ""}


class ResearchAgent(BaseAgent):
    """An agent that conducts research by generating and executing a plan."""

    def __init__(self, agent_id: str, config: Dict[str, Any], ai_services: AIServices):
        super().__init__(agent_id, config)
        self.ai_services = ai_services

    def generate_research_plan(self, query: str) -> List[Dict[str, str]]:
        """Generates a research plan using an AI model."""
        prompt = f"""
        Given the user query '{query}', generate a step-by-step research plan.
        The plan should be a JSON array of steps. Each step should be a dictionary with a 'tool' and 'query' field.
        The available tools are: 'google_search', 'view_text_website'.
        The primary knowledge base to use is CORDIS.
        Example:
        [
            {{"tool": "google_search", "query": "site:cordis.europa.eu xylella fastidiosa research projects spain"}}
        ]
        """
        response = self.ai_services.perplexity_service.query(
            prompt, model="sonar-reasoning"
        )
        if response["error"]:
            self.logger.error(f"Perplexity error: {response['error']}")
            return []
        try:
            plan = json.loads(response["content"])
        except json.JSONDecodeError:
            self.logger.error("Failed to decode JSON from research plan response.")
            return []
        steps = plan.get("steps")
        if not isinstance(steps, list):
            self.logger.error("Research plan response missing 'steps' field.")
            return []
        return steps

    def execute_research_plan(self, plan: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Executes the research plan."""
        self.logger.info(f"Executing research plan: {plan}")
        results = []
        for step in plan:
            tool = step.get("tool")
            query = step.get("query")
            if tool == "google_search":
                results.append(perform_google_search(query))
            elif tool == "view_text_website":
                results.append(fetch_page_text(query))
            else:
                self.logger.warning(f"Unknown tool in plan: {tool}")
        return results

    def run(self, parameters: Dict[str, Any]) -> Any:
        """Runs the research agent. Expects 'query' in parameters."""
        self.status = AgentStatus.RUNNING
        query = parameters.get("query")
        if not query:
            self.error = "Missing 'query' parameter."
            self.status = AgentStatus.FAILED
            self.logger.error(self.error)
            raise ValueError(self.error)

        self.logger.info(f"Starting research for query: {query}")
        try:
            plan = self.generate_research_plan(query)
            results = self.execute_research_plan(plan)

            self.result = results
            self.status = AgentStatus.COMPLETED
            self.logger.info(f"Research completed for query: {query}")
            return results
        except Exception as e:
            self.error = str(e)
            self.status = AgentStatus.FAILED
            self.logger.error(f"Research failed for query '{query}': {e}")
            raise
