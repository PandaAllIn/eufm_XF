import argparse
import json
import pathlib
import yaml

from eufm_assistant.agents.research_agent import ResearchAgent
from eufm_assistant.agents.document_agent import DocumentAgent
from eufm_assistant.agents.coordinator_agent import CoordinatorAgent

# The project root is 3 levels up from this file's directory
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[3]

def load_settings():
    """Loads settings from the YAML file."""
    settings_path = PROJECT_ROOT / "src" / "eufm_assistant" / "ai_assistant" / "config" / "settings.yaml"
    try:
        with open(settings_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: Settings file not found at {settings_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing settings YAML file: {e}")
        return None

def main():
    """
    Main entry point for the AI Assistant.
    This script initializes and runs agents based on command-line arguments.
    """
    parser = argparse.ArgumentParser(description="AI Assistant for Project Management")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # Research command
    parser_research = subparsers.add_parser("research", help="Run the research agent to find collaborators.")
    parser_research.add_argument("query", type=str, help="The research query for the research agent.")

    # Coordinate command
    parser_coordinate = subparsers.add_parser("coordinate", help="Run the coordinator agent for strategic tasks.")
    parser_coordinate.add_argument("--task", default="wbs_status", help="The specific task for the coordinator agent (e.g., 'proposal_checklist').")

    args = parser.parse_args()

    print("--- Starting AI Assistant ---")

    if args.command == "coordinate":
        coordinator_agent = CoordinatorAgent()
        coordinator_agent.run(task=args.task)
        # We return early for the coordinator as it doesn't follow the research->document workflow
        print("\n--- AI Assistant Finished ---")
        return

    # The rest of the function handles the 'research' command
    settings = load_settings()
    if not settings:
        print("Could not load settings. Exiting.")
        return

    # Initialize Agents
    print("--- Initializing Agents ---")
    research_agent = ResearchAgent(settings)
    document_agent = DocumentAgent(settings)

    # Load context into Document Agent
    brief_path = PROJECT_ROOT / "Horizon_Xilella.md"
    document_agent.load_project_brief(brief_path)

    # --- Execute a full workflow: Research -> Draft ---
    print(f"\n--- Running Research Agent with Query: '{args.query}' ---")
    potential_collaborators = research_agent.run(args.query)

    if not potential_collaborators:
        print("\nNo potential collaborators found. Exiting workflow.")
        return

    print("\n--- Running Document Agent to Draft Emails ---")
    for collaborator in potential_collaborators:
        email_draft = document_agent.draft_outreach_email(collaborator)
        collaborator['outreach_email'] = email_draft

    print("\n--- Main controller received final result: ---")
    print(json.dumps(potential_collaborators, indent=2))

    print("\n--- AI Assistant Finished ---")

if __name__ == "__main__":
    # Example commands:
    # python -m src.eufm_assistant.ai_assistant.main research "Find experts on Xylella fastidiosa in Italy"
    # python -m src.eufm_assistant.ai_assistant.main coordinate --task proposal_checklist
    main()
