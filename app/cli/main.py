import argparse
import json
from typing import Any, Dict

from config.settings import get_settings
from app.services.task_router import route_task
from app.services.agent_factory import AgentFactory
from app.utils.ai_services import get_ai_services


def _cmd_route(args: argparse.Namespace, **_: Any) -> None:
    agent = route_task(args.prompt)
    print(agent)


def _cmd_run_agent(
    args: argparse.Namespace,
    *,
    agent_factory: AgentFactory,
    **_: Any,
) -> None:
    params: Dict[str, Any] = json.loads(args.params)
    agent = agent_factory.create_agent(args.agent, args.id)
    result = agent.execute(params)
    print(result)


def _cmd_research(
    args: argparse.Namespace,
    *,
    agent_factory: AgentFactory,
    **_: Any,
) -> None:
    agent = agent_factory.create_agent("research", "research-cli")
    result = agent.execute({"query": args.query})
    print(result)


def _cmd_propose(
    args: argparse.Namespace,
    *,
    agent_factory: AgentFactory,
    **_: Any,
) -> None:
    agent = agent_factory.create_agent("proposal", "proposal-cli")
    result = agent.execute({})
    print(result)


def build_parser() -> argparse.ArgumentParser:
    epilog = (
        "Examples:\n"
        "  eufm route \"find collaborators in Italy\"\n"
        "  eufm research \"find partners in Spain\"\n"
        "  eufm run-agent research --params '{\"query\": \"xylella\"}'\n"
        "  eufm propose\n"
    )
    parser = argparse.ArgumentParser(
        description="Unified command-line interface for EUFM agents.",
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command")

    p_route = subparsers.add_parser("route", help="Suggest an agent for a given task")
    p_route.add_argument("prompt", help="Task description to route")
    p_route.set_defaults(func=_cmd_route)

    p_run = subparsers.add_parser("run-agent", help="Execute a specific agent")
    p_run.add_argument("agent", help="Agent type to run")
    p_run.add_argument("--id", default="cli", help="Identifier for the agent instance")
    p_run.add_argument(
        "--params",
        default="{}",
        help="JSON string of parameters to pass to the agent",
    )
    p_run.set_defaults(func=_cmd_run_agent)

    p_research = subparsers.add_parser("research", help="Run the research agent")
    p_research.add_argument("query", help="Research query")
    p_research.set_defaults(func=_cmd_research)

    p_propose = subparsers.add_parser("propose", help="Generate proposal content")
    p_propose.set_defaults(func=_cmd_propose)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return

    settings = get_settings()
    ai_services = get_ai_services(settings.ai.model_dump())
    agent_factory = AgentFactory(ai_services=ai_services, base_config={})

    args.func(
        args,
        settings=settings,
        ai_services=ai_services,
        agent_factory=agent_factory,
    )


if __name__ == "__main__":
    main()
