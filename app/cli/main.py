import argparse
from typing import Dict

from config.settings import get_settings
from app.utils.ai_services import get_ai_services
from app.services.task_router import route_task
from app.services.agent_factory import AgentFactory


def parse_params(param_list: list[str]) -> Dict[str, str]:
    params: Dict[str, str] = {}
    for item in param_list:
        if "=" in item:
            key, value = item.split("=", 1)
            params[key] = value
    return params


def handle_route(args: argparse.Namespace) -> None:
    print(route_task(args.prompt))


def handle_run_agent(args: argparse.Namespace) -> None:
    settings = get_settings()
    ai_services = get_ai_services(settings.ai.model_dump())
    factory = AgentFactory(ai_services=ai_services, base_config={})
    params = parse_params(args.param)
    agent = factory.create_agent(args.agent_type, agent_id=args.agent_id)
    result = agent.execute(params)
    if result is not None:
        print(result)


def handle_research(args: argparse.Namespace) -> None:
    settings = get_settings()
    ai_services = get_ai_services(settings.ai.model_dump())
    factory = AgentFactory(ai_services=ai_services, base_config={})
    agent = factory.create_agent("research", agent_id=args.agent_id)
    result = agent.execute({"query": args.query})
    if result is not None:
        print(result)


def handle_propose(args: argparse.Namespace) -> None:
    settings = get_settings()
    ai_services = get_ai_services(settings.ai.model_dump())
    factory = AgentFactory(ai_services=ai_services, base_config={})
    agent = factory.create_agent("proposal", agent_id=args.agent_id)
    result = agent.execute({})
    if result is not None:
        print(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="eufm", description="Unified CLI for EUFM Assistant"
    )
    subparsers = parser.add_subparsers(dest="command")

    route_parser = subparsers.add_parser("route", help="Suggest agent for a task")
    route_parser.add_argument("prompt", help="Task description")
    route_parser.set_defaults(func=handle_route)

    run_parser = subparsers.add_parser("run-agent", help="Run a specific agent")
    run_parser.add_argument("agent_type", help="Type of agent to run")
    run_parser.add_argument("--agent-id", default="cli-agent", help="Agent identifier")
    run_parser.add_argument(
        "--param", action="append", default=[], help="key=value parameters"
    )
    run_parser.set_defaults(func=handle_run_agent)

    research_parser = subparsers.add_parser("research", help="Run research pipeline")
    research_parser.add_argument("query", help="Research query")
    research_parser.add_argument("--agent-id", default="research-agent")
    research_parser.set_defaults(func=handle_research)

    propose_parser = subparsers.add_parser("propose", help="Generate proposals")
    propose_parser.add_argument("--agent-id", default="proposal-agent")
    propose_parser.set_defaults(func=handle_propose)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
