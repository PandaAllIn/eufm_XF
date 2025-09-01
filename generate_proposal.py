from app import create_app


def main():
    """Generate the Stage 1 proposal using the application factory."""
    print("--- Starting Proposal Generation ---")
    app = create_app()
    proposal_agent = app.agent_factory.create_agent("proposal", "proposal-generator")
    proposal_content = proposal_agent.run({})
    print("\n--- Generated Proposal ---")
    print(proposal_content)
    print("\n--- Proposal Generation Finished ---")


if __name__ == "__main__":
    main()
