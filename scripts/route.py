import json
import sys

from config.logging import setup_logging
from app.api.route_task import route_task
from app.services.task_router import log_routing_decision


def main(prompt: str) -> None:
    setup_logging()
    agent, reason = route_task(prompt)
    record = log_routing_decision(prompt, agent, reason)
    print(json.dumps(record))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.route \"prompt\"")
        sys.exit(1)
    main(sys.argv[1])
