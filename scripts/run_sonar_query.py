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
    """Runs a specific, detailed query on the Perplexity Sonar API."""
    print("--- Running Sonar Deep Research Query for System Optimization ---")
    
    settings = load_settings()
    
    if not settings.get("perplexity_api_key"):
        print("Error: PERPLEXITY_API_KEY not found in .env file.")
        return
        
    ai_services = get_ai_services(settings)
    
    query_prompt = """
    As an expert in software engineering and AI-driven development workflows, analyze the following project structure and provide a detailed plan for optimization.
    **Project Goal:** A system to manage and prepare a Horizon Europe funding proposal.
    **Core Components:**
    1.  A Python/Flask web dashboard for user interaction.
    2.  A set of Python-based AI 'agents' for specific tasks (research, document generation, coordination).
    3.  A centralized `ai_services.py` module that provides access to multiple external AI APIs (Google Gemini, OpenAI Codex, Perplexity Sonar).
    4.  Configuration is managed via `.yaml` and `.env` files.
    **Key Challenges:**
    *   The agent scripts have hardcoded file paths.
    *   The overall architecture needs to be more robust and scalable for future tasks.
    *   We need a clean, professional, and maintainable codebase.
    **Your Task:**
    Provide a step-by-step plan to refactor and professionalize this codebase. The plan should include:
    1.  **Configuration Management:** Best practices for managing settings and API keys, moving away from hardcoded paths. Suggest a specific Python library (e.g., Pydantic, Dynaconf) and provide a brief code example.
    2.  **Code Structure:** Recommend an improved directory structure for a scalable Python application.
    3.  **Agent Refactoring:** Propose a design pattern (e.g., Strategy Pattern, Factory Pattern) to refactor the individual agent scripts into a more cohesive and extensible system.
    4.  **Error Handling & Logging:** Suggest a robust strategy for implementing centralized logging and error handling across the application.
    5.  **Dependency Management:** Recommend the best tool (`pip-tools`, `Poetry`, `PDM`) for managing Python dependencies to ensure reproducible builds.
    """
    
    print(f"\nSending query to sonar-deep-research...")
    
    response = ai_services.query_perplexity_sonar(query_prompt, model="sonar-deep-research")
    
    print("\n--- Response from Perplexity Sonar ---")
    print(response)
    print("------------------------------------")
    
    # Save the response to a file for future reference
    response_file = project_root / "docs" / "system_optimization_plan.md"
    with open(response_file, "w") as f:
        f.write(response)
    print(f"\nOptimization plan saved to: {response_file}")


if __name__ == "__main__":
    main()
