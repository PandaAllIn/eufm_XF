import os
import sys
import yaml
from pathlib import Path
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

from app.utils.ai_services import get_ai_services
from config.settings import get_settings

def main():
    """Runs a specific, detailed query on the Perplexity Sonar API."""
    print("--- Running Sonar Deep Research Query for System Optimization ---")
    
    settings = get_settings()
    
    ai_services = get_ai_services(settings.ai.dict())
    
    query_prompt = """
    As an expert AI Systems Analyst, your task is to generate a strategic guide for leveraging the Perplexity Sonar API.

    **Context:**
    We are an AI Task Force developing a system to manage Horizon Europe funding proposals. We have already integrated your API and have access to the `sonar-reasoning` and `sonar-deep-research` models.

    **Research Sources:**
    - Your own documentation: https://docs.perplexity.ai/getting-started/overview
    - Your community forums: https://community.perplexity.ai/
    - The wider web for best practices in AI research.

    **Your Task:**
    Create a comprehensive Markdown document that provides a strategic guide for our team. The guide should include:

    1.  **Advanced Prompting Techniques:**
        *   How to effectively use the `focus` parameter for domain-specific searches (e.g., academic papers, specific news outlets).
        *   Best practices for structuring prompts to get specific output formats like JSON, Markdown tables, or XML.
        *   Techniques for "Chain of Thought" or multi-step reasoning with the `sonar-deep-research` model.

    2.  **Optimal Use Cases for Stage 2 Proposal Development:**
        *   Provide a detailed breakdown of which Sonar model is best suited for the following tasks:
            *   Conducting a comprehensive scientific literature review.
            *   Identifying and profiling potential consortium partners (universities, SMEs, research institutes).
            *   Analyzing the latest EU policy and regulations relevant to our project.
            *   Performing a competitive analysis of other funded projects.

    3.  **Community Insights & Hidden Gems:**
        *   Summarize the most valuable tips, tricks, and potential pitfalls you can find from discussions on the Perplexity community forums.
        *   Identify any "hidden gem" features or undocumented techniques that could give our team a competitive edge.

    4.  **Integration Patterns:**
        *   Propose a simple Python code pattern for a "meta-agent" that can take a high-level goal (e.g., "analyze competitor X") and break it down into a series of optimized prompts for the Sonar API.
    """
    
    print(f"\nSending query to sonar-deep-research...")
    
    response = ai_services.query_perplexity_sonar(query_prompt, model="sonar-deep-research")
    
    print("\n--- Response from Perplexity Sonar ---")
    print(response)
    print("------------------------------------")
    
    # Save the response to a file for future reference
    response_file = project_root / "docs" / "PERPLEXITY_STRATEGY.md"
    with open(response_file, "w") as f:
        f.write(response)
    print(f"\nOptimization plan saved to: {response_file}")


if __name__ == "__main__":
    main()