import json
from typing import Dict, Any, List
from app.agents.base_agent import BaseAgent, AgentStatus
from app.utils.ai_services import AIServices

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
        # For this refactoring, we will use the Perplexity Sonar for this task
        response_str = self.ai_services.query_perplexity_sonar(prompt, model="sonar-reasoning")
        try:
            plan = json.loads(response_str)
            return plan.get("steps", [])
        except json.JSONDecodeError:
            self.logger.error("Failed to decode JSON from research plan response.")
            return []

    def execute_research_plan(self, plan: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Executes the research plan. (Currently mocked)"""
        self.logger.info(f"Executing research plan: {plan}")
        # This part would involve calling the actual tools (e.g., google_search)
        # For now, we return mock data.
        mock_data = [
            {
                "organisation_name": "INSTITUTO VALENCIANO DE INVESTIGACIONES AGRARIAS",
                "country": "Spain",
                "project_acronym": "XF-ACTORS",
            },
            {
                "organisation_name": "CONSEJO SUPERIOR DE INVESTIGACIONES CIENTIFICAS",
                "country": "Spain",
                "project_acronym": "BIOVEXO",
            },
        ]
        return mock_data

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
