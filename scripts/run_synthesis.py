import argparse
import json
import sys
from eufm_assistant.agents.research_agent import ResearchAgent

def main():
    """
    Synthesizes raw data into structured JSON using the ResearchAgent.
    """
    parser = argparse.ArgumentParser(description="Synthesize research data.")
    parser.add_argument("query", help="The original research query.")
    parser.add_argument("data_file", help="The path to the file containing the raw research data.")
    args = parser.parse_args()

    try:
        with open(args.data_file, 'r') as f:
            raw_data = f.read()

        agent = ResearchAgent()
        structured_results = agent.synthesize_results(args.query, raw_data)

        print(json.dumps(structured_results, indent=2))

    except FileNotFoundError:
        print(f"Error: Data file not found at {args.data_file}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
