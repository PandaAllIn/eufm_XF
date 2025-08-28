import argparse
import json
import sys
from eufm_assistant.agents.research_agent import ResearchAgent

def main():
    """
    Generates a research plan using the ResearchAgent and prints it as JSON.
    """
    parser = argparse.ArgumentParser(description="Generate a research plan.")
    parser.add_argument("query", help="The research query.")
    args = parser.parse_args()

    try:
        agent = ResearchAgent()
        plan = agent.generate_research_plan(args.query)
        # Print the plan as a JSON string for the orchestrator (Jules) to capture.
        print(json.dumps(plan, indent=2))
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
