from pathlib import Path
from typing import Any, Dict

from app.agents.stage2_research_agent import Stage2ResearchAgent, save_research_tasks
from app.utils.ai_services import AIServices, get_ai_services


def run_stage2_research_pipeline(
    query: str,
    output_dir: Path,
    ai_services: AIServices,
    agent_config: Dict[str, Any] | None = None,
):
    agent = Stage2ResearchAgent(
        "stage2-research-agent", agent_config or {}, ai_services
    )
    tasks = agent.run({"query": query})
    save_research_tasks(tasks, output_dir)
    return tasks


if __name__ == "__main__":
    import argparse
    import json
    import os

    parser = argparse.ArgumentParser(description="Run Stage 2 research pipeline")
    parser.add_argument("query", help="Research query")
    parser.add_argument(
        "--output", default="stage2", help="Directory to store research plan"
    )
    args = parser.parse_args()

    settings = {"perplexity_api_key": os.environ.get("PERPLEXITY_API_KEY", "")}
    ai_services = get_ai_services(settings)
    output_dir = Path(args.output)
    tasks = run_stage2_research_pipeline(args.query, output_dir, ai_services)
    print(json.dumps({"tasks": tasks}, indent=2))
