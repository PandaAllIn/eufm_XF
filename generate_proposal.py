import yaml
import pathlib
from src.eufm_assistant.agents.proposal_agent import ProposalAgent

def load_settings():
    """Loads settings from the YAML file."""
    settings_path = (
        pathlib.Path(__file__).resolve().parent
        / "src"
        / "eufm_assistant"
        / "ai_assistant"
        / "config"
        / "settings.yaml"
    )
    try:
        with open(settings_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: Settings file not found at {settings_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing settings YAML file: {e}")
        return None

def main():
    """
    Main entry point for generating the proposal.
    """
    print("--- Starting Proposal Generation ---")

    settings = load_settings()
    if not settings:
        print("Could not load settings. Exiting.")
        return

    proposal_agent = ProposalAgent(settings)
    proposal_content = proposal_agent.generate_stage1_proposal()

    print("\n--- Generated Proposal ---")
    print(proposal_content)
    print("\n--- Proposal Generation Finished ---")

if __name__ == "__main__":
    main()
