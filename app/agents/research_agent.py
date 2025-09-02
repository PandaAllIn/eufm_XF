import asyncio
import json
import warnings
from typing import Dict, Any, List

from app.agents.base_agent import BaseAgent, AgentStatus
from app.utils.ai_services import AIServices, get_ai_services


class ResearchAgent(BaseAgent):
    """An agent that conducts research by generating and executing a plan."""

    def __init__(
        self,
        agent_id: str,
        config: Dict[str, Any],
        ai_services: AIServices | None = None,
    ):
        super().__init__(agent_id, config)
        self.ai_services = ai_services or get_ai_services()

    def lookup_call_id(self, call_id: str) -> str:
        """Lookup a call ID in the Horizon Europe Programme Guide."""
        return self.ai_services.query_programme_guide(call_id)

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
        response_str = asyncio.run(
            self.ai_services.query_perplexity_sonar(prompt, model="sonar-reasoning")
        )
        try:
            response_text = self.ai_services.query_perplexity_sonar(
                prompt, model="sonar-reasoning"
            )
        except AIServiceError as exc:
            self.logger.error(f"Perplexity error: {exc}")
            return []
        try:
            plan = json.loads(response_text)
        except json.JSONDecodeError:
            log_event(
                self.logger,
                logging.ERROR,
                "AGENT_ERROR",
                "Failed to decode JSON from research plan response.",
                error_code="PLAN_DECODE_ERROR",
            )
            return []
        steps = plan.get("steps")
        if not isinstance(steps, list):
            self.logger.error("Research plan response missing 'steps' field.")
            return []
        return steps

    def generate_research_plan_direct(
        self, query: str
    ) -> List[Dict[str, str]]:  # pragma: no cover - deprecated
        warnings.warn(
            "generate_research_plan_direct is deprecated; use generate_research_plan",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.generate_research_plan(query)

    def execute_research_plan(self, plan: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """Executes the research plan. (Currently mocked)"""
        log_event(
            self.logger,
            logging.INFO,
            "ROUTER_DECISION",
            f"Executing research plan: {plan}",
        )
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
        run_id = parameters.get("run_id")
        task_id = parameters.get("task_id")
        query = parameters.get("query")
        if not query:
            self.error = "Missing 'query' parameter."
            self.status = AgentStatus.FAILED
            log_event(
                self.logger,
                logging.ERROR,
                "AGENT_ERROR",
                self.error,
                run_id,
                task_id,
                error_code="MISSING_QUERY",
            )
            raise ValueError(self.error)

        log_event(
            self.logger,
            logging.INFO,
            "AGENT_START",
            f"Starting research for query: {query}",
            run_id,
            task_id,
        )
        try:
            plan = self.generate_research_plan(query)
            if not plan:
                raise AgentExecutionError(
                    f"Research failed for query '{query}'",
                    agent_type="research",
                    agent_id=self.agent_id,
                )
            results = self.execute_research_plan(plan)

            self.result = results
            self.status = AgentStatus.COMPLETED
            log_event(
                self.logger,
                logging.INFO,
                "AGENT_SUCCESS",
                f"Research completed for query: {query}",
                run_id,
                task_id,
            )
            return results
        except Exception as e:
            self.error = str(e)
            self.status = AgentStatus.FAILED
            log_event(
                self.logger,
                logging.ERROR,
                "AGENT_ERROR",
                f"Research failed for query '{query}': {e}",
                run_id,
                task_id,
                error_code="RESEARCH_FAIL",
            )
            raise
