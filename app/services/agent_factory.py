from typing import Dict, Any, Type, List
import logging
from app.agents.base_agent import BaseAgent
from app.agents.research_agent import ResearchAgent
from app.agents.document_agent import DocumentAgent
from app.agents.proposal_agent import ProposalAgent
from app.agents.coordinator_agent import CoordinatorAgent
from app.utils.ai_services import AIServices
from app.services.task_router import route_task, log_routing_decision

class AgentFactory:
    """Factory for creating and configuring AI agents."""

    def __init__(self, ai_services: AIServices, base_config: Dict[str, Any]):
        self.ai_services = ai_services
        self.base_config = base_config
        self._agent_registry: Dict[str, Type[BaseAgent]] = {
            "research": ResearchAgent,
            "document": DocumentAgent,
            "proposal": ProposalAgent,
            "coordinator": CoordinatorAgent,
        }

    def create_agent(self, agent_type: str, agent_id: str, agent_config: Dict[str, Any] = None) -> BaseAgent:
        """Create an agent instance of the specified type."""

        if agent_type == "auto":
            if not agent_config or "prompt" not in agent_config:
                raise ValueError("Auto agent requires 'prompt' in agent_config")
            prompt = agent_config.pop("prompt")
            agent_type, reason = route_task(prompt)
            log_routing_decision(prompt, agent_type, reason)

        agent_class = self._agent_registry.get(agent_type)
        if not agent_class:
            logger.error(
                f"{ConfigurationError.__name__}: Unknown agent type '{agent_type}'"
            )
            raise ConfigurationError(f"Unknown agent type: {agent_type}")

        # Combine base config with agent-specific config
        final_config = self.base_config.copy()
        if agent_config:
            final_config.update(agent_config)

        # Instantiate and return the agent
        # This part will need to be updated as we refactor the agents themselves
        if agent_type in ["research", "proposal"]:
            return agent_class(agent_id=agent_id, config=final_config, ai_services=self.ai_services)
        else:
            return agent_class(agent_id=agent_id, config=final_config)

    def list_available_agents(self) -> List[str]:
        """Get a list of available agent types."""
        return list(self._agent_registry.keys())
