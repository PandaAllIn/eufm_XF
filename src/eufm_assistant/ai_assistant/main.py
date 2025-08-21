import yaml
import argparse
import json
import pathlib

from eufm_assistant.agents.research_agent import ResearchAgent
from eufm_assistant.agents.document_agent import DocumentAgent

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
    parser.add_argument("task", type=str, help="The research task to be performed by the Research Agent.")
    args = parser.parse_args()

    print("--- Starting AI Assistant ---")
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

    # 1. Run Research Agent
    print(f"\n--- Running Research Agent with Task: '{args.task}' ---")
    potential_collaborators = research_agent.run(args.task)

    if not potential_collaborators:
        print("\nNo potential collaborators found. Exiting workflow.")
        return

    # 2. Run Document Agent on each result
    print("\n--- Running Document Agent to Draft Emails ---")
    for collaborator in potential_collaborators:
        email_draft = document_agent.draft_outreach_email(collaborator)
        collaborator['outreach_email'] = email_draft

    # 3. Print the final, consolidated results
    print("\n--- Main controller received final result: ---")
    print(json.dumps(potential_collaborators, indent=2))
    print("\n--- AI Assistant Finished ---")


if __name__ == "__main__":
    # To run this script directly, you must be in the project root and run
    # `python -m src.eufm_assistant.ai_assistant.main "Your task here"`
    main()
