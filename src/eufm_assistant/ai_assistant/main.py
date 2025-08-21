import yaml
import argparse
import json
import pathlib

from eufm_assistant.agents.research_agent import ResearchAgent
from eufm_assistant.agents.document_agent import DocumentAgent
from eufm_assistant.agents.coordinator_agent import CoordinatorAgent

# The project root is now 3 levels up from this file's directory
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[3]

def load_settings():
    """Loads settings from the settings.yaml file."""
    # Use an absolute path relative to this file to be more robust
    settings_path = pathlib.Path(__file__).parent / "config" / "settings.yaml"
    try:
        with open(settings_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: The configuration file '{settings_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred while loading the settings file: {e}")
        return None

def main():
    """
    Main entry point for the AI Assistant.
    This script initializes and runs agents based on command-line arguments.
    """
    parser = argparse.ArgumentParser(description="AI Assistant for Project Management")
    parser.add_argument(
        'agent',
        type=str,
        choices=['coordinator', 'research'],
        help="The agent to run ('coordinator' or 'research')."
    )
    parser.add_argument(
        'task',
        type=str,
        nargs='?',
        default="",
        help="The research task for the Research Agent."
    )
    args = parser.parse_args()

    print("--- Starting AI Assistant ---")
    settings = load_settings()
    if not settings:
        print("Could not load settings. Exiting.")
        return

    if args.agent == 'coordinator':
        print("\n--- Running Coordinator Agent ---")
        coordinator = CoordinatorAgent(settings)
        coordinator.load_context_from_file('project_brief', PROJECT_ROOT / "Horizon_Xilella.md")
        coordinator.load_context_from_file('architecture_design', PROJECT_ROOT / "ARCHITECTURAL_DESIGN.md")
        coordinator.load_context_from_file('wbs', PROJECT_ROOT / "project_wbs.yaml")

        plan = coordinator.generate_strategic_plan()

        print("\n--- Coordinator Agent's Strategic Plan: ---")
        for i, goal in enumerate(plan, 1):
            print(f"{i}. {goal}")

    elif args.agent == 'research':
        if not args.task:
            print("ERROR: The 'research' agent requires a task argument.")
            parser.print_help()
            return

        print("\n--- Running Full 'Research -> Draft' Workflow ---")
        research_agent = ResearchAgent(settings)
        document_agent = DocumentAgent(settings)
        document_agent.load_project_brief(PROJECT_ROOT / "Horizon_Xilella.md")

        potential_collaborators = research_agent.run(args.task)

        if not potential_collaborators:
            print("\nNo potential collaborators found. Exiting workflow.")
            return

        for collaborator in potential_collaborators:
            email_draft = document_agent.draft_outreach_email(collaborator)
            collaborator['outreach_email'] = email_draft

        print("\n--- Main controller received final result: ---")
        print(json.dumps(potential_collaborators, indent=2))

    print("\n--- AI Assistant Finished ---")


if __name__ == "__main__":
    # To run this script directly, you must be in the project root and run
    # `python -m src.eufm_assistant.ai_assistant.main "Your task here"`
    main()
