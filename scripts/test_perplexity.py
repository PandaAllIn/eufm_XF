from pathlib import Path
from dotenv import load_dotenv

from config.settings import get_settings
from app.utils.ai_services import AIServices


def load_settings():
    """Load settings from environment variables using Pydantic settings."""
    project_root = Path(__file__).resolve().parents[1]
    load_dotenv(project_root / ".gemini" / ".env")
    settings = get_settings()
    return settings.ai.dict()


def main():
    """Tests the Perplexity Sonar API integration."""
    print("--- Running Perplexity Sonar API Test ---")

    settings = load_settings()

    if not settings.get("perplexity_api_key"):
        print("Error: PERPLEXITY_API_KEY not found in .env file.")
        return

    ai_services = AIServices(settings)

    test_prompt = "Summarize the key findings of the Dalton Transactions paper 'Synthesis and electrochemical properties of metal(II)-carboxyethylphenylphosphinates' (DOI: 10.1039/d1dt00104c) and its relevance to Xylella fastidiosa research."

    print(f"\nSending test prompt to sonar-deep-research:\n'{test_prompt}'")

    response = ai_services.query_perplexity_sonar(
        test_prompt, model="sonar-deep-research"
    )

    print("\n--- Response from Perplexity Sonar ---")
    print(response)
    print("------------------------------------")

    if "Error" in response:
        print("\nTest Failed. Please check your API key and the error message above.")
    else:
        print("\nTest Successful!")


if __name__ == "__main__":
    main()
