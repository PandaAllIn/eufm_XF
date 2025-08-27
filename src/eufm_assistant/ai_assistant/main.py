import argparse
import sys
from eufm_assistant.agents.research_agent import ResearchAgent
from eufm_assistant.agents.document_agent import DocumentAgent
from eufm_assistant.agents.coordinator_agent import CoordinatorAgent

def main():
    parser = argparse.ArgumentParser(description="AI Assistant for EUFM Project")
    parser.add_argument("task", help="The task for the AI assistant to perform.")
    parser.add_argument("--query", help="The research query for the research agent.")
    args = parser.parse_args()
    if args.task == "find_partners":
        if not args.query:
            print("Error: The --query argument is required for the 'find_partners' task.")
            sys.exit(1)
        print(f"Starting the research agent to find partners with query: {args.query}")
        research_agent = ResearchAgent()
        partner_data = research_agent.run(args.query)
        if partner_data:
            print("\n--- Research Agent Found the Following Potential Partners ---")
            print(partner_data)
            print("\n--- Starting Document Agent to Draft Outreach Emails ---")
            document_agent = DocumentAgent()
            emails = document_agent.draft_outreach_emails(partner_data)
            print("\n--- Document Agent Drafted the Following Emails ---")
            for email in emails:
                print("---")
                print(email)
            print("---")
        else:
            print("The research agent did not find any partners.")
    elif args.task == "coordinate":
        print("Starting the Coordinator Agent...")
        coordinator_agent = CoordinatorAgent()
        coordinator_agent.run()
    else:
        print(f"Unknown task: {args.task}")
        sys.exit(1)

if __name__ == "__main__":
    main()
