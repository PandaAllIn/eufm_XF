import os
import sys
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Add src to the Python path
project_root = Path(__file__).resolve().parents[1]
sys.path.append(str(project_root / "src"))

from eufm_assistant.utils.ai_services import get_ai_services

def load_settings():
    """Loads settings from the YAML file and environment variables."""
    # Load environment variables from .env file
    load_dotenv(project_root / ".gemini" / ".env")
    
    # Load settings from YAML file
    settings_path = project_root / "src" / "eufm_assistant" / "ai_assistant" / "config" / "settings.yaml"
    with open(settings_path, "r") as f:
        settings = yaml.safe_load(f)
        
    # Add API keys from environment variables to settings
    settings["perplexity_api_key"] = os.getenv("PERPLEXITY_API_KEY")
    
    return settings

def main():
    """Tests the Perplexity Sonar API integration."""
    print("--- Running Perplexity Sonar API Test ---")
    
    settings = load_settings()
    
    if not settings.get("perplexity_api_key"):
        print("Error: PERPLEXITY_API_KEY not found in .env file.")
        return
        
    ai_services = get_ai_services(settings)
    
    test_prompt = "Summarize the key findings of the Dalton Transactions paper 'Synthesis and electrochemical properties of metal(II)-carboxyethylphenylphosphinates' (DOI: 10.1039/d1dt00104c) and its relevance to Xylella fastidiosa research."
    
    print(f"\nSending test prompt to sonar-deep-research:\n'{test_prompt}'")
    
    response = ai_services.query_perplexity_sonar(test_prompt, model="sonar-deep-research")
    
    print("\n--- Response from Perplexity Sonar ---")
    print(response)
    print("------------------------------------")
    
    if "Error" in response:
        print("\nTest Failed. Please check your API key and the error message above.")
    else:
        print("\nTest Successful!")

if __name__ == "__main__":
    main()
